#################################################################
### Main program / app, output here -> http://localhost:8501/ ###
#################################################################

# Import relevant modules and functions

# Twitter API
import tweepy

# Data wrangling
import pandas as pd
import numpy as np
import re

# Databases (postgres and mongodb)
from sqlalchemy import create_engine
import pymongo

# Import functions from other python files
try:
    from streamlit_app.tweets_collector import get_tweets, save_tweets
    from streamlit_app.etl_job import extract, transform, load
except:
    from tweets_collector import get_tweets, save_tweets
    from etl_job import extract, transform, load

# Frontend/app
import streamlit as st
import time
from bokeh.plotting import figure
from bokeh.io import show, output_notebook

#################################
### Get data from postgreSQL ###
#################################

def get_data():

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

    # Get data from postgres
    tweets = pd.read_sql_table('tweets', pg)

    return tweets

##################################
### Preapre plotting functions ###
##################################

def draw_hist(tweets, num_bins = 20, height=300, width=300):
    
    # Use numpy historgram to get data for a histogram
    arr_hist, edges = np.histogram(tweets['compound'], 
                                bins = num_bins, 
                                range = [-1, 1])

    # Put the data in a dataframe
    df = pd.DataFrame({'arr_sentiment': arr_hist, 
                        'left': edges[:-1], 
                        'right': edges[1:]})

    # Create the blank plot
    p = figure(plot_height = height,#plot_width = width, 
        title = 'Histogram of sentiment evaluation',
        x_axis_label = 'Sentiment evaluation', 
        y_axis_label = 'Number of tweets')

    # Add a quad glyph
    p.quad(bottom=0, top=df['arr_sentiment'], 
       left=df['left'], right=df['right'], 
       fill_color='red', line_color='black')
    
    return p

######################################
### Create front end via streamlit ###
######################################

# Add title
col1, col2 = st.columns([1, 5])

with col1:
    st.image('twitter.png', width = 100)
with col2:
    st.title('Twitter sentiment analysis')

# Create a form to enable customized search queries
#form = st.form('search_request')

 # Design query options
with st.form("my_form"):
    with st.sidebar:
        # Add title
        st.header('Conduct a query')
        # Get search request
        search_items = st.text_input('What do you want to search for in recent tweets?', 'Doncic')

        # Include retweets?
        with_retweets = st.checkbox('Include retweets')

        # Include replies?
        with_replies = st.checkbox('Include replies')

        # Every form must have a submit button.
        submitted = st.form_submit_button("Start query")

# Run python when search request is submitted
if submitted:
    # Get tweets
    tweets = get_tweets(search_items, with_retweets, with_replies)
    
    # Save tweets in mongodb
    save_tweets(tweets)

    # Perform etl_job
    load(transform(extract()))

    # Get data for query
    tweets = get_data()

# Draw a histogram

if submitted:
    p = draw_hist(tweets)
    st.bokeh_chart(p, use_container_width=True)
else:
    st.markdown('_Histogram will be plotted once a search was conducted._')

# Display twitter_icon and collected tweets

# Display content
with st.expander("Look at the collected tweets"):
    if submitted:
        with st.empty():
            while True:
                for row in tweets.iterrows():
                    st.markdown(f'_"{row[1][1]}"_ \n\n__Sentiment: {round(row[1][2],2)}__')
                    time.sleep(5)
                st.write("All tweets shown - restarting...")
                time.sleep(5)
    else:
        st.markdown('_Tweets will be displayed, once a search was conducted._')