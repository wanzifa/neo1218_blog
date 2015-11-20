title: "flask学习笔记（5）——API 上"
date: 2015-04-04 17:13:18
tags: 博客 flask

今天把flask web 开发教程上的api看完了，成功得到了教程实例的api，这篇博文主要以这个实例为例，对api进行总结，也是帮助自己理清思路。
ok开始吧！<br/>
<strong>1.What is API?</strong><br/>
--
首先，什么是api，api全称应用编程接口（application program interface），是连接服务器与除浏览器外的其他客户端（如手机app）的接口。<br/>
<strong>2.api 有什么用？</strong><br/>
--
首先我们要明确，在手机端、app，服务器的角色已经发生了变化，服务器不在是程序的控制者，而转变为资源的提供者——将数据库中的资源提供给手机客户端。而api就是资源流通的大门！<br/>
<strong>3.restAPI<br/></strong>
--
flask支持rest风格的API，这是API的的一种，详见：
<a href="http://zh.wikipedia.org/wiki/REST" target="_blank">restAPI</a><br/>
<strong>4.资源就是一切！<br/></strong>
--
一个网站，一个服务器最核心也是最需要保证的地方就是数据库，在电影《社交网络》中，马克.扎克伯格说过这样一句话：‘facebook与其他所有网站不一样的地方是它永远也不会崩溃，可是如果有一天数据库毁了，那它就完了！’，虽然电影渲染的有点夸张，但我们不得不承认数据库的重要性，数据库是网站的灵魂，而数据库里的数据则是一个网站赖以生存的血液。。当我们把目光转向移动端
，这些数据，也就变成了移动端所需的资源！<br/>
<strong>5.API代码示例：<br/></strong>
---
我们将为《flask web 开发》中的示例网站建立一个api<br/>
如果需要代码：<code>git clone https://github.com/neo1218/flasky.git</code><br/>
<strong>5.1:API蓝图结构</strong><br/>
如果不清楚什么是蓝图的话，请参见我的另一篇博客:<a href="http://neo1218.github.io/2015/04/02/post6-1/" target="_blank">flask学习笔记（3）——蓝图</a>
	
	|-flasky
		|-app/
			|-api_1_0
				|-__init__.py
				|-users.py
				|-posts.py
				|-comments.py
				|-authentication.py
				|-errors.py
				|-decorators.py

注：api_1_0,是api的版本号，要想明白为什么要设置版本号，首先我们要了解web浏览器和智能手机客户端的区别，web浏览器其实就是一个显示工具（显示html代码），它执行的代码就是服务器端的代码，所以服务器端版本更新后，浏览器能够很好的更新所有的用户。但是，手机的原生应用就不一样了，它只是利用服务器端的数据，app的开发代码都不一样(比如我们学校的桂声app，java开发，后台是python)，也就是说，应用更新是需要得到机主的允许的，如果机主不想更新呢？那么只有继续运行旧的程序啦，所以我们的服务器上要运行多套程序的，版本号的作用就不言而喻了吧！<br/>
1.API蓝图的构造文件(app/api-1-0/-init-.py)

	from flask import Blueprint
	
	api = Blueprint('api',__name__)

	from . import authentication, posts, users, comments, errors

2.注册API蓝图(app/-init.py-)
	
	def create_app(config_name):
		#...
		from .api_1_0 import api as api_1_0_blueprint
		app.register_blueprint(api_1_0_blueprint,url_prefix='/api/v1.0')
		#...

3.错误处理<br/>
在学习错误处理之前我们要了解两个概念：1.rest风格支持的http方法	，2.http状态码<br/>
1.rest风格支持以下几种http请求方法：<br/>

	1.GET: 单个资源的url 获取目标资源	
	2.GET: 资源集合的url 获取目标资源的集合（如果实现了分页则返回该页的资源集合）
	3.PUT: 单个资源的url 修改一个现有资源，如果客户端能够指派一个新的url则可以创建一个新的资源
	4.POST:资源集合的url 创建一个新的资源，并加入资源集合，由服务器为资源指派一个新的url
	5.DELETE: 单个资源的url 删除该资源
	6.DELETE: 资源集合的url 删除该资源集合中的所有资源

由上表我们可以看到url的重要性，客户端对资源的操控是以url为核心！<br/>
2.http状态码：
	
	200：                    OK                		请求成功完成 
	201：					Greated           		请求成功完成，并创建一个新资源
	400：                    Bad request      		请求不可用或不一致                 
	401：					Unauthorized      		请求未包含认证信息
   	403：                    Forbidden         		请求中发送的认证密令无权访问目标    
	404：					Notfound          		URL对应的资源不存在
	405：					Method not allowed 		指定资源不支持请求所用的方法
	500：					Internal server error 	内部服务器发生意外错误

另附上链接<a href="http://www.w3cschool.cc/w3cnote/404-page-design.html" target="_blank">创意404界面</a><br/>
<a href="https://thepiratebay.se/404" target="_blank">tpb</a><br/>
处理405和500状态码会比较麻烦，因为这两个错误是api自己生成的，而且返回的是html响应，所以我们要通过内容协商机制，把响应改为json格式（javascript object notation）<br/>
使用http内容协商处理错误(app/main/errors.py)
	
	@main.app_errorhandler(404)
	def page_not_found(e):
	#程序在请求的首部进行响应格式检查
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404

<strong>使用Flask-HTTPAuth认证用户</strong><br/>
资源很重要，所以资源也是需要保护的，但更多的是保护用户的信息不对外泄露。<br/>
如果大家之前认真看过我给的rest介绍（那个链接），那么你肯定会记得rest web 服务有一个很重要的一个特征--无状态，也就是说rest在两次请求之间不能记住客户端的任何信息，也就是服务器是不存储任何关于用户信息的，对于浏览器而言，可以把用户信息存储在cookies中，但对于手机端这种并不支持cookies的客户端就无能为力了！所以在每次请求中，客户端都要包含密令。<br/>
因为rest服务基于http协议，所以我们采用基于flask的httpauth认证!<br/>
1.在虚拟环境中安装flask-httpauth：<br/>
<code>pip install flask-httpauth</code>

	现在我们已经安装好了flask-httpauth，在下一篇博客中我们会继续处理认证系统，以及如何以json格式返回资源，和对资源url的处理！
