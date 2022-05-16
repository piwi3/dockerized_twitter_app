## Sentiment analysis of twitter tweets via dockerized pipeline

- Leveraged __Tweepy__ and the __Twitter developer API__ to download tweets from twitter via __customized querries__ (e.g., tweet mentions user x, timeline of user y until date z, discard retweets etc.)
- Built a __data pipeline__ using __docker__ (more precisely __docker-compose__), i.e., stored all tweets in __Mongo DB__, created an __ETL job__ (data cleaning, preparation) transferring the data to __PostgreSQL__, ran a __sentiment analysis__ leveraging [Vader](https://github.com/cjhutto/vaderSentiment)  
- Finally built a small webpage with __streamlit__ to __display the results__ of a querry in realtime (also dockerized)

_Note: To run the code, a credentials.py file with personal API keys and postgres info (see Dockerfile) needs to be added in the 'streamlit_app' folder._

<img src="https://github.com/piwi3/dockerized_twitter_app/blob/main/images/twitter_sentiment_app.png" width=800><br/>
_Figure 1: Frontend of my twitter sentiment app (created with streamlit)_
