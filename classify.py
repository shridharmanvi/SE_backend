import pickle
from nltk.stem import *
from nltk.stem.porter import *
from nltk.corpus import stopwords
import string
import pickle
import re

#the source to the trained data
#https://s3.amazonaws.com/manvi123/pos.pkl
#https://s3.amazonaws.com/manvi123/neg.pkl

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
DeterminePolarity(posDict, negDict, 'this does not make sense');

#print stemmed_tokens
#print GetPolarity(stemmed_tokens, posDict, negDict)
