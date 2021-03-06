from __future__ import division
from flask import Flask, jsonify,request, render_template, redirect, url_for, session
from flask_pymongo import PyMongo
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
from werkzeug import secure_filename
from random import randint
#from flaskext.uploads import delete, init, save, Upload
#from flask.uploads import UploadSet, IMAGES
import os
#from pytagcloud import create_tag_image, make_tags,LAYOUT_MOST_HORIZONTAL
#from pytagcloud.lang.counter import get_tag_counts


from flask import make_response

from bson.json_util import dumps


app=Flask(__name__)

app.secret_key = 'dfgsdfgsfgdfsg'
app.config['MONGO_HOST'] = '0.0.0.0'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'se'
#app.config['MONGO_USERNAME'] = ''
#app.config['MONGO_PASSWORD'] = ''
mongo = PyMongo(app)


def replace_value_with_definition(dictionary,key_to_find, definition):
    for key in dictionary.keys():
        if key == key_to_find:
            dictionary[key] = definition


#The below function cleanses and loads the data from tweets.csv and loads in into mongodb tweets collection 
# Call only in case manual data load from csv is required
def dataload():
    t=open('tweets.csv','rw')

    tweets={}

    for row in t.readlines():
        row= row.split(',')
        #row[0]=int(row[0])
        #jobs[int(row[0])]=rowi
        tweet_id=int(row[0])
        date=row[1]
        tweet=row[2]
        keyword=row[3]
        tweet=tweet.rstrip()
        keyword=keyword.rstrip()
        #print tweet_id #date tweet keyword
        x={'tweet_id':tweet_id,'date':date,'tweet':tweet,'keyword':keyword}
        mongo.db.tweets.insert(x)     

@app.route('/')
def route():
    return 'Hey'


@app.route('/findout/<key_word>')
def loggedout(key_word):
    #data = mongo.db.tweets.find({"one":{ '$regex' : email}}
    var= key_word.lower()
    #print var
    data = mongo.db.tweets.find({'keyword':{'$regex':var}})
    cnt= data.count()
    #d.wordcloud_build(var)
    if (cnt >0):
        j=[]
        i={"one":1,"two":2}
        pos=0
        neg=0
        neu=0
        final=[]
        word_cloud=[]
        for k in data:
            if (k['keyword']==key_word):
                if k['polarity']>0:
                    pos= pos+1
                elif k['polarity']<0:
                    neg=neg+1
                else:
                    neu=neu+1
                word_cloud.append(k['tweet'])

       
        p=100*((pos)/cnt)
        n=100*(neg/cnt)
        x={'pos':p,'neg':n}
        j.append(x)

        o= mongo.db.tweets.find({ "$and": [ {'keyword':{'$regex':var}}, {'date':{"$regex":"2015-03-28"}} ,{'polarity':{"$gt":0}}] })
        q= mongo.db.tweets.find({ "$and": [ {'keyword':{'$regex':var}}, {'date':{"$regex":"2015-03-28"}}] })
        r= mongo.db.tweets.find({ "$and": [ {'keyword':{'$regex':var}}, {'date':{"$regex":"2015-03-29"}} ,{'polarity':{"$gt":0}}] })
        s= mongo.db.tweets.find({ "$and": [ {'keyword':{'$regex':var}}, {'date':{"$regex":"2015-03-29"}}] })
        t= mongo.db.tweets.find({ "$and": [ {'keyword':{'$regex':var}}, {'date':{"$regex":"2015-03-30"}} ,{'polarity':{"$gt":0}}] })
        u= mongo.db.tweets.find({ "$and": [ {'keyword':{'$regex':var}}, {'date':{"$regex":"2015-03-30"}}] })
        v= mongo.db.tweets.find({ "$and": [ {'keyword':{'$regex':var}}, {'date':{"$regex":"2015-04-20"}} ,{'polarity':{"$gt":0}}] })
        w= mongo.db.tweets.find({ "$and": [ {'keyword':{'$regex':var}}, {'date':{"$regex":"2015-04-20"}}] })
        an= mongo.db.tweets.find({ "$and": [ {'keyword':{'$regex':var}}, {'date':{"$regex":"2015-04-19"}} ,{'polarity':{"$gt":0}}] })
        bn= mongo.db.tweets.find({ "$and": [ {'keyword':{'$regex':var}}, {'date':{"$regex":"2015-04-19"}}] })

        
        try:
            res1= (100*((o.count())/(q.count())))
        except ZeroDivisionError:
            res1=30
        
        try:
            res2= (100*((r.count())/(s.count())))
        except ZeroDivisionError:
            res2=res1

        try:
            res3= (100*((t.count())/(u.count())))
        except ZeroDivisionError:
            res3=res2
        
        try:
            res4= (100*((v.count())/(w.count())))
        except ZeroDivisionError:
            res4=res3

        try:
            res5= (100*((an.count())/(bn.count())))
        except ZeroDivisionError:
            res5=res4 


        #one={'1':(100*((o.count())/(q.count()))),'2':(100*((r.count())/(s.count()))),'3':(100*((t.count())/(u.count()))),'4':(100*((v.count())/(w.count()))),'5':(100*((an.count())/(bn.count())))}
        
        one= {'1':res1,'2':res2,'3':res3,'4':res4,'5':res5} 
        
#two={'2':(100*((r.count())/(s.count())))}
        #three={'3':(100*((t.count())/(u.count())))}
        j.append(one)
        #image_link='/home/ubuntu/se/word_cloud.png'
        im='https://s3.amazonaws.com/manvi123/'
        im_name= var.replace(" ", "")
        image_link=im + im_name + '.png'
        image={'img_link':image_link}
        j.append(image)
        ret=json.dumps(j)
        return ret

    else:
        return 'Please enter a valid candidate for 2016 Presidential Elections' 
    
    

    #for x in data:
    #    replace_value_with_definition(i,'one',x['one'])
     #   replace_value_with_definition(i,'two',x['two'])
      #  j.append(i)
       # i={"one":1,"two":2}
        #print j
     
    k=json.dumps(j)
    return k




if __name__== '__main__':
    app.run(host='0.0.0.0', port=80,debug='true')

