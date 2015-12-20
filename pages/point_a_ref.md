title: 引用和指针的实验
date: 2015-12-20 20:30:30

## 程序1 point.cpp

    # include <iostream>
    using namespace std;

    int main()
    {
        int var = 42;
        int* p = &var;
        return 0;
    }


## 程序2 refer.cpp

    # include <iostream>
    using namespace std;

    int main()
    {
        int var = 42;
        int& p = var;
        return 0;
    }

## 编译

    g++ point.cpp -o point
    g++ refer.cpp -o refer

## 反编译

    gobjdump -S point > test1
    gobjdump -S refer > test2

## 比较

    vimdiff test1 test2

## 结果
![result](http://7xj431.com1.z0.glb.clouddn.com/prpng)

## 结论

引用就是指针(常量指针)
