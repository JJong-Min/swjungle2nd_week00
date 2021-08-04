from logging import DEBUG
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import requests
from pymongo import MongoClient
import jwt
import datetime

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.week0
key = "secret"

@app.route('/', methods=['GET'])
def home():
   return render_template('index.html')

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

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/login_pro', methods=['POST'])
def login_pro():
   user_id = request.form['ID_give']
   user_pw = request.form['PW_give']
   user_info = db.user_info.find_one({'userID':user_id})
   try:
      if user_info['userPW'] == user_pw:
         access_payload = {"id": user_id, "password": user_pw, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}
         refresh_payload = {"id": user_id, "password": user_pw, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)}
         return jsonify({"result": "success", 'access_token': jwt.encode(access_payload, key, algorithm="HS256"), 'refresh_token': jwt.encode(refresh_payload, key, algorithm="HS256")})
      else:
         return jsonify(result = "fail")
   except:
      return jsonify(result = "fail")

@app.route('/join')
def join():
   return render_template('join.html')



@app.route('/join_pro', methods=['POST'])
def join_pro():
   user_id = request.form['ID_give']
   user_pw = request.form['PW_give']
   user_email = request.form['Email_give']
   user_name = request.form['Name_give']
   try:
      db.user_info.insert_one({'userID':user_id, 'userPW': user_pw, 'userEmail': user_email, 'userName': user_name})
      return jsonify({"result": "success"})
   except:
      return jsonify({'result':'fail'})


@app.route('/id_overlapping_confirm', methods=['POST'])
def id_overlapping_confirm():
   user_id = request.form['ID_give']
   candidate_id = db.user_info.find_one({'userID':user_id})
   print(user_id, candidate_id)
   if candidate_id is None:
      return jsonify({"result": "success"})
   else:
      return jsonify({"result": "fail"})


@app.route('/welcome')
def welcome():
   return render_template('welcome.html')


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)