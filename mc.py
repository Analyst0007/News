# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 07:51:35 2025

@author: Hemal
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from apscheduler.schedulers.background import BackgroundScheduler

# Function to fetch news
def fetch_news():
    url = "https://www.moneycontrol.com/news/business/companies/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    news_list = []
    for item in soup.find_all('li', class_='clearfix'):
        title = item.find('h2').text.strip()
        link = item.find('a')['href']
        news_list.append({'Title': title, 'Link': link})

    return news_list

# Function to update news
def update_news():
    st.session_state.news = fetch_news()

# Initialize session state
if 'news' not in st.session_state:
    st.session_state.news = fetch_news()

# Set up scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(update_news, 'interval', minutes=15)
scheduler.start()

# Streamlit app layout
st.title("Latest Company News")

# Display news in a table
news_df = pd.DataFrame(st.session_state.news)
st.table(news_df)

# Keep the app running
while True:
    time.sleep(1)
