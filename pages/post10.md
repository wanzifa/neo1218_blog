title: "flask学习笔记(7)——API 下"
date: 2015-04-06 09:43:36
tags: 博客 flask
---
在上一篇博文中，我们成功的处理了客户端的认证系统，在这一篇博客中我们将解释如何把资源json序列化，以及如何处理资源的url问题。<br/>
<strong>资源和JSON的序列化转换</strong></br>
在第一篇已经介绍过，JSON（Javascript Object Notation）是http协议的传输和响应格式，所以我们需要把数据库中的资源以JSON的格式规范化。<br/>
把文章转化为json格式的序列化字典(app/models.py)

	class Post(db.Model):
		#...
		def to_json(self):
        	json_post = {
            	'url': url_for('api.get_post', id=self.id, _external=True),
            	'body': self.body,
            	'body_html': self.body_html,
            	'timestamp': self.timestamp,
            	'author': url_for('api.get_user', id=self.author_id,
                              _external=True),
            	'comments': url_for('api.get_post_comments', id=self.id,
                                _external=True),
            	'comment_count': self.comments.count()
        	}
        	return json_post

可以看到，资源的绝大多数属性和数据库模型是一致的，但是我们也可以自己添加虚拟的属性比如comments_count<br/>
我们给每一个返回url的属性都添加了_externel=True,从而返回url的绝对路径，这样的好处是用户可以从明确的顶级url中自己挖掘出其他资源的url。<br/>
把用户转化为json格式的序列化字典（app/models.py）

	class User(UserMixin,db.Model):
		#...
		def to_json(self):
        	json_user = {
            	'url': url_for('api.get_post', id=self.id, _external=True),
            	'username': self.username,
            	'member_since': self.member_since,
            	'last_seen': self.last_seen,
            	'posts': url_for('api.get_user_posts', id=self.id, _external=True),
            	'followed_posts': url_for('api.get_user_followed_posts',
                                      id=self.id, _external=True),
            	'post_count': self.posts.count()
        	}
        	return json_user
然而客户端提供的数据可能是空的、错误的，所以客户端创建文章的时候我们要对客户端提交的文章进行验证。<br/>
从JSON格式数据创建一篇文章（app/models.py）

	from app.exceptions import ValidationError
	
	Class Post(db.Model):
		#...
		@staticmethod
    	def from_json(json_comment):
        	body = json_comment.get('body')
        	if body is None or body == '':
            	raise ValidationError('comment does not have a body')
        	return Comment(body=body)

当用户提供的文章出现问题的时候会抛出ValidationError异常，接下来我们要来处理这个异常。<br/>
API中ValidationError异常的处理程序(app/api-1-0/errors.py)

	@api.errorhandler(ValidationError)
	def validation_error(e):
    	return bad_request(e.args[0])

我们还要在视图函数中定义用户提交文章的路由(flasky/app/api-1-0/posts.py)

	@api.route('/posts/', methods=['POST'])
	@permission_required(Permission.WRITE_ARTICLES)
	def new_post():
	    post = Post.from_json(request.json)
	    post.author = g.current_user
	    db.session.add(post)
	    db.session.commit()
	    return jsonify(post.to_json()), 201, \
	        {'Location': url_for('api.get_post', id=post.id, _external=True)}

可以看到有了前面的铺垫，视图函数的代码已经很简洁了。

到目前为止，我们的资源已经很好的序列化了，用户认证也很完善了，接下来我们将实现api真正的功能——与客户端交互。客户端将请求http方法，而我们将返回相应的路由。让我们再来回顾一下http方法ba:<br/>

	1.GET: 单个资源的url 获取目标资源	
	2.GET: 资源集合的url 获取目标资源的集合（如果实现了分页则返回该页的资源集合）
	3.PUT: 单个资源的url 修改一个现有资源，如果客户端能够指派一个新的url则可以创建一个新的资源
	4.POST:资源集合的url 创建一个新的资源，并加入资源集合，由服务器为资源指派一个新的url
	5.DELETE: 单个资源的url 删除该资源
	6.DELETE: 资源集合的url 删除该资源集合中的所有资源

文章资源GET请求处理程序（app/api-1-0/posts.py）

	@api.route('/posts/')
	@auth.login_required
	def get_post():
		'''
		返回文章资源的集合
		'''
		posts = Post.query.all()
		return jsonify({'posts':[post.to_json() for post in posts]})		

	@api.route('/posts/<int:id>')
	@auth.login_required
	def get_post(id):
		'''
		返回特定id的文章
		'''	
    	post = Post.query.get_or_404(id)
    	return jsonify(post.to_json())	
	
如果特定id的文章不存在，会返回404错误。你也可以自己定义404错误界面。<br/>

文章资源的POST请求处理程序（app/api-1-0/posts.py）

	@api.route('/posts/', methods=['POST'])
	@permission_required(Permission.WRITE_ARTICLES)
	def new_post():
    	post = Post.from_json(request.json)
    	post.author = g.current_user
    	db.session.add(post)
    	db.session.commit()
    	return jsonify(post.to_json()), 201, \
        	{'Location': url_for('api.get_post', id=post.id, _external=True)}

permission_required()装饰器（app/api-1-0/decorators.py）

	def permission_required(permission):
    	def decorator(f):
        	@wraps(f)
        	def decorated_function(*args, **kwargs):
            	if not g.current_user.can(permission):
                	return forbidden('Insufficient permissions')
            	return f(*args, **kwargs)
        	return decorated_function
    	return decorator

我们还需要PUT方法对文章进行更新<br/>
文章资源的PUT请求处理程序（app/api-1-0/posts.py）

	@api.route('/posts/<int:id>', methods=['PUT'])
	@permission_required(Permission.WRITE_ARTICLES)
	def edit_post(id):
    	post = Post.query.get_or_404(id)
    	if g.current_user != post.author and \
            	not g.current_user.can(Permission.ADMINISTER):
        	return forbidden('Insufficient permissions')
    	post.body = request.json.get('body', post.body)
    	db.session.add(post)
    	return jsonify(post.to_json())

这里的验证比较复杂，不过程序还比较好懂。<br/>


到这里，我们的API学习就要接近尾声了，我们实现了API客户端的认证、资源的JSON序列化、以及如何利用http方法与客户端交互，当然还有对错误格式的处理。不过大家对API可能还是觉得有些抽象，API呈现给客户端的究竟是什么样的呢？<br/>
不用着急，利用火狐的RESTCilent插件，我们就可以一窥API的真容了！<br/>
以我们的API为例：查询http://hostname:5000/api/v1.0/posts/，GET请求，就可以看到API的json序列啦！<br/>
![再见](C:\\hexo\\source\\img\\post10.jpg)