from flask import Flask, request, url_for,g
import random
from flask.ext.sqlalchemy import SQLAlchemy
import mysql.connector
import json
from bson import json_util
from bson.json_util import dumps
import newtrial as n


app = Flask(__name__)
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://shridharmanvi:hireyaru@mysql.server/db'
db = SQLAlchemy(app)
"""

app.secret_key = 'This is really unique and secret'

@app.route('/')
def hello_person():
    return 'Hi there!!'


@app.route('/<search_key>')
def show_entries(search_key):
    key=search_key
    y=n.trial(key)
    return y