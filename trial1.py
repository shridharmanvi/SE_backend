from pytagcloud import create_tag_image, make_tags, LAYOUT_MOST_HORIZONTAL
from pytagcloud.lang.counter import get_tag_counts

from pymongo import MongoClient
import re
from boto.s3.key import Key
from boto.s3.connection import S3Connection

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['se']
collection = db.tweets
key= 'ted cruz'
data = collection.find({'keyword':{'$regex':key}})
   
k=''  
num=0
for i in data:
    tweet = i['tweet']
    k= k + tweet  
    num +=1
    if(num==1000):
        break

shortword = re.compile(r'\W*\b\w{1,3}\b')
g=shortword.sub('', k)
newstr = g.replace("ted", "")
newstr1= newstr.replace("cruz", "")

def wordcloud_build():
    max_tags = 60
    tags = make_tags(get_tag_counts(newstr1)[:max_tags], minsize=1,  maxsize=60)
    size = (500, 500)

    create_tag_image(tags, 'tedcruz.png', size=(1024, 800), background=(0,0,0,255) ,layout=LAYOUT_MOST_HORIZONTAL,fontname='Lobster')


def loads3():
    AWS_ACCESS_KEY_ID='AKIAI5R6WVIRAZWYOEIA'
    AWS_SECRET_ACCESS_KEY='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'
    con=S3Connection(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
    bucket_name=con.create_bucket('manvi123')
    k= Key(bucket_name)
    k.key= 'tedcruz.png'
    k.set_contents_from_filename('tedcruz.png',policy='public-read') 
    con.close()
    
   

wordcloud_build()
loads3()
