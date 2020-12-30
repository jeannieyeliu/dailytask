from flask import Flask, escape, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import os, click, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app)


class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Task(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 任务标题
    estimate = db.Column(db.Integer)  # 分钟（时间）
    state = db.Column(db.String(60))  # 状态，checked or
    tag = db.Column(db.String(60))
    date = db.Column(db.DateTime)


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')  #
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
        click.echo('Old Database dropped.')
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
    name = "Jack Liu"
    tasks = [{'id': '1', 'title': '洗衣服', 'estimate': 10, 'state': 'checked', 'tag': '家务'},
             {'id': '2', 'title': '看Flask', 'estimate': 10, 'state': 'checked', 'tag': '技术'},
             {'id': '3', 'title': '冥想', 'estimate': 10, 'state': 'checked', 'tag': '运动'},
             {'id': '4', 'title': 'keep运动', 'estimate': 10, 'state': '', 'tag': '运动'},
             {'id': '5', 'title': 'Ted', 'estimate': 10, 'state': 'checked', 'tag': '看的'},
             {'id': '6', 'title': '刷LeetCode', 'estimate': 10, 'state': '', 'tag': '技术'},
             {'id': '7', 'title': '敷面膜', 'estimate': 10, 'state': '', 'tag': '护理'},
             {'id': '8', 'title': '素描', 'estimate': 10, 'state': '', 'tag': '爱好'},
             {'id': '9', 'title': '看电影《教父3》', 'estimate': 10, 'state': '', 'tag': '看的'},
             {'id': '0', 'title': '读书《梦的解析》', 'estimate': 10, 'state': 'checked', 'tag': '看的'}]

    user = User(name=name)
    db.session.add(user)
    for m in tasks:
        task = Task(title=m['title'], estimate=m['estimate'], state=m['state'], tag=m['tag'] or '',
                    date=datetime.date.today())
        db.session.add(task)

    db.session.commit()
    click.echo('Done.')


# fake data
user = User.query.first()
name = "Jack Liu" if not user else user.name;
tasks = Task.query.all()
"""[
    {'id': '1', 'title': '洗衣服', 'estimate': 10, 'state': 'checked', 'tag': '家务'},
    {'id': '2', 'title': '看Flask', 'estimate': 10, 'state': 'checked'},
    {'id': '3', 'title': '冥想', 'estimate': 10, 'state': 'checked'},
    {'id': '4', 'title': 'keep运动', 'estimate': 10, 'state': ''},
    {'id': '5', 'title': 'Ted', 'estimate': 10, 'state': 'checked'},
    {'id': '6', 'title': '刷LeetCode', 'estimate': 10, 'state': ''},
    {'id': '7', 'title': '敷面膜', 'estimate': 10, 'state': ''},
    {'id': '8', 'title': '素描', 'estimate': 10, 'state': ''},
    {'id': '9', 'title': '看电影《教父3》', 'estimate': 10, 'state': ''},
    {'id': '0', 'title': '读书《梦的解析》', 'estimate': 10, 'state': 'checked'}
]"""


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


@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    return render_template('404.html'), 404


@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)
