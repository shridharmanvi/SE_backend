# this program reads data from tweets.csv and loads it to mongodb

from flask import Flask, jsonify,request, render_template, redirect, url_for, session
from flask_pymongo import PyMongo
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
from werkzeug import secure_filename
from random import randint
import os
from flask import make_response
from bson.json_util import dumps

app.secret_key = 'dfgsdfgsfgdfsg'
app.config['MONGO_HOST'] = '0.0.0.0'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'se'
app.config['MONGO_USERNAME'] = ''
app.config['MONGO_PASSWORD'] = ''

mongo = PyMongo(app)




def replace_value_with_definition(dictionary,key_to_find, definition):
    for key in dictionary.keys():
        if key == key_to_find:
            dictionary[key] = definition



def dataload():
    t=open('tweets.csv','rw')

    tweets={}

    for row in t.readlines():
        row= row.split(',')
        #row[0]=int(row[0])
        #jobs[int(row[0])]=rowi
        tweet_id=row[0]
        date=row[1]
        tweet=row[2]
        keyword=row[3]
        x={'tweet_id':tweet_id,'date':date,'tweet':tweet,'keyword':keyword}
        print x
        break
           


dataload()
#print len(jobs.keys())i    


