from nltk.stem import PorterStemmer
from textblob import TextBlob

stop=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
      'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her',
      'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
      'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was',
      'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
      'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
      'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
      'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
      'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
      'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
      'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
      'should', 'now']

stemmer = PorterStemmer()

def trial(y):
    x= y + ' .... Work in progress'
    return x

def read_data():
    tweets_f=open('tweets.csv','rw')

    tweets={}

    for row in tweets_f.readlines():
        row= row.split(',')
        try:
            row[0]=int(row[0])
            y=row[2]
            g= ' '.join([word for word in y.split() if word not in stop])
            row.append(g)
            tweets[int(row[0])]=row

        except ValueError:
            x=1

    sent='I would anyday prefer iphone to S3 because it is  not better than that'
    blob = TextBlob(sent)

    for sentence in blob.sentences:
        print(sentence.sentiment.polarity)

read_data()
