title: "python 学习笔记(day 1)"
date: 2015-06-04 14:54:38
tags: 博客 python
---
<strong>前言:</strong><br/>
接触python快半年了,回过头把基础再总结一下应该会更好.<br/>
<strong>1.python style</strong><br/>
请见 <a href="http://neo1218.github.io/2015/05/25/post24-md/">import this</a><br/>
python采用缩进的方式组织代码,这可以让代码更加简单、优雅。但是有些时候，缩进本身就是一个坑！<br/>
<strong>2.python安装(windows)</strong><br/>
linux 和 mac 已经安装好了python(所以争取暑假换mac)<br/>
<strong>3.python解释器</strong><br/>
主要还是Cpython,先占位,等以后弄懂了原理好好分析一下<br/>
<a href="https://github.com/python/cpython">源代码</a><br/>
<strong>4.第一个坑</strong><br/>
		
	#!/usr/bin/env python
	# -*- coding: utf-8 -*-
我接触python的第一个坑是字符编码,而且这个坑伴着我度过了新年,直到我换了windows的用户名(所以争取暑假换mac)<br/>
ok,关于字符编码:首先来张自己总结的图<br/>
![字符编码](http://7xj431.com1.z0.glb.clouddn.com/pic.png)
(不好意思:ASCII码可以视为utf-8编码的一部分,打错了.)<br/>
了解了字符编码,现在来看看python对字符编码的支持<br/>
1.python 与 ASCII<br/>
python最早支持的编码方式就是ASCII(因为那时只有ASCII。。)<br/>

	>>ord('A')
	65
	>>chr(65)
	'A'
2.python 与 unicode<br/>
python 比 unicode要大,python中采用 u"..."表示unicode字符串<br/>
	
	>>u"neo1218"
	u'neo1218'

3.python中字符编码相互转换问题<br/>
ASCII码可以视为utf-8的一部分,所以仅需讨论utf-8 与 unicode的转换<br/>

	>># 把unicode转换为utf-8编码
	>>u'neo1218'.encode('utf-8')
	'neo1218'
	>># 把utf-8转化为unicode编码
	>>'neo1218'.decode('utf-8')
	u'neo1218'
改变<br/>
utf-8 与 unicode 的转化似乎看上去没有什么改变,但是：<strong>我举的例子都是英文呀！！</strong>
	
	>>len("朱承浩")
	9
	>>len(u"朱承浩")
	3
也就是说一个<strong>unicode中文字符</strong>转化后会变成3个utf-8字符<br/>
<strong>4.坑在何方?<br/></strong>
所以要用utf-8 无 bom格式写代码,就是这样。<br/>
开头加上这句注释<code># -**- coding: utf-8 -*-</code><br/>
如果调用html文件则在调用前加上:

	#-------------------编码设置---------------------------
	import sys
	reload(sys)
	sys.setdefaultencoding('utf-8')
	#-----------------------------------------------------
