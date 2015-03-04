from tweepy import streaming
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import csv
import json
import datetime
import time
#import tweepy package


consumer_key='WbREEJKoXbv8DrlWMzRwHCPtm'
consumer_secret='WZeUQfjMDESe5Mp60WagJv61veSvgpOCk85yF4wmMZo4CnH3HM'

access_token='3000677634-7Os7M2jtgJCCChqiRAd57gLgjqKw1GqKHxNDUJS'
axxess_secret_token='dozZjqK9SSRJ4QvCURdtNXvp6mnjHv7pFV3qK55ejPb1N'

keywords=['nexus5','samsunggalaxy','nexus6','nexus',
                            'iphone','iphone5s','iphone6plus','iphone6','6plus','iphone6+',
                            'iphone5','htcone','htc1','oneplus','galaxys5','xperia','sonyxperia',
                            'Alcatelonetouch','alcatelfierce']

tweet={}

class listener(StreamListener):    
    def on_status(self,status):
        omitwords=['price','USD','Price','$','games','case','iphonegames','deals','game','sale','advertisement','sex','porn','pornography']
        tweet_text=status.text.encode("utf-8")
        for word in omitwords:
            if(word not in tweet_text.split()):
                for words in tweet_text.split():
                    if(words in keywords):
                        tweet_id=int(status.id)
                        if(tweet_id not in tweet.keys()):    
                            tweet_created=status.created_at.date()
                            a= [[tweet_id,tweet_created,tweet_text,words]]
                            tweet[tweet_id]= a
                            print tweet
                            f=open('tweets.csv', "a+")
                            writer = csv.writer(f)
                            writer.writerows(a)
                else:
                    x=1
            else:
                k=1            


    def on_error(self, status):
        print status

    

auth= OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,axxess_secret_token)
twitterStream= Stream(auth,listener())
#twitterStream.filter(track=['iphone,iphone5s,iphone6plus,iphone6,6plus,iphone6+,iphone5'],languages = ['en'])
twitterStream.filter(track=['nexus5','samsunggalaxy','nexus6','nexus',
                            'iphone','iphone5s','iphone6plus','iphone6','6plus','iphone6+',
                            'iphone5','htcone','htc1','oneplus','galaxys5','xperia','sonyxperia',
                            'Alcatelonetouch','alcatelfierce'],languages = ['en'])

