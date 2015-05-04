import pickle
from nltk.stem import *
from nltk.stem.porter import *
from nltk.corpus import stopwords
import string
import pickle
import re
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
from pymongo import Connection
import pymongo
from pymongo import MongoClient

#the source to the trained data is:
#https://s3.amazonaws.com/manvi123/pos.pkl
#https://s3.amazonaws.com/manvi123/neg.pkl

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

def Index_of_keyword(tweet, keyword):
    for i in range (0,len(keyword)):
        
        if keyword[i] in tweet:
           return i
        
    return -1

def ReadFileIntoDictionary(filename):
    f = open(filename, 'rb')
    obj_dict = pickle.load(f)
    f.close();
    return obj_dict;

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def ReadFile(filename):
    fp = open(filename, "r")
    data = fp.readlines()
    fp.close()
    rows =[]
    for line in data :
        #print line
        rows.append(line.strip('\n').split(','));
    return rows
    
def stem_tokens(words):
    tokens = [];
    stemmer=SnowballStemmer("english");
    for word in words:
        stemmed_word=(stemmer.stem(word));
        tokens.append(stemmed_word.encode('unicode-escape'))

    return tokens

#returns words that are not stop words
def remove_stopwords_common_words(tweet):
    tweet = tweet.lower();
    words = tweet.split(' ');
    not_stop_words = []
    stop = [u'i', u'me', u'my', u'myself', u'we', u'our', u'ours', u'ourselves', u'you', u'your', u'yours', u'yourself', u'yourselves', u'he', u'him', u'his', u'himself', u'she', u'her', u'hers', u'herself', u'it', u'its', u'itself', u'they', u'them', u'their', u'theirs', u'themselves', u'what', u'which', u'who', u'whom', u'this', u'that', u'these', u'those', u'am', u'is', u'are', u'was', u'were', u'be', u'been', u'being', u'have', u'has', u'had', u'having', u'do', u'does', u'did', u'doing', u'a', u'an', u'the', u'and', u'but', u'if', u'or', u'because', u'as', u'until', u'while', u'of', u'at', u'by', u'for', u'with', u'about', u'against', u'between', u'into', u'through', u'during', u'before', u'after', u'above', u'below', u'to', u'from', u'up', u'down', u'in', u'out', u'on', u'off', u'over', u'under', u'again', u'further', u'then', u'once', u'here', u'there', u'when', u'where', u'why', u'how', u'all', u'any', u'both', u'each', u'few', u'more', u'most', u'other', u'some', u'such', u'no', u'nor', u'only', u'own', u'same', u'so', u'than', u'too', u'very', u's', u't', u'can', u'will', u'just', u'don', u'should', u'now']
    common = ['im',"i'm"];
    for word in words:
        if word not in stop and word not in common:
            not_stop_words.append(word)
    return not_stop_words

def Remove_url_and_at_name_from_tweet(tweet):
    words = tweet.split(' ');

    tweet_without_http="";
    for x in range(0,len(words)):
        if 'http' not in words[x] and '@' not in words[x]:
            tweet_without_http += " "+words[x];
    return tweet_without_http;

def GetPolarity(stemmed_tokens, posDict, negDict):

    pos=float(1);
    neg=float(1);
    for i in range(0,len(stemmed_tokens)):
        token = stemmed_tokens[i];

        #print token;
        
        pos_no = 1;
        neg_no = 1;

        
        if token in posDict:
            pos_no = posDict[token];
            #print 'pos', pos_no
            
        if token in negDict:
            neg_no = negDict[token];
            #print 'neg', neg_no

        pos = pos * pos_no /(pos_no+neg_no);
        neg = neg * neg_no /(pos_no+neg_no);

    return pos, neg

def GetPolarity_extension(stemmed_tokens, posDict, negDict):

    pos=float(1);
    neg=float(1);

    if 'but' in stemmed_tokens:
        index = stemmed_tokens.index('but');

        stemmed_tokens = stemmed_tokens[index+1:];

        index_not = stemmed_tokens.index('not');
        if 'not' in stemmed_tokens and index_not< len(stemmed_tokens)-1:
            index = stemmed_tokens.index('not');
            stemmed_tokens = stemmed_tokens[index+1:];
            pos_no = 1;
            neg_no = 1;
            
            for i in range(0,len(stemmed_tokens)):
            
                token = stemmed_tokens[i];
                if token in posDict:
                    pos_no = posDict[token];

                if token in negDict:
                    neg_no = negDict[token];

                pos = pos * neg_no /(pos_no+neg_no);
                neg = neg * pos_no /(pos_no+neg_no);
        else:
            pos_no = 1;
            neg_no = 1;
            
            for i in range(0,len(stemmed_tokens)):
            
                token = stemmed_tokens[i];
                if token in posDict:
                    pos_no = posDict[token];

                if token in negDict:
                    neg_no = negDict[token];

                pos = pos * pos_no /(pos_no+neg_no);
                neg = neg * neg_no /(pos_no+neg_no);
                
        return pos, neg;

    if 'not' in stemmed_tokens:
        pos_no = 1;
        neg_no = 1;

        index = stemmed_tokens.index('not');
        stemmed_tokens = stemmed_tokens[index+1:];

        pos_no = 1;
        neg_no = 1;
            
        for i in range(0,len(stemmed_tokens)):
            
            token = stemmed_tokens[i];
            if token in posDict:
                pos_no = posDict[token];

            if token in negDict:
                neg_no = negDict[token];

            pos = pos * neg_no /(pos_no+neg_no);
            neg = neg * pos_no /(pos_no+neg_no);

    return pos, neg;
        
def DeterminePolarity(posDict, negDict, tweet):

    tweet=re.sub(' +',' ',tweet);
        
    words = remove_stopwords_common_words(tweet)
    stemmed_tokens = stem_tokens(words);
        
    if 'but' in stemmed_tokens or 'not' in stemmed_tokens:
        pos,neg=GetPolarity_extension(stemmed_tokens, posDict, negDict)
    else:
        pos,neg=GetPolarity(stemmed_tokens, posDict, negDict)

    res = pos - neg;
        #print res, pos, neg
    if res >0.01:
        
        print '---pos'
        return 1;
    elif res <= -0.001:
        print '---neg'
        return -1;
    else:
        print '---neu'
        return 0;

    
    
posDict=load_obj('pos'); 
negDict=load_obj('neg');

#print tweets


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
                    pol = DeterminePolarity(posDict, negDict, tweet_str);
                    

                    #-----------------------------------code to insert values into the database

                    x={'tweet_id':tweet_id,'date':tweet_created,'tweet':tweet_str,'keyword':keywords[index],'polarity':pol}
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
