from tweepy import streaming
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import csv
import json
import datetime
import time
from threading import Timer
import time
import sys
import traceback
from textblob import TextBlob
from pymongo import Connection
import pymongo
from pymongo import MongoClient

#Connection string
c= MongoClient()
db=c.se # mongoDatabase



consumer_key='WbREEJKoXbv8DrlWMzRwHCPtm'
consumer_secret='WZeUQfjMDESe5Mp60WagJv61veSvgpOCk85yF4wmMZo4CnH3HM'

access_token='3000677634-7Os7M2jtgJCCChqiRAd57gLgjqKw1GqKHxNDUJS'
access_secret_token='dozZjqK9SSRJ4QvCURdtNXvp6mnjHv7pFV3qK55ejPb1N'


#Consumer keys and access keys
#consumer_key='v9ldUGSWVpGNwSijNGc9KTava'
#consumer_secret='AdannwtH6L8wl5Zv57hhiP6Vg2EAtHx0yIzs0sqYGpHwWa0v88'
#=======
#consumer_key=' '
#consumer_secret=' '
#>>>>>>> efd6b3dbfaea517139e544491779b9c61d1c24b8

#access_token=' '
#access_secret_token=' '

#dictionary to contain tweets where key = tweet_id and value=tweet_information
tweet={}

#read keywords contained in a file and convert them to lower case
def Read_file(filename):
    fp = open(filename, "r")
    data = fp.readlines();
    fp.close()
    keywords =[]
    for line in data :
        keywords.append(line.strip('\n').lower());
    return keywords

#return index of the keyword
def Index_of_keyword(tweet, keyword):
    for i in range (0,len(keyword)):
        
        if keyword[i] in tweet:
           return i
        
    return -1

#return a tweet devoid of ascci characters
def Remove_non_ascci_characters(tweet):

    tweet_without_aascii = "";
    for c in tweet:
        if ord(c)>0 and ord(c) < 127:
            tweet_without_aascii = tweet_without_aascii + c;

    return tweet_without_aascii;

#remove url in a tweet
def Remove_url_and_at_name_from_tweet(tweet):
    words = tweet.split(' ');

    tweet_without_http="";
    for x in range(0,len(words)):
        if 'http' not in words[x] and '@' not in words[x]:
            tweet_without_http += " "+words[x];
    return tweet_without_http;


class listener(StreamListener):    
    def on_status(self,status):

        tweet_text=status.text;
        tweet_text = Remove_non_ascci_characters(tweet_text).lower().replace(',',' ');
        tweet_str = str(tweet_text);
        tweet_str = Remove_url_and_at_name_from_tweet(tweet_str);
        
        
        try:
            
            index=Index_of_keyword(tweet_text,keywords);
            
            if  index != -1:
                    
                tweet_id=int(status.id)
                if(tweet_id not in tweet.keys()):    
                    tweet_created=str(status.created_at.date())
                    tweet_details= [[tweet_id,tweet_created,tweet_str,keywords[index]]]
                    tweet[tweet_id]= tweet_details;
                    senti = TextBlob(tweet_str);
                    senti.sentiment

                    #-----------------------------------code to insert values into the database

                    x={'tweet_id':tweet_id,'date':tweet_created,'tweet':tweet_str,'keyword':keywords[index],'polarity':senti.sentiment.polarity}
                    print x
                    db.tweets.insert(x)
                    #----------------------------------
                    #print tweet_str, 'keyword:',keywords[index], 'polarity:',senti.sentiment.polarity
                                      
                    #f=open('tweets_new_elections.csv', 'a+')
                    #writer = csv.writer(f);
                    #writer.writerows(tweet_details);

        except Exception, err:
            print "....Exception";
            print traceback.format_exc()
            
            
    def on_error(self, status):
        print(status);

keywords = Read_file('contestants.txt');

    
auth= OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret_token)
twitterStream= Stream(auth,listener())
twitterStream.filter(track=keywords,languages = ['en'])




