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

# @app.route('/api/list', methods=['GET'])
# def show_stars():
#     # 1. db에서 mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
#     # 참고) find({},{'_id':False}), sort()를 활용하면 굿!
#     stars = list(db.mystar.find({}, {'_id': False}).sort('like', -1))
#     # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
#     return jsonify({'result': 'success', 'stars_list': stars})




@app.route('/quiz1')
def quiz1():
   return render_template('quiz1.html', imgSrc = 'http://img2.tmon.kr/cdn3/deals/2019/05/10/2025175798/review_7eec8_97vkj.jpg'
   , questionList = ['피츄', '피피츄', '핖핖카', '피카츄'] , answer ='피카츄', num = 'null')



if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)