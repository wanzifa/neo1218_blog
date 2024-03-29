title: python尾递归优化
date: 2015-09-05 18:55:32
tags: python小记
img: http://7xj431.com1.z0.glb.clouddn.com/2kWVh9jrFWU.jpg

## 一般递归与尾递归
#### 一般递归:

    def normal_recursion(n):
        if n == 1:
            return 1
        else:
            return n + normal_recursion(n-1)

执行：

    normal_recursion(5)
    5 + normal_recursion(4)
    5 + 4 + normal_recursion(3)
    5 + 4 + 3 + normal_recursion(2)
    5 + 4 + 3 + 2 + normal_recursion(1)
    5 + 4 + 3 + 2 + 1
    15

<strong>一般递归</strong>的效率是比较低的，因为在<code>return n + normal_recursion(n-1)</code>时需要
调用栈保存中间变量n的值，递归进行的越深入，需要调用的栈就越多，效率也就越低。<br/>

#### 尾递归
如果可以将中间变量作为参数直接传递给递归调用函数，那么可以大大提高递归效率，这就是尾递归
的实现

    def tail_recursion(n, total=0):
        if n == 0:
            return total
        else:
            return tail_recursion(n-1, total+n)

执行：

    tail_recursion(5)
    tail_recursion(4, 5)
    tail_recursion(3, 9)
    tail_recursion(2, 12)
    tail_recursion(1, 14)
    tail_recursion(0, 15)
    15

## 存在的问题
python 本身对尾递归的支持不太好，当递归深度超过1000时会报错

    RuntimeError: maximum recursion depth exceeded

## 一个牛人想出的解决办法：
#### 实现一个 tail_call_optimized 装饰器

    #!/usr/bin/env python2.4
    # This program shows off a python decorator(
    # which implements tail call optimization. It
    # does this by throwing an exception if it is
    # it's own grandparent, and catching such
    # exceptions to recall the stack.
    # 抛出异常，捕获异常，重新调用栈...牛

    import sys

    class TailRecurseException:
        """尾递归异常类"""
        def __init__(self, args, kwargs):
            self.args = args
            self.kwargs = kwargs

    def tail_call_optimized(g):
        """
        This function decorates a function with tail call
        optimization. It does this by throwing an exception
        if it is it's own grandparent, and catching such
        exceptions to fake the tail call optimization.

        This function fails if the decorated
        function recurses in a non-tail context.
        """
        def func(*args, **kwargs):
            f = sys._getframe()
            if f.f_back and f.f_back.f_back \
                and f.f_back.f_back.f_code == f.f_code:
                # 抛出异常
                raise TailRecurseException(args, kwargs)
            else:
                while 1:
                    try:
                        return g(*args, **kwargs)
                    except TailRecurseException, e:
                        # 捕获异常，重新调用栈
                        args = e.args
                        kwargs = e.kwargs
        func.__doc__ = g.__doc__
        return func

    @tail_call_optimized
    def factorial(n, acc=1):
        "calculate a factorial"
        if n == 0:
            return acc
        return factorial(n-1, n*acc)

    print factorial(10000)
    # prints a big, big number,
    # but doesn't hit the recursion limit.

    @tail_call_optimized
    def fib(i, current = 0, next = 1):
        if i == 0:
            return current
        else:
            return fib(i - 1, next, current + next)

    print fib(10000)
    # also prints a big number,
    # but doesn't hit the recursion limit.


作者的基本思想就是当尾递归达到最大深度时自己抛出一个异常(TailRecurseException), 然后
捕获这个异常，然后重新调用栈，而不是让异常终止尾递归的运行。<br/>

这里解释一下 sys._getframe() 函数:<br/>

    sys.getframe([depth]):
    Return a frame object from the call stack. If optional integer depth is given, return the frame object that many calls below the top of the stack. If that is deeper than the call stack, ValueError is raised. The default for depth is zero, returning the frame at the top of the call stack.

    即返回depth深度调用的栈帧对象.

    import sys

    def get_cur_info():
        print sys._getframe().f_code.co_filename  # 当前文件名
        print sys._getframe().f_code.co_name  # 当前函数名
        print sys._getframe().f_lineno # 当前行号
        print sys._getframe().f_back # 调用者的帧

## 参考
http://www.cnblogs.com/hello--the-world/archive/2012/07/19/2599003.html<br/>
http://www.chinaz.com/program/2013/0917/318157_2.shtml
