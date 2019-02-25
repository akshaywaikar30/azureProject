# <h3>Name: Akshay Waikar</h3>
# <h3>ID: 1001373973</h3>
import os
from flask import Flask,redirect,render_template,request
import pypyodbc
import time
import random
import urllib
import datetime
import json
import redis
import pickle
import hashlib

app = Flask(__name__)


server = 'tcp:akshayserver.database.windows.net'
database = 'sqlDB'
username = 'akshay305@akshayserver'
password = 'Welcome@1234'
trust='no'
driver= '{ODBC Driver 13 for SQL Server}'
R_SERVER = redis.Redis(host='redisakshay.redis.cache.windows.net',
        port=6379, db=0, password='dKIcSrBGZa/7ailAOrva/9aSpvqBrGO9HfFbWnwpS5U=')
   
def disdata():
   cnxn = pypyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password +';TrustServerCertificate'+trust )
   cursor = cnxn.cursor()
   start = time.time()
   cursor.execute("SELECT TOP 10000 * FROM quakes")
   row = cursor.fetchall()
   end = time.time()
   executiontime = end - start
   return render_template('list.html', ci=row, t=executiontime)

def earthmagnitude(magfrom=None,magto=None,noq=None):
    dbconn = pypyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()
    start = time.time()
    for i in range(0,int(noq)):
    	mag= round(random.uniform(magfrom, magto),2)
    	success="SELECT * from quakes where mag>'"+str(mag)+"'"
    	sql="select * from quakes where mag>'"+str(mag)+"'"
    	hash = hashlib.sha224(sql.encode('utf-8')).hexdigest()
    	key = "sql_cache:" + hash
    	if (R_SERVER.get(key)):
    		print ("cached")
    	else:
    		cursor.execute(sql)
    		data = cursor.fetchall()
    		akshayarr=[]
    		for k in data:
    			akshayarr.append(str(k))
    		R_SERVER.set(key, pickle.dumps(akshayarr))
    		R_SERVER.expire(key, 36);
    	cursor.execute(success)
    end = time.time()
    xtime = end - start
    return render_template('result.html', x=xtime)



@app.route('/')
def hello_world():
  return render_template('index.html')

@app.route('/dispdata', methods=['POST'])
def display():
    return disdata() 

@app.route('/getdata', methods=['GET'])
def magnitudeofearth():
    magfrom = float(request.args.get('magfrom'))
    magto = float(request.args.get('magto'))
    noq = request.args.get('noq')
    return earthmagnitude(magfrom,magto,noq) 	

if __name__ == '__main__':
  app.run()
