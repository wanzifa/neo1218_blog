title: "flask 学习笔记(1)——flask简介&安装"
date: 2015-04-01 00:13:27
tags: 博客 flask
img: http://7xj431.com1.z0.glb.clouddn.com/love.png

1.flask简介
---
互联网的世界是自由的、是神奇的。而<strong>python flask</strong>则是我们进入网络内核世界的一个工具！
flask 是基于python的一个轻量级的web开发框架——>让我来解释一下这句话:
——>基于python：flask采用python语言开发，继承了python面向对象的编程方式(甚至数据库也是^^)
——>轻量级：flask仅依赖两个东西：1.路由，调试. 2.WSGI(web 服务 网关 接口)(具体见：URL)，子系统有Werkzeug提供，模板有Jinjia2模板引擎提供。当然，轻量不代表功能低。flask绝大多数的核心功能来自于flask扩展，因而你可以选择自己想要实现的功能的扩展，自由、方便！
——>web开发框架: 这是flask最本质的功能，他能让你在开发web程序时更省力！

2.flask安装
---
——><strong>windows下安装</strong>
--------------------------------安装python----------------------------------------------
1>去python官网下载页(https://www.python.org/downloads/)下载python2.7
2>下载后按步骤安装
3>在开始菜单栏找到python，或在cmd中任意位置输入python ——>出现python命令行，则安装成功
4>python自带IDLE，不过推荐notepad++，sublime text，后面写flask程序时会更方便

--------------------------------设置虚拟环境--------------------------------------------
我们采用虚拟环境virtualenv安装flask，这可以让不同的flask应用程序互不干扰且共用一套python
1>安装pip(pip是python包管理工具，后面许多扩展都是通过pip安装是)
——><strong>下载 distribute_setup.py</strong>
——><strong>双击 distribute_setup.py运行文件</strong>
——><strong>添加 ;C:\Python27\Scripts 到 PATH 环境变量</strong>
——><strong>进入cmd:</strong><code>easy_install pip</code>
2>进入cmd 
<code>pip install virtualenv</code>——>注意，如果你的windows用户名是中文的话，pip可能会报错，不过也不要慌，换一个就行了^^
3>创建项目文件夹(C:/flasky)
<code>mkdir flasky</code>
<code>cd flasky</code>
——><strong>虚拟化项目文件夹(创建虚拟环境入口)</strong>
<code>virtualenv venv</code>
——><strong>进入虚拟环境</strong>
<code>cd venv/Scripts/</code>
<code>activate</code>
这时你会发现命令提示符前出现了(venv) ——>已进入虚拟环境^^
——><strong>退出虚拟环境</strong>
<code>Ctrl C</code>

--------------------------------安装flask--------------------------------------------------
1>进入刚刚创建的虚拟环境
2><code>pip install flask</code>
--------------------------------安装成功！-------------------------------------------------
——><strong>linux下的安装详见我的博文(CentOS+uWSGI+Nginx 部署flask全记录)</strong>
