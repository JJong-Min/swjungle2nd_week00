from flask import Flask, request, render_template, jsonify, redirect, url_for, session
import requests
from pymongo import MongoClient
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.week0

@app.route('/')
def home():
   return render_template('layout.html')

@app.route('/rank')
def rank():
   return render_template('ranking.html')

@app.route('/rank_list')
def rank_list():
   page = int(request.args.get('num'))
   result = []
   #rank_list = list(db.rank.find({'quiz':page},{'_id':False})).sort({'score':1})
   for rank_list in db.rank.find({'quiz':page}).sort('score',-1):
      rank_list['_id'] = str(rank_list['_id']) 
      result.append(rank_list)
   return jsonify({'rank':result})



if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)