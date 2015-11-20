title: "flask 学习笔记(2)——flask基本程序结构"
date: 2015-04-01 00:24:45
tags: 博客 flask

#本次笔记将介绍flask的基本程序结构，并写出第一个web应用
--------------我们选择在服务器端直接编程---------------

0.基本框架
---
<code>mkdir /root/www/flasky</code>新建项目文件夹
<code>vituralenv venv</code>创建虚拟环境
<code>source venv/bin/activate</code>进入虚拟环境
<code>pip install flask</code>安装flask
<code>vim hello.py</code>
	
	from flask import Flask 
	app = Flask(__name__)
	
	@app.route('/')	
	def index():
		return 'Come from MuxiStudio!'
	if __name__=="__main__":
		app.run(debug=True)

程序的首先从flask模块中导入Flask类，利用Flask类实例化app(__name__是Flask类的一个属性)，利用route(路由)装饰器关联url和执行函数(index)，index函数会在相应的url地址返回字符串“Come from MuxiStudio!”。最后程序判别__name__属性，调用run方法，开启调试模式(debug=True),运行app。

好吧，我想你肯定是一头雾水，不过不要着急，我接下来将逐字逐句的解释上面这段话！

1.Flask类实例化app
---
如果你没有接触过面向对象编程，那么这句话可能对你而言就像天书，不过没关系，请戳下面链接
<a href="http://www.zhihu.com/question/19854505">面向对象思想</a>
我的理解是--Flask类具有定义好的属性和方法,app被实例化后也就继承了这些方法。

2."__name__"属性
---
"__name__"属性就是Flask类的一个很重要的属性啦！在正式介绍他的用处之前我们先理解一下flask的目录组织方式。
----flask的目录组织结构没有强制要求--

	------|——>app————————————————|——>__init__.py
	------|——>db_repository------|——>static
	flask—>venv------------------|——>templates
	------|——>config.py----------|——>views.py
	------|——>run.py-------------|——>forms.py
	------|——>runp.py------------|——>modles.py
	------|——>readme.md

以上就是一个flask项目的文件组织结构，<strong>app</strong>是app应用程序所在的主目录，<strong>db_repository</strong>是与数据库迁移相关的(以后再说)，<strong>venv</strong>就是我们创建的虚拟环境入口文件夹,<strong>config.py</strong>是配置文件，<strong>run.py</strong>是开发时应用程序的启动文件，<strong>runp.py</strong>是生产环境下的启动文件( 两者的区别在于生产环境千万不能开调试器，这会让使用者看到不该看到的代码！)<strong>readme.md</strong>是一个项目介绍文件，用的也是markdown语法。 
再看看<strong>app</strong>文件夹，<strong>static</strong>用于存放css、image等静态文件，<strong>templates</strong>用于放置模板文件，<strong>views.py</strong>是视图函数所在的模块，<strong>forms.py</strong>则是表单所在的模块，<strong>modles.py</strong>是数据库表对象所在的模块，而<strong>__init__</strong>.py....

对，__init__.py和我们的__name__属性有着密切的关系：首先__init__.py是app创建的地方，但我们知道app的运行是在run.py中调用的呀！这时就需要把app变成包，以便让其他程序导入app文件夹中的模块，而__init__.py就是模块的标志。通过在运行时判别__name__属性就可以知道该程序究竟是作为模块被导入还是直接执行！原来如此！可是这有什么用呢？这就要谈到templates文件夹了，程序在运行时会寻找该文件夹中的模板，如果app是直接执行则templates文件夹应放置在于app所在文件同级的位置，如果app作为模块被导入则应该一起放于包中！

3."路由"与装饰器
---
"路由"是flask的一种装饰器，你可能会问什么是装饰器，请戳下面：
<a href="http://segmentfault.com/blog/xuelang/1190000000632572">python装饰器</a>
我的理解，装饰器就是让函数具有附加行为的东西，python的装饰器可以通过语法糖@实现

再说说路由装饰器，我们访问网站输入的网址其实是url--统一资源定位器，通过特定的url就可以得到特定的页面，可是服务器如何知道对于这个页面应该调用哪个执行函数呢？路由装饰器就可以把其下的执行函数与url绑定在一起，解决这个问题！

4.返回字符串
---
返回字符串其实不应该直接在函数中进行，应该由模板完成！至于模板下次再说！

-------------------------------------部署web应用-----------------------------------
1.设置nginx
---
找到nginx的安装目录，打开conf/nginx.conf文件，修改server配置

	server {
			listen       80;
			server_name  localhost;
			location / {            
				include  uwsgi_params;
				uwsgi_pass  公网IP:9090;                          //必须和uwsgi中的设置一致
				uwsgi_param UWSGI_SCRIPT /root/www/flasky.wsgi; //. 就相当于一层目录了 
				uwsgi_param UWSGI_CHDIR /root/www/flasky;       //项目根目录(例如)
				index  index.html index.htm;
				client_max_body_size 35m;
			}
	}

2.建立引导文件
---
在 /root/www/flasky 下新建 wsgi.py

	from hello import app

	if __name__=="__main__":
		app.run(host="0.0.0.0",port=8080)

3.开启uwsgi服务器
在/root/www/flasky/下进入虚拟环境 还记得命令吗？ source venv/bin/activate
输入：uwsgi —socket 公网IP:8080 —protocol=http -w wsgi:app -H /root/www/flasky/venv

---------------------------------------补充------------------------------------------
如果你没有服务器，利用命令行进入虚拟环境,<code>python hello.py</code> 
在python自带的127.0.0.1上也可以看到。
