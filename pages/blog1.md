title: Flask 文档笔记(1) flaskr
date: 2015-08-13 15:48:53
tags: Flask web
---
**flaskr**<br/>
flaskr 是flask文档中的一个实例，是一个微型blog。我觉得flaskr很是特别，因为它几乎都是原生的flask操作，
没有用到太多的扩展。通过它，我们可以了解一个纯正的flask。<br/>

**1.文件目录的构造**<br/>
flaskr是一个比较简单的flask应用，所以它的文件结构就是项目文件夹下app文件＋templates/＋static/<br/>

**2.配置加载**<br/>
flaskr的配置不多，所以将配置和app实例放在了一个文件中(flask配置名大写):
/flaskr/flaskr.py

    from flask import Flask

    DATABASE = '/tmp/flaskr.db'
    DEBUG = True
    SECRET_KEY = 'development key'
    USERNAME = 'admin'
    PASSWORD = 'default'

    app = Flask(__name__)
    app.config.from_object(__name__)

这里app实例调用了from_object()方法加载配置<br/>
flask加载配置有三种方式: from_object(), from_pyfile(), from_envvar()。from_object()会自动搜寻并加载字符串配置以及名称
为大写的配置变量;此外,也可以把配置类或者配置字典作为from_object()的参数。但是如果想直接加载配置文件，则
需使用 from_pyfile()。对于一些特定配置比如管理员密码、密钥，这些是不希望别人看到的，这些配置可以设置为环境变量，
使用from_envvar()加载。<br/>

**3.数据库**<br/>
对于sql数据库，我一般都采用flask-sqlalchemy扩展处理，这个扩展使开发者无需编写底层的sql语句而是采用类的形式处理数据
库：每一个表都是一个类，而表中的每一个实际对象都是类实例。数据库的创建、迁移以及teardown使用flask-migrate扩展即可
实现。但是flaskr则没有使用扩展，而是完全依据原生的flask与sql。<br/>

3.1: 创建数据库表:<br/>
flaskr/schema.sql

    drop table if exists entries;
    create table entries (
        id integer primary key autoincrement,
        title text not null,
        text text not null,
    );

just sql语句:)<br/>

3.2:创建数据库<br/>
最简单的方法就是使用管道和sqlite3，将之前创建的表导入到数据库中:<br/>
<code>sqlite3 /tmp/flaskr.db < schema.sql</code><br/>
你也可以这样做：

    from contextlib import closing


    def connect_db():
       return sqlite3.connect(app.config['DATABASE'])


    def init_db():
        with closing(connect_db()) as db:  # closing 函数可以使数据库再整个with block中保持连接
            with app.open_resource('schema.sql', mode='r') as f:
                db.cursor.excutescript(f.read())  # 执行整个脚本
            db.commit()  # 向数据库提交

然后进入python shell:

    >>from flaskr import init_db()
    >>init_db()

数据库就创建完成了。

3.3:请求和关闭数据库连接<br/>
使用三个重要的装饰器：before_request[被注册函数在每次请求之前执行], after_request[被注册函数在每次请求之后执行,
如遇异常则终止执行], teardown_request[被注册函数在所有请求后(ctx pop 以后)执行，且遇异常不会终止，而且会接受error
的object!]<br/>

    from flask import g


    @app.before_request
    def before_request():
        """用来在请求之前连接数据库"""
        g.db = connect_db()


    @app.teardown_request()
    def teardown_request():
        """用来在请求之后关闭数据库"""
        if flask.g.get('db', None) is not None:
            db.close()

3.4:视图函数<br/>

    from flask import render_template, session, absort, flash, redirect, url_for, request


    @app.route('/')
    def show_entries():
        cur = g.db.excute('select title, text from entries order by id desc')
        entries = [dict(title=row[0], text=row[1]) for row in cur.fechall()]
        return render_template('show_entries.html', entries=entries)


    @app.route('/add', methods=["POST"])
    def add_entry():
        if not session.get('logged_in'):
            absort(401)
        g.db.excute('insert into entries (title,text) in values (?,?) ')
        g.db.commit()
        flash('New entries was successfully posted!')
        return redirect(url_for('show_entries'))  # 重定向到show_entries，由show_entries调用GET方法，表单也在
                                                  # show_entries中


    @app.route('/login', methods=["GET", "POST"])
    def login():
        error = None
        if request.method == 'POST':
            if request.form['username'] != app.config["USERNAME"]:
                error = 'Invalid username'
            elif request.form['password'] != app.config['PASSWORD']:
                error = 'Invalid password'
            else:
                session['logged_in'] = True
                flash('You were logged in')
                return redirect(url_for('show_entries'))
        return render_template('login.html', error=error)


    @app.route('/logout', methods=['GET'])
    def logout():
        session.pop('logged_in', None)
        flash('you were logged out!')
        return redirect(url_for('show_entries'))

**3.4:表单**<br/>
一般对表单的处理都是使用 flask-wtf 扩展，然后在模版中渲染表单。但是flaskr则是直接在html中构造表单，用action属性
与视图函数连接。

**3.5：模版**<br/>
至于模板都是jinja啦:)
