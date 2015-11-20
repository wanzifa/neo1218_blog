title: "CentOS+uWSGI+Nginx 部署flask全记录"
date: 2015-03-20 00:36:37
tags: 博客 flask

步骤0.准备工作
---
1.既然是部署，首先要买一台服务器（推荐在阿里云上买）。
2.之后就是选择合适的镜像了，本教程选取的是CentOS原版镜像(不要选集成环境，会发生怪怪的事情!)
3.安装连接服务器的工具（推荐 putty）
4.以root身份进入终端
5.安装所需的内库，进入 / 目录输入 
<code>yum groupinstall "Development tools"</code>
<code>yum install zlib-devel bzip2-devel pcre-devel openssl-devel ncurses -devel sqlite-devel readline-devel tk-devel</code>

步骤1.安装python
---
linux系统一般自带python，在终端任意位置输入 python —V 如果返回版本是2.7系列，恭喜可以跳过步骤一啦|）
如果版本较低比如和我一样是python 2.4。。那么进入家目录~ 输入：
1 <code>wget http://python.org/ftp/python/2.7.5/Python-2.7.5.tar.bz2</code>   (获取python安装包)
2 <code>tar xvf Python-2.7.5.tar.bz2</code>                                  （解压缩python安装包）
3 <code>cd Python-2.7.5</code>                                               （进入安装目录）
4 <code>./configure --prefix=/usr/local</code> 								  (编译源码，安装到/user/local/)
5 <code>#make && make altinstall</code>
安装好了以后输入 python2.7 就可以进入交互式命令行啦{）
注意：wget 是在线获取python安装包，所以网速要好哦！否则会返回 RunTimeError !

步骤2.安装python包管理
---
python的包管理工具给我们的安装带来了很大的方便！只需要简单的 pip命令！
进入到 ~ 目录下，输入;
<code>wget https://pypi.python.org/packages/source/d/distribute/distribute-0.6.49.tar.gz</code>
<code>tar xf distribute-0.6.49.tar.gz</code>
<code>cd distribute-0.6.49</code>
<code>python2.7 setup.py install</code>
<code>easy_install pip</code>
在任意位置输入 pip --version 如果返回版本号--恭喜，可以使用pip命令啦|）

步骤3.安装uwsgi
---
uwsgi就是我们web应用的服务器啦。他的功能很强大，尤其适合处理动态请求，但是不能处理http请求(这点很重要！)
进入 ~ 目录，输入：
<code>pip install uwsgi</code>
pip命令，立刻搞定！

测试uwsgi：
在 ~ 下新建test.py 内容如下：
<strong>def application(env, start_response):
			start_response('200 OK', [('Content-Type','text/html')])
			return "Welcome to MuxiStudio!"</strong>
在终端运行 </strong>uwsgi --http :8001 --wsgi-file test.py</strong>
在浏览器内输入：公网IP:8001/，如果返回 Welcome to MuxiStudio! 恭喜你 uwsgi安装成功！！！

步骤4.安装flask
---
既然是flask应用自然要安装flask啦！
我们采用虚拟环境安装flask，所谓虚拟环境即flask并不是安装在全局中，而是安装在我们指定的环境中，
只有进入这个环境才可以运行flask哦！这样我们就可以用一个实际python环境运行许多flask程序啦！

进入~目录，输入：
<code>pip install virtualenv</code>(安装虚拟环境)
进入项目所在的文件夹，例如：
<code>cd /root/www/flaskr/</code>
<code>virtualenv venv</code>(建立虚拟环境venv)
<code>source venv/bin/activate</code>（进入虚拟环境）
进入虚拟环境后，你会发现命令符前出现 (venv) 字样，很神奇呀！
退出虚拟环境只要输入 <code>deactivate</code>
进入虚拟环境<code>pip install flask</code>,搞定！！

步骤5.安装nginx
---
我们用nginx作反向代理，并处理http请求（之前说过uwsgi只能处理动态请求。其实通俗一点说就是前端nginx，后台uwsgi）
进入 ~ 目录下，输入
<code>wget http://nginx.org/download/nginx-1.5.6.tar.gz</code>
<code>tar xf nginx-1.5.6.tar.gz</code>
<code>cd nginx-1.5.6</code>
<code>./configure --prefix=/usr/local/nginx-1.5.6 --with-http_stub_status_module --with-http_gzip_static_module</code>
<code>make && make install</code>

到此，安装部分就顺利完成啦|），接下来让我们进入到有点小琐碎的配置环节吧！

步骤6.配置uwsgi
---
我们采用.ini文件配置uwsgi
在/etc/目录下新建 uwsgi.ini 文件，添加如下配置：
<strong>
[uwsgi]
socket = 公网IP:9090
master = true         //主进程
vhost = true          //多站模式
no-stie = true        //多站模式时不设置入口模块和文件
workers = 2           //子进程数
reload-mercy = 10     
vacuum = true         //退出、重启时清理文件
max-requests = 1000   
limit-as = 512
buffer-sizi = 30000
pidfile = /var/run/uwsgi.pid    //pid文件，用于下面的脚本启动、停止该进程
daemonize = /website/uwsgi.log
</strong>
uwsgi灵活的配置可以让flask应用的性能达到最佳，但对于你我一样的初学者往往就不知所云了。不过先不管是否完全理解配置项，
！！跑起来再说！！

步骤7.设置nginx
---
找到nginx的安装目录，打开conf/nginx.conf文件，修改server配置

	server {
			listen       80;
			server_name  localhost;
			location / {            
				include  uwsgi_params;
				uwsgi_pass  公网IP:9090;              			//必须和uwsgi中的设置一致
				uwsgi_param UWSGI_SCRIPT /root/www/flaskr.wsgi; //. 就相当于一层目录了 
				uwsgi_param UWSGI_CHDIR /root/www/flaskr;       //项目根目录(例如)
				index  index.html index.htm;
				client_max_body_size 35m;
				}
    }
	
步骤8.部署flask应用
---
终于---改装的装完了，该配的配完了。可我们的应用还不见踪影。。不要着急，我们将部署一个最简单的flask应用。
其实原理都是一样的！

在项目目录下（/root/www/flaskr）新建welcome.py文件，内容如下：

	from flask import Flask
	app=Flask(__name__)
	
	@app.route("/")
	def welcom():
		return "Welcome to MuxiStudio!"
		
	if __name__=="__main__":
		app.run(host="0.0.0.0",port=8080)
		
注意单有应用文件还不行，我们还要建立引导文件，在 /root/www/flaskr 下新建 wsgi.py

	from welcome import app

	if __name__=="__main__":
		app.run(host="0.0.0.0",port=8080)
导入app，设置运行状态--yep！

接下来就是最激动人心的部署环节了！
在/root/www/flaskr/下进入虚拟环境 还记得命令吗？ <code>source venv/bin/activate</code>
输入：<code>uwsgi --socket 公网IP:8080 --protocol=http -w wsgi:app -H /root/www/flaskr/venv</code>

终端会提示你uwsgi正在运行，在浏览器中输入 公网IP：8080/ 
<strong>"Welcome to MuxiStudio!"</strong>

步骤9.总结
---
不要怕出错，错了就谷歌一下，如果还不对就初始化重来，只要坚持，问题肯定可以解决！

步骤10.庆祝
---
合上电脑，出去走走。


