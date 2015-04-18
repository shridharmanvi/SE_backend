from pymongo import MongoClient
import re

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['se']


collection = db.tweets
key='hillary clinton'
data = collection.find({'keyword':{'$regex':key}})

name_remove=re.compile(r'hillary')

g=0
k=''
for i in data:
    tweet = i['tweet']
    k= k + tweet
    newstr = k.replace("hillary", "")
    newstr1 = newstr.replace("clinton", "")
    print newstr1
    g +=1
    if (g==3):
        exit()


#String regex = "\\s*\\bis\\b\\s*";
#content = content.replaceAll(regex, "");
