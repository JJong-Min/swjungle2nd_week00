from array import array
from flask import Flask, request, render_template, jsonify, redirect, url_for, session
import requests, random
from pymongo import MongoClient
import jwt
import datetime
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = "OOO"

client = MongoClient('localhost', 27017)
db = client.week0



@app.route('/')
def home():
   if 'loged_in' in session:
      print(session['logged_in'])
   else:
      print('a')
   for x in range(3):
      num = str(x+1)
      db.quiz2.update_one({'quiz_num':num},{'$set':{'check':False}})
   session['score_check'] = 0
   session['array_check'] = []
   x = np.arange(4)
   x = np.delete(x,0)
   x = np.random.permutation(x)
   for i in x:
      session['array_check'].append(int(i))
   return render_template('index.html')


@app.route('/quiz2', methods=['GET', 'POST'])
def quiz2():
   if request.method == 'POST':
      session['score_check'] += 20
      print(session['score_check'])
      return jsonify({'msg':'점수공개'})
   already_question_num = request.args.get('q_num')
   already_check_num = request.args.get('check')
   count = int(request.args.get('count'))
   print(count)
   check_answer = db.quiz2.find_one({'quiz_num':already_question_num})['answer']
   if check_answer == already_check_num:
      session['score_check'] += 20
      print(session['score_check'])
   #print(type(already_question_num),already_check_num)
   rand = session['array_check'][count]
   num = str(rand)
   check = db.quiz2.find_one({'quiz_num':num})['check']

   url = db.quiz2.find_one({'quiz_num':num})['url']
   question = db.quiz2.find_one({'quiz_num':num})['question']
   question_list = db.quiz2.find_one({'quiz_num':num})['questionList']
   answer = db.quiz2.find_one({'quiz_num':num})['answer']
   return render_template('quiz2.html',question_list=question_list, score=session['score_check'],url=url, question=question, num_check=num, count=count)
   

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

@app.route('/score')
def score():
   return render_template('score.html',score=session['score_check'])

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
         session['logged_in'] = True
         return jsonify({"result": "success", 'access_token': jwt.encode(access_payload, app.config['SECRET_KEY'], algorithm="HS256"), 'refresh_token': jwt.encode(refresh_payload, app.config['SECRET_KEY'], algorithm="HS256")})
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