# Import relevant modules and functions

import tweepy
import pymongo

#############################
### Get tweets via tweepy ###
#############################

def get_tweets(search_items='Doncic', with_retweets=True, with_replies=True):

    # Get credentials for twitter API
    try:
        from streamlit_app.credentials import BEARER_TOKEN
    except:
        from credentials import BEARER_TOKEN

    # Initialize client
    client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)

    # Replace the limit=1000 with the maximum number of Tweets you want
    
    search_query = f'{search_items} lang:en' 
    if with_retweets:
        search_query = search_query + ' -is:retweet'
    if with_replies:
        search_query = search_query + ' -is:reply'

    tweets = tweepy.Paginator(
        method=client.search_recent_tweets,
        query=search_query,
        tweet_fields=['author_id', 'created_at', 'public_metrics']
    ).flatten(limit=1000)

    return tweets

################################
### Store tweets in mongo db ###
################################

def save_tweets(tweets):
    
    # Initialize mongo database -> mongodb container listens on port 27017
    client = pymongo.MongoClient(host="mongodb", port=27017)
    db = client.twitter

    # Delete collections in mongodb, if exists (docker container) 
    db.tweets.drop()

    # Store tweets in mongodb (docker container) 
    for tweet in tweets:
        db.tweets.insert_one(dict(tweet))

    return None