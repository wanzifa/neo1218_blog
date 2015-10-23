title: 记爬取CET4报名网站的那一夜
date: 2015-09-26 20:54:03
tags: 博客 小记
---
## 首先:

    中秋节快乐

## 然后:

    没有了...

## 回寝室之前在304的晚上
转眼间就大二了，于是就要考四级，考四级就要报名，于是去了报名网站http://cet.tinyin.net/accuse.asp, 上传了照片，报了名,理论上就结束了。但是，中秋要来了，我要做点什么。<br/>
四级报名网站为了公平公正，将每个报名学生的基本信息(姓名、学号、大头照、报考等级)放在了网上，这样同学院、同年级的同学就可以进行监督。不得不说，证件照是很吸引人的部分，于是我审查了页面元素，希望可以发现更多a。

    <img width="120" border="0" height="160" src="photos/2014210761.jpg"></img>

<code>photos/2014210761.jpg</code>，有意思，看上去似乎是某个子目录，于是我尝试加上了主机名

    http://cet.tinyin.net/photos/2014210761.jpg

于是我可爱的证件照出现了。。。而且，等我登录过期后，我依然可以访问这个url看到图片(现在就可以试试)！！这意味着我可以通过改变学号看到同学的大头照!😄

## 然而我并不知道学号
是的，我知道我的同学的名字，但是记不住学号。但是CET4报名网站已经将姓名学号一并奉上了，我要做的就是抓取姓名和学号信息，并将这些信息写入文件，建立关系，就像这样:

    学生学号：2014210761 学生姓名：朱承浩
    学生学号：2014210781 学生姓名：我室友
    ......  ......  ....... .....  ......

## 买了两瓶啤酒🍺 ，开爬! 当然还有 httpfox
### 模拟登录
首先就是要登录进报名网站，才可以访问信息页的url。打开 httpfox，监听登录过程
![监听过程](http://7xj431.com1.z0.glb.clouddn.com/屏幕快照%202015-09-27%20上午4.31.54.png) <br/>
![相关信息](http://7xj431.com1.z0.glb.clouddn.com/屏幕快照%202015-09-27%20上午4.34.51.png) <br/>
CET4网站为了防我这种好奇心很强的人还是做了一些处理，登录url<code>/login.asp</code>实际上是一个refer，真正的登录url是<code>http://cet.tinyin.net/reginfo.asp</code>，我要做的，就是利用我的用户名和密码登入网站，获取cookie，然后利用cookie进行后续登录。当然，首先需要把我自己变成浏览器啦

    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:42.0) Gecko/20100101 Firefox/42.0"
        self.headers = {
                'User-Agent':self.user_agent,
                'Referer':'http://cet.tinyin.net/login.asp',
                'Accept-encoding':'gzip'
        }
        self.postdata = urllib.urlencode({
                'stype':'#',
                'stuno':'2014214761',
                'stupwd':'密码就不说了'
        })

然后就是登录获取cookie

    def analog_login(self):
        """
        登录cet4网站，获取cookie，并将
        cookie保存至文件
        """
        filename = 'cet4_cookie.txt'
        cookie = cookielib.MozillaCookieJar(filename)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

        login_url = 'http://cet.tinyin.net/reginfo.asp'
        request = urllib2.Request(login_url, self.postdata, self.headers)
        opener.open(request)
        cookie.save(ignore_discard=True, ignore_expires=True)

cookie get!!!

    # Netscape HTTP Cookie File
    # http://www.netscape.com/newsref/std/cookie_spec.html
    # This is a generated file!  Do not edit.

    cet.tinyin.net	FALSE	/	FALSE		ASPSESSlllllDAQBASRAC	LKNFEMDCDOLABMFPLLLLL

### 该正则表达式上场了!
首先实验一下，cookie能否正常使用, 尝试访问 http://cet.tinyin.net/accuse.asp 页面, cookie是没问题，但是html却是中文乱码，没关系，改成utf-8，就行

    html = response.read().decode('gbk').encode('utf-8’)

![html](http://7xj431.com1.z0.glb.clouddn.com/屏幕快照%202015-09-25%20下午11.48.57.png) <br/>
现在，一切都豁然开朗了，我只需要爬取<td>标签，将获取的学号和姓名写入文件就行了。

    正则表达式 parttern = re.compile('<td width=25% >(.*?)<br><br>(.*?)<br><br>', re.S)

[爬取的信息文件](https://github.com/neo1218/CET4-photo/blob/master/stuinfo.txt) <br/>


### flask 靠你了
接下来就是用flask搭一个搜索引擎了。在文字编码这一块用了很长时间，因为表单的输入数据编码和文件的编码是不匹配的，经过几次实验，我发现需要将表单输入数据decode为汉字编码

    name = form.name.data.decode('utf-8')

编码真头痛！！看一下这篇吧http://dengshuan.me/misc/xi-shuo-bian-ma-yu-luan-ma.html <br/>


### ok了
![有图为证](http://7xj431.com1.z0.glb.clouddn.com/屏幕快照%202015-09-27%20上午5.22.50.png) <br/>

## 备注
#### 实际的过程没有上面说的这么的一气呵成，中间还睡了一觉😄 <br/>
#### 两瓶啤酒没有喝完<br/>
#### 信息都是公开的，应该没有侵犯隐私吧😔 <br/>
#### 开心就好😄 <br/>
