# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 20:13:49 2019

@author: LENOVO
"""

import tweepy
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from wordcloud import WordCloud
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator

analyser = SentimentIntensityAnalyzer()
translator = Translator()

ACCESS_TOKEN = '1152950533583331328-0Sj63UT39UbQJxlAASI7HSC8JjgMDZ'
ACCESS_SECRET = 'Gp8Na6qKNgdWCFplu4VGfMb39qDEy0eeidDlO3nfj7Juk'
CONSUMER_KEY = '1xu2YEB7fGektQdYSbhlTl75c'
CONSUMER_SECRET = '7zhkssfgqq1V8lZI4LBjRvWS1m3f7heajBvSYdTT62BNTkgMG0'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def connect_twitter_OAuth():
    
    tweets = api.user_timeline('@WWF_ID', count=200, tweet_mode='extended')
    for t in tweets:
      print(t.full_text)
      print()

def list_tweets(user_id, count, prt=False):
    tweets = api.user_timeline(
        "@" + user_id, count=count, tweet_mode='extended')
    tw = []
    for t in tweets:
        tw.append(t.full_text)
        if prt:
            print(t.full_text)
            print()
    return tw

def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)        
    return input_txt

def _removeNonAscii(s): 
    return "".join(i for i in s if ord(i)<128)

def clean_text(text):
    text = text.lower()
    text = re.sub(r"what's", "what is", text)
    text = text.replace('(ap)', '')
    text = re.sub(r"\'s", "is", text)
    text = re.sub(r"\'ve", "have", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"n't", "not", text)
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"\'re", "are", text)
    text = re.sub(r"\'dgn", "dengan", text)
    text = re.sub(r"\'yg", "yang", text)
    text = re.sub(r"utk", "untuk", text)     
    text = re.sub(r"nya", "", text)
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r"\\", "", text)
    text = re.sub(r"\'", "", text)    
    text = re.sub(r"\"", "", text)
    text = re.sub('[^a-zA-Z ?!]+', '', text)
    text = re.sub('https?://[A-Za-z0-9./]*', '', text)
    text = _removeNonAscii(text)
    text = text.strip()
    return text

def clean_lst(lst):
    lst_new = []
    for r in lst:
        lst_new.append(clean_text(r))
    return lst_new

def clean_tweets(lst):    
    
    # remove twitter Return handles (RT @xxx:)
    lst = np.vectorize(remove_pattern)(lst, "rt @[\w]*:")
    # remove twitter handles (@xxx)
    lst = np.vectorize(remove_pattern)(lst, "@[\w]*")
    # remove URL links (httpxxx)
    lst = np.vectorize(remove_pattern)(lst, "https?://[A-Za-z0-9./]*")
    # remove punctuation 
    lst = np.core.defchararray.replace(lst, "[^\w\s]+", "")
    # remove special characters, numbers, punctuations (except for #)
    lst = np.core.defchararray.replace(lst, "[^a-zA-Z#]", " ")
    return lst

def sentiment_analyzer_scores(text, engl=True):
    if engl:
        trans = text
    else:
        trans = translator.translate(text).text
    score = analyser.polarity_scores(trans)
    lb = score['compound']
    if lb >= 0.05:
        return 1
    elif (lb > -0.05) and (lb < 0.05):
        return 0
    else:
        return -1

user_id = 'WWF_ID'
count=200

tw_wwfid = list_tweets(user_id, count)

stop_words = []
f = open('D:\DTS FGA 2019 - Unmul\Data\stopwords_indonesia.txt', 'r')
for l in f.readlines():
    stop_words.append(l.replace('\n', '')) 
additional_stop_words = ['t', 'will']
stop_words += additional_stop_words

print(len(stop_words))

tw_wwfid = clean_tweets(tw_wwfid)

tw_wwfid[10]
sentiment_analyzer_scores(tw_wwfid[10])

def anl_tweets(lst, title='Tweets Sentiment', engl=True ):
    sents = []
    for tw in lst:
        try:
            st = sentiment_analyzer_scores(tw, engl)
            sents.append(st)
        except:
            sents.append(0)
    ax = sns.distplot(
        sents,
        kde=False,
        bins=3)
    ax.set(xlabel='Negative                Neutral                 Positive',
           ylabel='#Tweets',
          title="Tweets of @"+title)
    return sents

tw_wwfid_sent = anl_tweets(tw_wwfid, user_id)

def word_cloud(wd_list):
    stopwords = stop_words + list('stopwords')
    all_words = ' '.join([text for text in wd_list])
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        width=1600,
        height=800,
        random_state=21,
        colormap='jet',
        max_words=50,
        max_font_size=200).generate(all_words)
    plt.figure(figsize=(12, 10))
    plt.axis('off')
    plt.imshow(wordcloud, interpolation="bilinear");
    plt.show()
    
word_cloud(tw_wwfid)

#user_id = 'WWF_ID'
#tw_wwfid = list_tweets(user_id, count)
#tw_wwfid = clean_tweets(tw_wwfid)
#tw_wwfid_sent = anl_tweets(tw_wwfid, user_id)
#word_cloud(tw_wwfid)