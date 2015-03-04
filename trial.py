from flask import Flask, request, url_for,g
import random
#import MySQLdb
import mysql.connector
import json
from bson import json_util
from bson.json_util import dumps
import newtrial as n

#SQL connection string
sql = mysql.connector.connect(user="shridharmanvi", password="root", host="mysql.server", database="shridharmanvi$tweets")
cur = sql.cursor()

app = Flask(__name__)
app.secret_key = 'This is really unique and secret'


@app.route('/')
def hello_person():
    return 'Hi there!!'


@app.route('/<search_key>')
def show_entries(search_key):
    key=search_key
    y=n.trial(key)

    k_json=[]
    cur = sql.execute('select id, tweet from tweets')
    """
    entries = [dict(id=row[0], tweet=row[1]) for row in cur.fetchall()]

    for doc in entries:
                json_dump = json.dumps(doc, default=json_util.default)
                k_json.append(json_dump)
    """
    return y