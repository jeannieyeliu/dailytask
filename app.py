from flask import Flask, escape, url_for, render_template

app = Flask(__name__)

# fake data
name = 'Jeannie Liu'
tasks = [
    {'id': '1', 'title': '洗衣服', 'estimate': '15分钟', 'state': 'checked'},
    {'id': '2', 'title': '看Flask', 'estimate': '30 分钟', 'state': 'checked'},
    {'id': '3', 'title': '冥想', 'estimate': '30 分钟', 'state': 'checked'},
    {'id': '4', 'title': 'keep运动', 'estimate': '60 分钟', 'state': ''},
    {'id': '5', 'title': 'Ted', 'estimate': '15 分钟', 'state': 'checked'},
    {'id': '6', 'title': '刷LeetCode', 'estimate': '10 分钟', 'state': ''},
    {'id': '7', 'title': '敷面膜', 'estimate': '15 分钟', 'state': ''},
    {'id': '8', 'title': '素描', 'estimate': '30 分钟', 'state': ''},
    {'id': '9', 'title': '看电影《教父3》', 'estimate': '30 分钟', 'state': ''},
    {'id': '0', 'title': '读书《梦的解析》', 'estimate': '30 分钟', 'state': 'checked'}
]


@app.route('/hello')
def hello():
    return '<h1>欢迎来到每日任务与奖励!</h1><img src="http://helloflask.com/totoro.gif">'


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', name=name, tasks=tasks)

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)


@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='jeannie liu'))
    return 'Test page'
