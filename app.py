from array import array
from flask import Flask, json, request, render_template, jsonify, redirect, url_for, session
import requests, random
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import jwt
import datetime
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'IOJPI241JPI'
bcrypt = Bcrypt(app)
client = MongoClient('localhost', 27017)
db = client.week0


@app.route('/')
def home():
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
      if bcrypt.check_password_hash(user_info['userPW'], user_pw):
         access_payload = {"id": user_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=3)}
         session['logged_in'] = True
         return jsonify({"result": "success", 'access_token': jwt.encode(access_payload, app.config['SECRET_KEY'], algorithm="HS256")})

      else:
         return jsonify({"result": "fail"})
   except:
      return jsonify({"result": "fail"})

@app.route('/logout')
def logout():
    session['logged_in'] = False
    print(session['logged_in'])
    return redirect('/')

@app.route('/join', methods=['GET'])
def join():
   return render_template('join.html')



@app.route('/join_pro', methods=['POST'])
def join_pro():
   user_id = request.form['ID_give']
   user_pw = request.form['PW_give']
   pw_hash = bcrypt.generate_password_hash(user_pw)
   user_email = request.form['Email_give']
   user_name = request.form['Name_give']
   try:
      db.user_info.insert_one({'userID':user_id, 'userPW': pw_hash, 'userEmail': user_email, 'userName': user_name})
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

@app.route('/modification', methods=['POST'])
def modification():
   user_token = request.form['token_give']
   if not user_token:
      return jsonify({'result': 'fail'})
   try:
      decoded = jwt.decode(user_token, app.config['SECRET_KEY'], algorithms=["HS256"])
      existing_user_infos = db.user_info.find_one({'userID':decoded['id']}, {'_id':False})
      user_name = existing_user_infos['userName']
      user_id = existing_user_infos['userID']
      user_email = existing_user_infos['userEmail']
      return jsonify({'result':'success', 'user_id':user_id, 'user_name': user_name, 'user_email': user_email})
   except jwt.ExpiredSignatureError:
      session['logged_in'] = False
      return jsonify({'result':'fail'})

@app.route('/modication_form')
def modification_form():
   return render_template('modification.html')

@app.route('/modification_complete', methods=['POST'])
def modification_complete():
   oridinal_id = request.form['Oridinal_id']
   user_id = request.form['ID_give']
   user_pw = request.form['PW_give']
   pw_hash = bcrypt.generate_password_hash(user_pw)
   user_email = request.form['Email_give']
   user_name = request.form['Name_give']
   try:
      db.user_info.update_one({'userID':oridinal_id}, {'$set':{'userPW':pw_hash, 'userEmail': user_email, 'userName': user_name, 'userID':user_id}})
      session['logged_in'] = False
      return jsonify({"result": "success"})
   except:
      return jsonify({'result':'fail'})


if __name__ == '__main__':
   
   app.run('0.0.0.0',port=5000,debug=True)