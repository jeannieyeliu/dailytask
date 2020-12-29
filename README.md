# dailytask
Daily task is a website that I can use to manage my everyday task

# environment config 环境配置
(mac only at the momentpy)

* 打开~/.bashrc文件，并添加如下：
~~~shell script
# 如果出错就加上以下两行
export VIRTUALENVWRAPPER_PYTHON=`which python3` 
export VIRTUALENVWRAPPER_VIRTUALENV=`which virtualenv` 

export WORKON_HOME=$HOME/.virtualenv  # 导入虚拟环境保存的目录
source $HOME/Library/Python/3.8/bin/virtualenvwrapper.sh  # 添加命令的路径
~~~

在命令行执行：
~~~shell script
# 1. install pip3
curl https://bootstrap.pypa.io/get-pip.py | python3
python3 get-pip.py 
pip3 install --upgrade pip

# 2. build virtual environment
pip install virtualenv
pip install virtualenvwrapper

# 3. ~/.bashrc配置文件声效
mkdir $HOME/.virtualenv
source ~/.bashrc  # 让命令生效

# 4.创建并使用虚拟环境
mkvirtualenv dailytask
workon dailytask

# 5. 安装包
pip3 install -r requirements.txt 
~~~

## 开发相关环境变量

~~~shell script
# 开启调试模式，这样浏览器上会显示错误信息
export FLASK_ENV=development
touch .env .flaskenv
~~~

# 创建数据库
~~~shell script
flask shell
>>> from app import db
>>> db.create_all()
~~~

## 启动
~~~shell script
set FLASK_APP=hello.py
flask run
~~~


# 部署

