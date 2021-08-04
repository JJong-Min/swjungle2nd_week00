from flask import Flask, json, request, render_template, jsonify, redirect, url_for, session
import requests, random
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
import jwt
import datetime
from functools import wraps

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
   return render_template('index.html')


@app.route('/quiz2')
def quiz2():
   # test1 = {'quiz_num':1, 'question':'골드 버전에서 처음 고를 수 있는 포켓몬이 아닌 것은?', 'name': '브케인', 'url':'https://mblogthumb-phinf.pstatic.net/MjAyMDAxMTZfMTg4/MDAxNTc5MTA3ODQxOTg4.D9UzB7yzFnanFcm4w6tJRW5KFTcKLdf3NU5UKuiN2uwg.0vG-b0J0odK-8oOK6M5S7Et_kvTqI-Y2JVPDHp_88GEg.PNG.sanyo1122/pm0155_00_hinoarashi_256.ktx_.png?type=w800'}
   # test2 = {'quiz_num':1, 'question':'골드 버전에서 처음 고를 수 있는 포켓몬이 아닌 것은?', 'name': '치코리타', 'url':'https://e7.pngegg.com/pngimages/666/1023/png-clipart-pokemon-pikachu-chikorita-fan-fiction-chikorita-pokemon-go-comics-mammal.png'}
   # test3 = {'quiz_num':1, 'question':'골드 버전에서 처음 고를 수 있는 포켓몬이 아닌 것은?', 'name': '피카츄', 'url':'https://w7.pngwing.com/pngs/244/439/png-transparent-pikachu-drawing-anime-pokemon-pikachu-leaf-cartoon-flower.png'}
   # test4 = {'quiz_num':1, 'question':'골드 버전에서 처음 고를 수 있는 포켓몬이 아닌 것은?', 'name': '리아코', 'url':'https://images.gameinfo.io/pokemon/256/158-00.png'}
   rand = random.randint(1,3)
   print(rand)
   num = str(rand)
   check = db.quiz2.find_one({'quiz_num':num})['check']
   if check == False:
      url = db.quiz2.find_one({'quiz_num':num})['url']
      question = db.quiz2.find_one({'quiz_num':num})['question']
      question_list = db.quiz2.find_one({'quiz_num':num})['questionList']
      answer = db.quiz2.find_one({'quiz_num':num})['answer']
      db.quiz2.update_one({'quiz_num':num},{'$set':{'check':True}})
      return render_template('quiz2.html',question_list=question_list, url=url, question=question)
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
      
      
if __name__ == '__main__':
   
   app.run('0.0.0.0',port=5000,debug=True)