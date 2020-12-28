from flask import Flask, escape, url_for, render_template

app = Flask(__name__)

# fake data
name = 'Jeannie Liu'
tasks = [
    {'id': '1', 'title': 'My Neighbor Totoro', 'estimate': '1988', 'state': 'checked'},
    {'id': '2', 'title': 'Dead Poets Society', 'estimate': '1989', 'state': 'checked'},
    {'id': '3', 'title': 'A Perfect World', 'estimate': '1993', 'state': 'checked'},
    {'id': '4', 'title': 'Leon', 'estimate': '1994', 'state': ''},
    {'id': '5', 'title': 'Mahjong', 'estimate': '1996', 'state': 'checked'},
    {'id': '6', 'title': 'Swallowtail Butterfly', 'estimate': '1996', 'state': ''},
    {'id': '7', 'title': 'King of Comedy', 'estimate': '1999', 'state': ''},
    {'id': '8', 'title': 'Devils on the Doorstep', 'estimate': '1999', 'state': ''},
    {'id': '9', 'title': 'WALL-E', 'estimate': '2008', 'state': ''},
    {'id': '0', 'title': 'The Pork of Music', 'estimate': '2012', 'state': 'checked'}
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
