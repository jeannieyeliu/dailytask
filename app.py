from flask import Flask, escape, url_for, render_template, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
import os, click, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev'
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


@app.route('/', methods=['GET', 'POST'])
# @app.route('/index')
def index():
    if request.method == 'POST':
        title = request.form.get('title');
        estimate = request.form.get('estimate');
        tag = request.form.get('tag');
        date = datetime.date.today()
        if not title or not estimate:
            flash('输入有误')
            return redirect(url_for('index'))
        task = Task(title=title, estimate=estimate, state='', tag=tag,
                    date=date)
        db.session.add(task)
        db.session.commit()
        flash('任务添加成功！')
        return redirect(url_for('index'))
    tasks = Task.query.all()
    return render_template('index.html', name=name, tasks=tasks)


@app.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        estimate = request.form['estimate']
        tag = request.form['tag']

        if not title or not estimate:
            flash('输入有误.')
            return redirect(url_for('edit', task_id=task_id))  # 重定向回对应的编辑页面

        task.title = title  # 更新标题
        task.estimate = estimate
        task.tag = tag
        task.date = datetime.date.today()
        db.session.commit()  # 提交数据库会话
        flash('修改成功！.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', task=task)  # 传入被编辑的电影记录


@app.route('/task/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    title = task.title
    db.session.delete(task)
    db.session.commit()
    flash("成功删除任务'" + title + "'.")
    return redirect(url_for('index'))


@app.route('/task/done/<task_id>/<state>', methods=['POST', 'GET'])
def done(task_id, state):
    task = Task.query.get_or_404(int(task_id))
    task.state = "checked" if state == "true" else "";
    db.session.commit()
    return redirect(url_for('index'))


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

