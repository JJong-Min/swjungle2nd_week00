from flask import Flask, render_template
import requests
from pymongo import MongoClient
app = Flask(__name__)



@app.route('/')
def home():
   return render_template('layout.html')

@app.route('/quiz1')
def post():
   return render_template('layout.html', imgSrc='https://www.google.com/search?q=%ED%94%BC%EC%B9%B4%EC%B8%84+%EC%8B%A4%EB%A3%A8%EC%97%A3&tbm=isch&source=iu&ictx=1&fir=cOJ-BrW3Sx7xTM%252CUZhKQIetJNS5oM%252C_&vet=1&usg=AI4_-kQ9jNPHNiw7p7yGQh2BteAEot5c3Q&sa=X&ved=2ahUKEwiusrTI3pTyAhWJEogKHcL8DdoQ9QF6BAgNEAE#imgrc=cOJ-BrW3Sx7xTM' , questionList = ['피츄', '피피츄', '핖핖카', '피카츄'])

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)