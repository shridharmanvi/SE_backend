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


@app.route('/findout/< key_word >')
def loggedout():
    #data = mongo.db.tweets.find({"one":{ '$regex' : email}})
    data = mongo.db.tweets.find({'keyword':{'$regex':'key_word'}})

    j=[]
    i={"one":1,"two":2}

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

