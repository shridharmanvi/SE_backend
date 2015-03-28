# this program reads data from tweets.csv and loads it to mongodb

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



def dataload():
    job=open('tweets.csv','rw')

    jobs={}

    for row in job.readlines():
        row= row.split(',')
        try:
            row[0]=int(row[0])
            jobs[int(row[0])]=row
        except ValueError:
            x=1

#print len(jobs.keys())i    


