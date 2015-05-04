import re
import traceback
import sys

def ReadRowsInFile(filename):
    #print filename
    fp = open(filename, "r")
    data = fp.readlines()
    
    fp.close()
    rows =[]

    for row in data:
        rows.append(row.strip('\n'));

    return rows
 
def ReadCsvFile(filename):
    print filename
    fp = open(filename, "r")
    data = fp.readlines()
    
    fp.close()
    tweets =[]
    
    for line in data :
        #print line

        line = line.replace('\"','');
        tuple_=(line.lower().strip('\n').split(','));
        #print tuple_[2]
        t = "";
        
        if len(tuple_) > 3:
            if len(tuple_[2]) > 0:
                tweets.append(tuple_[2])
    #print tweets
    return tweets

def CleanData(tweets,contestants):

    tweets_cleaned = [];
    #remove http.

    for x in range(0,len(tweets)-1):
        tweet = tweets[x];
        
        tweet_words = tweet.split(' ');
        #print tweet_words; 

        cleaned_tweet = "";
        for i in range(0,len(tweet_words)):
            #print tweet_words[i];
            #raw_input();
            if '#' not in tweet_words[i] and 'http' not in tweet_words[i] and 'rt' not in tweet_words[i] and '@' not in tweet_words[i] and len(tweet_words)>0:
                cleaned_tweet = cleaned_tweet+" " + tweet_words[i];

        #print cleaned_tweet 

        for i in range(0,len(contestants)):
            cleaned_tweet = cleaned_tweet.replace(contestants[i],' ');

        #print cleaned_tweet     
        cleaned_tweet = (re.sub('[^0-9a-zA-Z ]', '', cleaned_tweet)).strip();
        #print cleaned_tweet;
        #raw_input();
        if cleaned_tweet not in tweets_cleaned and len(cleaned_tweet) > 0 :
            tweets_cleaned.append(cleaned_tweet);   
        
   
    return tweets_cleaned
        

        
def WriteToFile(filename, tweet,op):
    file = open(filename, op)

    file.write(tweet+'\n')

    file.close()

def CountClassifiedNumbers():
    count =0;
    try:
        count =count+ len(ReadRowsInFile('pos.csv'));
    except:
        #print traceback.format_exc()
        pass

    try:
        #print len(ReadRowsInFile('neg.csv'))
        count  = count+ len(ReadRowsInFile('neg.csv'));
    except:
        #print traceback.format_exc()
        pass

    try:
        #print len(ReadRowsInFile('neu.csv'))
        count = count+ len(ReadRowsInFile('neu.csv'));
    except:
        #print traceback.format_exc()
        pass

    #print 'count', count
    return count;

def CheckIfFileExists(filename):
    try:
        fp = open(filename, "r");
        return True;
    except:
        return False;

def ClassifyTweets(filename):

    tweets = ReadCsvFile(filename);
    contestants = ReadRowsInFile('contestants.txt');
    
    bool_val=CheckIfFileExists('cleaned_tweets.txt');
    #print bool_val 
    if bool_val == False:
        cleaned_tweets=CleanData(tweets, contestants);
        for x in range(0,len(cleaned_tweets)):
            WriteToFile('cleaned_tweets.txt',cleaned_tweets[x],'a')
    
    start = CountClassifiedNumbers();
    #print start
    
    rows = ReadRowsInFile('cleaned_tweets.txt');

    print '0- neutral';
    print '1- positive';
    print '2- negative\n\n';
    for x in range(start, len(rows)):
        print (x+1),'.',rows[x];
        response=raw_input("response:");
        
        
        while response != '0' and response !='1' and response !='2':
            print (x+1),'.',rows[x];
            response=raw_input("response:");

        if response=='0':
            WriteToFile('neu.csv',rows[x],'a');

        if response=='1':
            WriteToFile('pos.csv',rows[x],'a');

        if response=='2':
            WriteToFile('neg.csv',rows[x],'a');

ClassifyTweets('tweets.csv');   
            
    
