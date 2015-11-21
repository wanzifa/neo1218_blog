title: "Flask学习笔记(4)——web 表单"
date: 2015-04-03 00:37:45
tags: 博客 flask
img: http://7xj431.com1.z0.glb.clouddn.com/love.png

<strong>这次博客的主题是 web 表单</strong>
<p><strong>wiki百科解释</strong>：web 表单是一个网页表单，可以将用户输入的数据发送到服务器进行处理。因为互联网用户使用复选框，单选按钮或文本字段填写表格，所以WebForms的形式类似文件或数据库。例如，WebForms可以用来进入航运或信用卡资料订购产品，或可用于检索数据（例如，搜索引擎上搜索）。
其实我的理解是——web表单就是我们与浏览器交互的一个平台，我们把想说的悄悄话通过web表单告诉浏览器，浏览器就可以为我们做些事情啦！</p>
<strong>1.进入虚拟环境,安装扩展</strong>

<code><venv>$ pip install flask-wtf</code>

<strong>2.创建app文件</strong>

<code><venv>$ vim hello.py</code>
	
	from flask import Flask
	app = Flask(__name__)
	
	@app.route('/')
	def hello():
		return '<h1>Hello 木犀！</h1>'

	if __name__=='__main__':
		app.run(debug=True,port=8080)

<strong>3.配置Flask-WTF(./hello.py)</strong>

<code>app.config['SECRET_KEY'] = 'hard to guess string'</code>
<p>配置密钥的目的是为了防止CSRF攻击，关于CSRF攻击，请戳^^</p>
<a href="http://zh.wikipedia.org/wiki/%E8%B7%A8%E7%AB%99%E8%AF%B7%E6%B1%82%E4%BC%AA%E9%80%A0">CSRF</a>

<strong>4.创建表单类(./hello.py)</strong>
	
	from flask.ext.wtf import Form
	from wtforms import StringField,SubmitField
	from wtforms.validators import Required

	class NameForm(Form):
		name = StringField('你的姓名是？'，validators=[Required()])
		submit = SubmitField("提交！")

<p>	python是一种面向对象的编程语言，类的概念尤其重要，在这里我们创建了一个NameForm类--这是Form类的子类，继承表单的基本属性和行为。同时，我们给了他特殊的功能--用于提交你的名字！cool！
	StringField、和SubmitField 是两个类，分别用于处理字符串和提交。其实他们的背后是html代码的实现！
	至于Required()则是验证器--防止提交空的表单。</p>

<strong>5.渲染模板</strong>
#-------------------------------------#
不好意思，代码问题解决中ing...
#-------------------------------------#
然后启动服务器，你就可以告诉浏览器你的名字啦！

总结
---
创建一个web表单可以概括为以下几个步骤：
1.安装flask-wtf扩展
2.配置flask-wtf
3.创建表单类,确定表单的功能
4.渲染模板
