title: "nginx反向代理uwsgi部署flask应用"
date: 2016-01-01 21:50:50

## 写在前面
这是一篇教程!<br/>
这是一篇关于如何在服务器上部署flask应用的教程!<br/>
这是一篇讲解如何在centos服务器上使用nginx反向代理uwsgi服务器部署flask的教程...<br/>

## 一些概念

0. centos服务器: 运行着centos系统的服务器, centos是一个Linux发行版, 这篇教程以centos7为例。<br/>
1. nginx服务器: nginx是一个由俄罗斯工程师设计的web服务器, 尤其擅长处理静态文件。<br/>
2. uwsgi服务器: 一个实现了WSGI协议的web服务器。<br/>

## 为什么要用 nginx反向代理uwsgi?
其实只用uwsgi服务器完全可以实现flask应用的部署, 但是使用nginx反向代理可以提高服务器响应的性能。nginx擅长处理静态文件,
所以可以把请求由nginx接受, 如果请求静态文件则nginx直接返回, 动态请求再转交uwsgi处理, 这样nginx就相当于uwsgi和客户端之间的一层代理。

## 开始吧! 安装uwsgi和nginx
### 1. 安装所需组件

1. EPEL

    $ sudo yum install epel-release

2. python, pip

    $ sudo yum install python-pip python-devel

3. gcc

    $ sudo yum install gcc

### 2. 安装nginx

    $ sudo yum install nginx

#### 3. 安装uwsgi

    $ sudo pip install uwsgi

## 创建你的flask应用
这里使用我自己造的轮子[mana](https://github.com/neo1218/mana)来构建一个简单的flask应用

    $ mana init flaskapp

这样就创建了名为flaskapp的flask应用<br/>
接下来是创建虚拟环境

    $ virtualenv venv

进入虚拟环境

    $ source venv/bin/activate

安装所需扩展

    $ pip install -r requirement.txt

在本地运行应用

    $ python manage.py runserver

没有报错, 一切正常。

<hr/>
## [部署]配置uwsgi
### 编写 wsgi.py
进入项目(以flaskapp为例, 下同)的根目录下, <code>vim ~/wsgi.py</code>

    # coding: utf-8
    from app import app

    if __name__ == "__main__":
        app.run()

这样WSGI服务器就可以调用wsgi.py文件去运行python应用。<br/>
[⚠ ]: 在生产环境下不可开启调试器!<br/>

### 配置uwsgi服务器
使用ini文件对uwsgi服务器进行配置,<br/>
在flaskapp项目根目录下创建flaskapp.ini文件,<br/>
配置如下:

    [uwsgi]
    module = wsgi:app

    master = true
    processes = 5

    socket = flaskapp.sock
    chmod-socket = 660
    vacuum = true

    die-on-term = true

### 启动配置好的uwsgi服务器
你只要在终端输入

    $ uwsgi --ini flaskapp.ini&

即可启动并在后台运行 uwsgi 服务器

##[部署]配置运行项目
为了更加方便的运行我们的项目, 我们可以编写 service
文件,这样可以方便启动我们的项目(包括uwsgi服务器),并可以设置为开机自启动。<br/>
创建<code>/etc/systemd/system/flaskapp.service</code>文件:

    [Unit]
    Discription=uWSGI instance to serve flaskapp
    After=network.target

    [Service]
    User=user
    Group=nginx
    WorkingDirectory=/abs/path/to/flaskapp
    Environment="PATH=/abs/path/to/flaskapp/venv/bin"
    ExecStart=uwsgi --ini flaskapp.ini

    [Install]
    WantedBy=multi-user.target

保存service配置文件, 我们就可以方便的启动和停止我们的项目了

    $ sudo systemctl start flaskapp  => 启动flaskapp
    $ sudo systemctl enable flaskapp  => 设置flaskapp为服务器开机自启动
    $ sudo systemctl stop flaskapp => 停止运行flaskapp

## [部署]接下来就是配置nginx反向代理了
修改nginx配置文件(/etc/nginx/nginx.conf)

    在http配置里再开一个server

    http {
        ...
        include /etc/nginx/conf.d/*.conf;
        server {
            # 新开的server配置
        }

        server {
        ......
        }
        ......
    }

配置如下:

    server {
        listen 80;
        server_name 域名或者ip;
        location / {
            include uwsgi_params;
            uwsgi_pass unix:/abs/path/to/flaskapp.sock;
        }
    }

## [部署]将nginx添加到用户组

    $ sudo usermod -a -G your_username nginx

## [部署]设置权限, 运行nginx进程在家目录中写入内容

    $ sudo chmod 710 /home/your_username

## [部署]加载nginx配置文件
检测nginx配置文件是否有语法错误

    $ sudo nginx -t

如果没有报错, 就可以加载配置了

    $ sudo nginx -s reload

## [部署]启动nginx服务器

    $ sudo systemctl start nginx  => 启动nginx服务器
    $ sudo systemctl enable nginx  => 设置nginx为开机自启动
    $ sudo systemctl stop nginx  => 关闭nginx

<hr/>
## 部署完毕
现在我们可以查看系统进程<code>$ netstat -nplt</code>, 我们可以看到nginx的进程已经在相应的端口上运行了,我们看不到uwsgi的进程，因为uwsgi已经被nginx代理了。


## 进阶
[更多nginx配置, 建议阅读《精通nginx》](http://book.douban.com/subject/26341690/) <br/>
![精通nginx](http://img6.douban.com/lpic/s28271787.jpg)<br/>

## 参考
[how-to-serve-flask-applications-with-uwsgi-and-nginx-on-centos-7](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-centos-7)
