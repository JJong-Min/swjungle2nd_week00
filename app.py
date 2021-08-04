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
      db.quiz2.update_one({'quiz_num':num},{'$set':{'check':False}})
   return render_template('layout.html')

@app.route('/quiz2')
def quiz2():
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

@app.route('/score')
def score():
   return render_template('score.html')

if __name__ == '__main__':
   
   app.run('0.0.0.0',port=5000,debug=True)