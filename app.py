from flask import Flask, request, render_template, jsonify, redirect, url_for, session
import requests, random
from pymongo import MongoClient
import jwt
import datetime

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
      # db.quiz2.update_one({'quiz_num':num},{'$set':{'check':False}})
   
   db.quiz1.update_many({},{'$set':{'check':False}})
   return render_template('index.html')


# @app.route('/quiz2')
# def quiz2():
#    rand = random.randint(1,3)
#    print(rand)
#    num = str(rand)
#    check = db.quiz2.find_one({'quiz_num':num})['check']
#    if check == False:
#       url = db.quiz2.find_one({'quiz_num':num})['url']
#       question = db.quiz2.find_one({'quiz_num':num})['question']
#       question_list = db.quiz2.find_one({'quiz_num':num})['questionList']
#       answer = db.quiz2.find_one({'quiz_num':num})['answer']
#       answer_encode = answer.encode()
#       print(answer)
#       db.quiz2.update_one({'quiz_num':num},{'$set':{'check':True}})
#       return render_template('quiz2.html',question_list=question_list, url=url, question=question, answer=answer_encode)
#    else:
#       return redirect('/quiz2')

@app.route('/quiz1')
def quiz1():
      rand = random.randint(1,3)
      tmp_num = str(rand)
      check = db.quiz1.find_one({'quiz_num':tmp_num})['check']
      if check == False:
         url = db.quiz1.find_one({'quiz_num' : tmp_num})['imgSrc']
         question_list = db.quiz1.find_one({'quiz_num' : tmp_num})['questionList']
         answer = db.quiz1.find_one({'quiz_num':tmp_num})['answer']
         print(question_list)
         db.quiz1.update_one({'quiz_num': tmp_num},{'$set':{'check':True}})
         return render_template('quiz1.html' ,  imgSrc = url, question_list  = question_list, answer= answer )
      else:
         return redirect('/quiz2')

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
   return render_template('score.html')

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