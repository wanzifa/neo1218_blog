title: "Windows下搭建github博客"
date: 2015-04-18 16:05:23
tags: 博客 文章
---
在本篇博客的开头，我要先说明几点：<br/>
1.注意标题，本文介绍的是在windows下搭建github博客，如果是mac请移步<a href="http://jinyixinseraph.github.io/2015/04/03/OS-X%E4%B8%8B%E6%90%AD%E5%BB%BAHexo/" target="_blank">OS X下搭建Hexo</a><br/>
2.如果你还不清楚github的话请参考<a href="https://zh.wikipedia.org/wiki/GitHub" target="_blank">github</a><br/>
3.在进入教程之前你要了解<a href="https://zh.wikipedia.org/wiki/Node.js" target="_blank">node.js</a>  知道概念就行<br/>
4.知道<a href="http://segmentfault.com/a/1190000000370778" target="_blank">hexo</a>是什么<br/>
如果你已经了解了以上概念，那么，我们开始吧！！！<br/>

步骤1.在github上创建博客仓库
---
博客仓库和其他仓库没有任何区别，只是仓库的命名是固定的—<code>用户名.github.io</code>,github会自动识别此用户名,你可以进入仓库点击侧栏的Settings，会发现这样一行文字"Your site is published at http://用户名.github.io. "，恭喜你，你已经完成了第一步！<br/>
步骤2.安装node.js
---
去node.js的<a href="https://nodejs.org/" target="_blank">官网</a>下载对应版本的node.js<br/>
下载、安装好了以后，在cmd中进入安装目录，输入node -V，如果返回路径结果，则安装成功！<br/>
步骤3.安装hexo
---
node.js安装成功后，安装hexo就是一件很容易的事啦，只要使用npm命令<br/>
<code>npm install -g hexo</code><br/>
步骤4.建立hexo文件夹
--
在你喜欢的盘符下建立hexo文件夹，然后用你的git终端进入此文件夹<br/>
1.初始化hexo文件夹<br/>
<code>hexo init</code><br/>
2.安装依赖包<br/>
<code>npm install</code><code><br/>
步骤5.部署至github
---
其实这也是我们建立github博客的主要原因—免费、无限流量。。<br/>
如果你成功搭建了你的博客,请千万把博客利用好，空间是有限的，免费不能浪费！<br/>
1.在你的git终端输入<code>npm install hexo-deployer-git --save</code><br/>
2.在你的hexo文件夹中修改_config.yml

	deploy:
  	type: git
  	repository: https://github.com/用户名/用户名.github.io.git
  	branch: master

注意":"后的空格！<br/>
3.从git终端进入hexo文件夹，输入<br/>
<code>hexo g</code><br/>
<code>hexo d</code><br/>
至此，你的博客就搭建好了！
如何写博客
---
写博客的步骤是固定的<br/>
每当你准备写博客的时候，只要从git终端进入hexo文件夹，输入<br/>
<code>hexo new "标题"</code><br/>
然后你会发现你的hexo/source/_post/下便出现了你新建的文章.<br/>
接下来就是书写博客了，hexo博客支持的是<a href="https://github.com/riku/Markdown-Syntax-CN" target="_blank">markdown语法</a>，建议安装一个支持markdown语法预览的编辑器，我用的是MarkdownPad.<br/>
ok,你所希望分享的都写完啦！接下来就是提交啦！可是你还是有点不放心，没事，输入<br/>
<code>hexo g</code><br/>
<code>hexo s</code><br/>
你就可以在localhost:4000/上看到啦，只有你能看到哦！<br/>
于是，激动的你就要提交你的第一篇博客啦！<br/>
<code>hexo g</code><br/>
<code>hexo d</code><br/>
over.......