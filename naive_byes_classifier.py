#from __future__ import print_function
from nltk.stem import *
from nltk.stem.porter import *
from nltk.corpus import stopwords
import string
import pickle

'''

This file implemets nad trains the bayesian classifier

'''

#write dictioanry to file source:http://stackoverflow.com/questions/19201290/python-how-to-read-save-dict-to-file
def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        
#read disctionary from file source:http://stackoverflow.com/questions/19201290/python-how-to-read-save-dict-to-file
def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
    
#returns stemmed words
def stem_tokens(words):
    tokens = [];
    stemmer=SnowballStemmer("english");
    for word in words:
        stemmed_word=(stemmer.stem(word));
        tokens.append(stemmed_word.encode('unicode-escape'))

    return tokens

#returns words that are not stop words
def remove_stopwords_common_words(tweet):
    words = tweet.split(' ');
    #print words;
    not_stop_words = []
    stop = [u'i', u'me', u'my', u'myself', u'we', u'our', u'ours', u'ourselves', u'you', u'your', u'yours', u'yourself', u'yourselves', u'he', u'him', u'his', u'himself', u'she', u'her', u'hers', u'herself', u'it', u'its', u'itself', u'they', u'them', u'their', u'theirs', u'themselves', u'what', u'which', u'who', u'whom', u'this', u'that', u'these', u'those', u'am', u'is', u'are', u'was', u'were', u'be', u'been', u'being', u'have', u'has', u'had', u'having', u'do', u'does', u'did', u'doing', u'a', u'an', u'the', u'and', u'but', u'if', u'or', u'because', u'as', u'until', u'while', u'of', u'at', u'by', u'for', u'with', u'about', u'against', u'between', u'into', u'through', u'during', u'before', u'after', u'above', u'below', u'to', u'from', u'up', u'down', u'in', u'out', u'on', u'off', u'over', u'under', u'again', u'further', u'then', u'once', u'here', u'there', u'when', u'where', u'why', u'how', u'all', u'any', u'both', u'each', u'few', u'more', u'most', u'other', u'some', u'such', u'no', u'nor', u'only', u'own', u'same', u'so', u'than', u'too', u'very', u's', u't', u'can', u'will', u'just', u'don', u'should', u'now']
    common = ['im',"i'm"];
    for word in words:
        if word not in stop and word not in common:
            not_stop_words.append(word)
    #print not_stop_words;
    #raw_input();
    return not_stop_words

#read file and split by comma
def ReadFile(filename):
    fp = open(filename, "r")
    data = fp.readlines()
    fp.close()
    rows =[]
    for line in data :
        #print line
        rows.append(line.strip('\n').split(','));
    return rows

#return a tweet devoid of ascci characters
def Remove_non_ascci_characters(tweet):

    tweet_without_aascii = "";
    for c in tweet:
        if ord(c)>0 and ord(c) < 127:
            tweet_without_aascii = tweet_without_aascii + c;

    return tweet_without_aascii;

#remove url in a tweet
def Remove_url_atname_hashtags_from_tweet(tweets):

    tweets_processed = [];
    for i in range(0,len(tweets)):
        tweet = tweets[i];
        words = tweet.split(' ');

    
        processed_tweet="";
        for x in range(0,len(words)):
            if 'http' not in words[x] and '@' not in words[x] and '#' not in words[x]:
                processed_tweet += " "+words[x];

        tweets_processed.append(processed_tweet);
        
    return tweets_processed;


#return tweets from tweet details
def GetTweet(tweet_details):

    tweets = [];
    polarity = [];

    punc = [',','.',':',';','"','!','?','-',"'"];
    for i in range(0,len(tweet_details)):
        detail = tweet_details[i];

        tweet = ''
        for j in range(5,len(detail)):
            tweet = tweet + ' ' + detail[j]
        
        tweet = ''.join(ch for ch in tweet if ch not in punc)
        tweets.append(tweet.lower());
        pol = detail[0];
        pol = ''.join(ch for ch in pol if ch != '"')
        polarity.append(pol);

    return (tweets, polarity);

#return a tweet devoid of ascci characters
def Remove_non_ascci_characters(tweet):

    tweet_without_aascii = "";
    for c in tweet:
        if ord(c)>0 and ord(c) < 127:
            tweet_without_aascii = tweet_without_aascii + c;

    return tweet_without_aascii;

def Create_Dictionary(tweets, polarity):
    pos_words_frequency = {};
    neg_words_frequency = {};

    for x in range (0, len(tweets)):

        #print polarity[x]
        tweet = tweets[x];
        tweet = " ".join(tweet.split())
        tweet = Remove_non_ascci_characters(tweet);
        words = remove_stopwords_common_words(tweet);
        words = stem_tokens(words);

        #print words;
        #raw_input();
        if (len(words) > 0):
            if polarity[x] == '4':
                for i in range(0,len(words)):
                    if words[i] in pos_words_frequency:
                        pos_words_frequency[words[i]] = pos_words_frequency[words[i]] + 1;
                    else:
                        pos_words_frequency[words[i]] = 1;
            else:
                for i in range(0,len(words)):
                    if words[i] in neg_words_frequency:
                        neg_words_frequency[words[i]] = neg_words_frequency[words[i]] + 1;
                    else:
                        neg_words_frequency[words[i]] = 1;

    return (pos_words_frequency, neg_words_frequency);

def WriteDictionaryToFile(filename, dictionary):
    
    f = open(filename, 'ab+');
    pickle.dump(dictionary, f)
    f.close()

tweet_details = ReadFile('Training_data.csv');
print tweet_details[0];

print 'file_read';
tweets, polarity = GetTweet(tweet_details);
print 'tweet_got';
tweets=Remove_url_atname_hashtags_from_tweet(tweets);

pos_words_frequency, neg_words_frequency=Create_Dictionary(tweets, polarity);

sortedValues=sorted(neg_words_frequency.items(), key=lambda x: x[1],reverse=True);

save_obj(pos_words_frequency, 'pos')
save_obj(neg_words_frequency, 'neg')

