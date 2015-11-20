title: "flask学习笔记(3)——蓝图"
date: 2015-04-02 22:40:12
tags: 博客 flask

今天花了一下午，把博客的源码看了一遍，对蓝图有了大致的了解。在这篇博客中我想对蓝图的应用做一个总结，可能会有疏忽，但就是想理清楚自己的思路。<br/>
<strong>1.为什么要用蓝图</strong><br/>
为什么要用蓝图？因为网站的运行环境复杂，已知至少有三种环境：开发环境、测试环境、生产环境。每个环境的的数据库、配置文件都不一样，可见一个全局的app实例显然无法满足我们的需求了。于是我们就想，能不能在局部作用域中创建不同的实例，在不同的环境中调用呢？当然可以，这其实就是工厂函数的概念，工厂函数就是在该函数作用域中创建app的函数。但是，但是！问题来了，如果在函数内部创建app，那么url岂不是要在执行函数被调用后才会被注册，可是没有url如何访问执行函数呢？这不就是一个先有鸡还是先有蛋的问题吗？于是蓝图就被推上了历史的舞台^^。<br/>
<strong>2.什么是蓝图</strong><br/>
说了这么多，那到底什么是蓝图呢？蓝图其实是一个网站程序,是定义url的一种方式。网站实例注册蓝图后，我们就可以访问蓝图定义的url，而不用深入执行函数去找app了。<br/>
<strong>3.代码实现</strong><br/>
附上一个小例子：<br/>
1.~/flasky/app/-init-.py<br/>
	
	from flask import Flask
	from config import config
	
	def create_app(config_name):
		'''
		工厂函数
		'''
		app = Flask(__name__)
		app.config.from_object(config[config_name])                                    
    	config[config_name].init_app(app) 
		#注册蓝图
		from .main import main as main_blueprint                                        
    	app.register_blueprint(main_blueprint)
	
		return app

2.~/flasky/app/main/-init-.py<br/>

	#导入蓝图
	from flask import Blueprint
	#实例化蓝图（参数1：蓝图的名字；参数2：蓝图所在的包or模块）
	main = Blueprint('main', __name__)

	from . import views

	@main.app_context_processor
	def inject_permissions():
    	return dict(Permission=Permission)
3.~/flasky/app/main/views.py
	
	from flask import render_template
	from . import main

	@main.route('/')
	def index():
	    return render_template('index.html')

注意咯，这里路由的注册方式是main.route，此外，蓝图还提供命名空间注册路由，这样index在main.index 和 auth.index 下是不一样的路由哦。
