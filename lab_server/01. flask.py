from flask import Flask
app = Flask(__name__)


@app.route('/')
def f1():
    return '시작 페이지'


@app.route('/a')
def f2():
    return 'a'


app.run()
