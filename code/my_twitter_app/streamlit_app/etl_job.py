# Import relevant modules and functions

# Data wrangling
import pandas as pd
import re

# Sentiment analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Databases
import pymongo
from sqlalchemy import create_engine

#############################
### Get data from mongodb ###
#############################

def extract():
    # Establish a connection to the MongoDB server
    client = pymongo.MongoClient(host="mongodb", port=27017)

    # Select the database to use within the MongoDB container
    db = client.twitter

    # Get tweets from mongodb
    docs = db.tweets.find()

    #Test
    #for doc in docs:
    #   print(doc['text'])

    return docs

######################
### Transform data ###
######################

def transform(docs):

    tweets = [doc['text'] for doc in docs]
    df = pd.DataFrame(tweets, columns=['tweet_text'])

    # Clean data

    new_line=r'\n\n|\n'
    mentions_regex= r'@[A-Za-z0-9]+'  # "+" means one or more times
    url_regex=r'https?:\/\/\S+' # this will catch most URLs; "?" means 0 or 1 time; "S" is anything but whitespace
    hashtag_regex= r'#'
    rt_regex= r'RT\s'

    def clean_tweets(tweet):
        tweet = re.sub(new_line, '', tweet)  # removes line breaks
        tweet = re.sub(mentions_regex, '', tweet)  # removes @mentions
        tweet = re.sub(hashtag_regex, '', tweet) # removes hashtag symbol
        tweet = re.sub(rt_regex, '', tweet) # removes RT to announce retweet
        tweet = re.sub(url_regex, '', tweet) # removes most URLs
        return tweet

    df['tweet_text'] = df['tweet_text'].apply(clean_tweets)

    # Perform sentiment analysis

    analyser = SentimentIntensityAnalyzer() 
    pol_scores = df['tweet_text'].apply(analyser.polarity_scores).apply(pd.Series)

    df['compound'] = pol_scores['compound']
    df.reset_index(inplace = True)
    
    return df

#################################
### Load data into postgreSQL ###
#################################

def load(df):
        
    # Get credentials for postgresdb
    try:
        from streamlit_app.credentials import POSTGRES_USER
        from streamlit_app.credentials import POSTGRES_PASSWORD
        from streamlit_app.credentials import POSTGRES_DB
    except:
        from credentials import POSTGRES_USER
        from credentials import POSTGRES_PASSWORD
        from credentials import POSTGRES_DB

    # Create postgres engine
    pg = create_engine(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgresdb:5432/{POSTGRES_DB}')

    # Create table in postgres
    pg.execute('CREATE TABLE IF NOT EXISTS tweets (text VARCHAR(500), sentiment NUMERIC);')

    # Load data into table
    df.to_sql('tweets', pg, if_exists='replace', index=False)
    pg.execute('ALTER TABLE tweets ADD PRIMARY KEY ("index")')

    return None