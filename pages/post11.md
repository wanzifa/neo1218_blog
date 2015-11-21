title: "uwsgi配置(1)——进程与线程"
date: 2015-04-07 22:42:41
tags: 博客 uwsgi
img: http://7xj431.com1.z0.glb.clouddn.com/love.png

最近在看《flask web 开发》的时候遇到了一个小bug，邮件发送不了，只有手动(ctrl+c)停止主程序后，邮件才可以发送。可见，一般的uwsgi配置启动命令已经满足不了我们越来越复杂的程序了，我记得在我的第一篇博客<a href="http://neo1218.github.io/2015/03/20/post1/" target="_blank">CentOS+uWSGI+Nginx 部署flask全记录 </a>中说到先把<strong>程序跑起来</strong>再说，但是现在不仅仅是跑起来，而且还要<strong>跑的好</strong>。所以我打算开辟一个新战场——uwsgi web服务器配置。<br/>
ok，回到博客的主题——进程与线程，其实上文中的邮箱bug就是一个进程问题，发送邮件的进程和网站主程序的进程冲突了，导致运行网站主程序的时候邮件无法发送。那么该如何解决呢？我们只要修改uwsgi服务器的启动命令(在命令里增加配置)：<br/>
<code>uwsgi --socket 121.43.230.104:5000 --protocol=http -w wsgi:app -H /root/www/flaskr/venv <strong>--master --processes 4 --threads 2</strong></code>
注意加粗的部分，在这里，我们给uwsgi服务器增加了4个进程，每个进程设置了2个线程，再次运行程序的时候，你会发现邮件飞快的送入你的邮箱(虽然在垃圾邮件中..)，网站主程序也运行正常。bug解决了，似乎一切ok。但是总感觉有些不对劲，对了——进程、线程是什么呀！<br/>
其实通俗的说，你可以把<strong>一个个进程</strong>视为<strong>一个个车间</strong>，每一个进程中的<strong>线程</strong>就像车间里的<strong>工人</strong>，这些车间共同组成了我们的程序工厂，运行着我们的程序。<br/>
<small>如果你想深入的了解进程与线程，请参见我的<strong>博客 推荐</strong>里的链接2。</small>
