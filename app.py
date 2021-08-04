
from flask import Flask, request, render_template, jsonify, redirect, url_for, session
import requests, random

from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.week0


@app.route('/')
def home():
   for x in range(3):
      num = str(x+1)
   #   db.quiz2.update_one({'quiz_num':num},{'$set':{'check':False}})
   return render_template('layout.html')

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

@app.route('/quiz1')
def quiz1():
   rand = random.randint(1,3)
   tmp_num = str(rand)
   check = db.quiz1.find_one({'quiz_num': tmp_num})['check']
   if check == False:
      url = db.quiz1.find_one({'quiz_num' : tmp_num})['imgSrc']
      question_list = db.quiz1.find_one({'quiz_num' : tmp_num})['questionList']
      answer = db.quiz1.find_one({'quiz_num':tmp_num})['answer']
      db.quiz1.update_one({'quiz_num' : tmp_num}, {'$set' : {'check': True }}) 
      return render_template('quiz1.html' , imgSrc = url, quesitons_list  = question_list, answer= answer )
   else:

      return redirect('/quiz1')

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

# @app.route('/api/list', methods=['GET'])
# def show_stars():
#     # 1. db에서 mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
#     # 참고) find({},{'_id':False}), sort()를 활용하면 굿!
#     stars = list(db.mystar.find({}, {'_id': False}).sort('like', -1))
#     # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
#     return jsonify({'result': 'success', 'stars_list': stars})





@app.route('/login')
def login():
   return render_template('login.html')



@app.route('/join')
def join():
   return render_template('join.html')

if __name__ == '__main__':
   
   app.run('0.0.0.0',port=5000,debug=True)