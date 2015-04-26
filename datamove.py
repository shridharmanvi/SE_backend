from pymongo import MongoClient
import re

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['se']
collection = db.tweets
key= 'ted cruz'
data = collection.find()

shortword = re.compile(r'\W*\b\w{1,3}\b')
#newstr = g.replace("ted", "")
#newstr1= newstr.replace("cruz", "")

f= open('data_tweets.csv','a')


for line in data:
    row1= line['tweet']
    row2= line['keyword']
    row3= line['date']
    #wr= row1 + ',' + row2 + '\n'

    g=shortword.sub('', row1)
    wr = g + ',' + row2 + ',' + row3 + '\n'

    #newstr = g.replace("ted", "")
    #newstr1= newstr.replace("cruz", "")
    #print newstr1
    f.write(wr)
    wr=''

f.close()

    

