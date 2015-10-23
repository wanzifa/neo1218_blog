title: "python 学习笔记(day 2)"
date: 2015-06-10 00:08:06
tags: 博客 python
---
今天的主题是python的内存管理<br/>
![内存](http://7xj431.com1.z0.glb.clouddn.com/image.jpg)<br/>
python的特性: 动态语言,面向对象，python的内存管理也很有特点,用一句话概括
<strong>基于对象和引用</strong><br/>
<strong>1.对象的内存使用</strong><br/>
<ciode>a = 1</code><br/>
这是一个最简单的赋值语句,但是可不要小看它,它包含了python绝妙的设计哲学,
在python中万物皆为对象,1也不例外,通过赋值语句,我们创建了一个指向1 这个
对象的引用。python通过引用控制对象,引用与对象的分离使得引用对于对象的入侵性
减少。<br/>
为了更好的探明对象在内存中的存储,我们借助<strong>id()</strong>函数<br/>

    >>a = 1
    >>id(a)
    7431496L

可见,我们创建一个对象时,系统就自动为这个对象分配了内存空间<br/>
在python中，python会缓存整数、短字符串,这些缓存的对象在重复创建时不会建立新
的引用<br/>

    >>b = 1
    >>id(b)
    7431496L

可见这里的b和a指向的是同一个对象<br/>
我们还可以使用is关键字判断两个引用是否是同一个引用<br/>

    >>a is b
    True

<strong>在python中,每个对象都存有指向这个对象的引用总数:引用计数</strong><br/>
我们可以使用sys包中的<strong>getrefcount()</strong>函数查看某个对象的引用计数(注意调用函数时也是一次引用)

    >>from sys import getrefcount
    >>getrefcount(1)
    3
    >># 作为函数参数时被引用了一次


<strong>2.对象引用对象</strong><br/>
所谓对象引用对象即python的容器对象引用基本对象,但是这种引用并不是真正的包含
元素对象本身,而是指向各个元素对象的引用(类似C中的指针)<br/>
我们可以自定义一个对象,并引用其他对象

    >>class from_obj(object):
    >>...  def __init__(self,to_obj):
    >>...    self.to_obj = to_obj
    >>a = from_obj(b)
    >>id(a.to_obj)
    >>35023112
    >>id(b)
    >>35023112

这里的a的确引用了b<br/>
再看赋值:<code>a = 1</code><br/>
对象引用对象是python最基本的构成方式,赋值语句也是对象引用对象的体现
这里的a不仅仅是引用,他还是一个字典,用以存放赋值语句的键值对!<br/>
其实这涉及到python namespace的问题,我们下一讲重点复习(预习...)<br/>
容器对象的引用可以形成很复杂的拓扑结构,我们可以用objgraph包绘制这种关系<br/>

    x = [1,2,3]
    y = [x,dict(key1=x)
    z = [y,(x,y)]

    import objgraph
    objgraph.show_refs([z],filename='refs.png')
![图](http://7xj431.com1.z0.glb.clouddn.com/361A.tmp.png)<br/>
两个对象可以互相引用构成引用环<br/>
<code>a = []</code><br/>
<code>b = [a]</code><br/>
<code>a.append(b)</code><br/>
![双引用](http://7xj431.com1.z0.glb.clouddn.com/1F2B.tmp.png)<br/>
单个对象自己引用自己时也可以构成引用环<br/>
<code>a = []</code><br/>
<code>a.append(a)</code><br/>
![单引用](http://7xj431.com1.z0.glb.clouddn.com/200C.tmp.png)<br/>


<strong>3.引用减少</strong><br/>
当我们不在需要一个对象时,他的引用计数是如何减少的呢？<br/>
1.del删除对象<br/>
我们可以通过del删除某个对象从而减少对这个对象的引用<br/>

    from sys import getrefcount
    a = 1
    b = a
    print getrefcount(b)
    del a
    print getrefcount(b)

    #122
    #121

del 也可以用删除容器中的对象<br/>

    >>lit = [1,2,3,4]
    >>del lit[2]
    >>lit
    [1,2,4]

2.引用对象改变从而减少引用计数<br/>

    >>from sys import getrefcount
    >>a = [1,2,3]
    >>b = a
    >>b
    [1,2,3]
    >>getrefcount(b)
    4
    >>a = 1
    >>b
    [1,2,3]
    >>getrefcount(b)
    3

<strong>4.垃圾回收</strong><br/>
python 的垃圾回收是自动的,当对象的引用计数为0时,会自动开启垃圾回收,
当对象的数目达到某个阈值时,python也会自动清除没有用的对象。python的垃圾
回收并不是完全对coder封闭的,我们可以使用gc模块的get_threshold()函数查看
这个阈值<br/>

    import gc
    print(gc.get_threshold())
    # （700，10，10）

这里的700就是垃圾回收的阈值,我们可以通过set_threshold()函数设置阈值<br/>
我们还可以手动启动垃圾回收: gc.collect()<br/>

<strong>5.分代回收</strong><br/>
分代回收就很有意思啦,python中的对象也是有三六九等的:)寿命越长的对象
python就会越信任他,也就不会清除他。python中的对象分为三等：0，1，2.0是
新建对象,1是第一轮扫描存活下的对象，2则是第二轮扫描存活下来的对象。还记得之前的阈值
吗？（700，10，10）就表示每10次扫描0代对象就会扫描一次1代对象,每10次扫描1代对象
就会扫描一次2代对象,哈哈:)<br/>

<strong>6.孤立的引用环</strong><br/>
还记的之前的引用环吗？他会对垃圾回收机制带来很大的麻烦！

    a = []
    b = [a]
    a = b.append(b)

    del a
    del b

由于引用环的存在,a,b的引用计数不会降为0,所以python就不会回收这两个变量<br/>
当然python也有他的解决办法,他会遍历所有的变量并将该变量引用的变量的引用计数减一,最后将引用计数为0的
变量回收<br/>
ok,就是这些啦,虽然有点小麻烦,但在绝大多数情况下,程序员是不需要亲自操作内存的
，这比C语言好多啦:)
