title: Difference between ++*p, *p++, and *++p
date: 2015-09-24 18:50:00
tags: C&C++
---

## 猜猜这些代码的输出结果吧!
program1

    # include <iostream>
    using namespace std;

    int main(void)
    {
        int arr[] = {10, 20};  // 定义并初始化了一个数组
        int *p = arr;  // 定义一个指针指向这个数组
        ++*p;
        cout << "arr[0]=" << arr[0] << " arr[1]=" << arr[1] << " *p=" << *p << endl;
        return 0;
    }

program2

    # include <iostream>
    using namespace std;

    int main(void)
    {
        int arr[] = {10, 20};  // 定义并初始化了一个数组
        int *p = arr;  // 定义一个指针指向这个数组
        *p++;
        cout << "arr[0]=" << arr[0] << " arr[1]=" << arr[1] << " *p=" << *p << endl;
        return 0;
    }

program3

    # include <iostream>
    using namespace std;

    int main(void)
    {
        int arr[] = {10, 20};  // 定义并初始化了一个数组
        int *p = arr;  // 定义一个指针指向这个数组
        *++p;
        cout << "arr[0]=" << arr[0] << " arr[1]=" << arr[1] << " *p=" << *p << endl;
        return 0;
    }


## 如何计算？
只要遵循下面这两个原则，判断就很简单了

    1. ++p 的优先级和 *p 是一样的, 都具有右结合性
    2. p++ 的优先级高于 ++p 和 *p, 具有左结合性


## 猜对了吗?
program1输出:

    arr[0]=10 arr[1]=20 *p=11

program2输出:

    arr[0]=10 arr[1]=20 *p=20

program3输出:

    arr[0]=10 arr[1]=20 *p=20


## 总结

    虽然这篇博客很短，但是很好的总结了自增自减运算符和*运算符的优先级关系

## 参考
[原文(英文)](www.geeksforgeeks.org/difference-between-p-p-and-p/) <br/>
