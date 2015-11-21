title: "flask学习笔记(6)——API 中"
date: 2015-04-06 00:46:27
tags: 博客 flask
img: http://7xj431.com1.z0.glb.clouddn.com/2kWVh9jrFWU.jpg

在上一篇博文中我们已经安装了flask-httpauth，接下来我们可以利用它进行用户认证了；<br/>
在我们初始化flask-httpauth扩展之前，我们要先创建一个HTTPBasicAuth类对象。<br/>
初始化Flask-HTTPAuth(app/api-1-0/authentication.py)

	from flask.ext.httpauth import HTTPBasicAuth
	auth = HTTPBasicAuth()

	@auth.verify_password
	def verify_password(email_or_token, password):
    	if email_or_token == '':
        	g.current_user = AnonymousUser()
        	return True
    	if password == '':
        	g.current_user = User.verify_auth_token(email_or_token)
        	g.token_used = True
        	return g.current_user is not None
    	user = User.query.filter_by(email=email_or_token).first()
    	if not user:
        	return False
    	g.current_user = user
    	g.token_used = False
    	return user.verify_password(password)

还记得上一篇博文中提到的401错误吗？当用户认证密令不正确时，服务器向客户端返回401错误，为了让服务器端返回的错误格式统一，我们可以自定义这个错误响应。<br/>
flask-httpauth错误处理程序(app/api-1-0/authentication.py)
	
	@api.before_request
	@auth.login_required
	def before_request():
    	if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden('Unconfirmed account')

在这里使用了before_request装饰器，如此我们便可以调用一次login_required装饰器并将其应用到整个api蓝本中。

<strong>基于令牌的认证</strong><br/>
由于rest风格的api具有无状态性，所以客户端在每次请求时都要发送http认证密令，但密令中包含着一些敏感信息，为了保护客户端的信息（这也是认证的初衷），我们采用更安全的、基于令牌的认证模式——用户向特定的url发送密令即可生成令牌，在令牌的寿命期限内只需令牌就可以完成认证。<br/>
为了生成和验证令牌，我们需要在数据库模型中新增两个方法，这两个方法用到了itsdangerous包<br/>
支持基于令牌的认证(app/models.py)

	class User(UserMixin, db.Model):
	#...
	def generate_auth_token(self, expiration):
        '''
		1.使用编码后用户的id生成签名令牌；2.指定以秒为单位的令牌寿命。
		'''
		s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
		'''
		验证解码后的令牌，并返回相应的用户id；
		'''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

支持令牌的改进验证回掉(app/api-1-0/authentication.py)

	@auth.verify_password
	def verify_password(email_or_token, password):
    	if email_or_token == '':
        	g.current_user = AnonymousUser()
        	return True
    	if password == '':
        	g.current_user = User.verify_auth_token(email_or_token)
        	g.token_used = True
        	return g.current_user is not None
   		user = User.query.filter_by(email=email_or_token).first()
    	if not user:
        	return False
    	g.current_user = user
    	g.token_used = False
    	return user.verify_password(password)

发送令牌至客户端的路由(app/api-1-0/authentication.py)
	
	@api.route('/token')
	def get_token():
    	if g.current_user.is_anonymous() or g.token_used:
        	return unauthorized('Invalid credentials')
    	return jsonify({'token': g.current_user.generate_auth_token(
        	expiration=3600), 'expiration': 3600})

到此，我们已经能够很好的处理客户端用户认证了。在接下来的博文中，让我们把目光放在如何用json的序列化表示资源吧！
