title: 'Python一些书写技巧'
date: 2016-11-13 21:36:55
tags:
    - Python
categories: Python
---
# 简介
本文介绍了一些平时用到的Python书写技巧。之后会不断更新。
<img src="/assets/img/python.png" alt="我是一只的图片" width="20%">
<!-- more -->

## 交换变量

```python
x = 6
y = 5
 
x, y = y, x
 
print(x, y) #5 6
```

## if 语句在行内

```python
print("Hello") if True else "World" #Hello
```

## 连接

```python
a = [1, 2]
b = [3, 4]
print(a + b) #[1, 2, 3, 4]
 
print(str(1) + " world") #1 world
 
print(`1` + " world") #1 world
 
print(1, "world") #1 world

print(a, 3) #[1, 2] 3
```

## 除法

```python
print(5.0//2) #2 地板除
print(2**5) #32 2的5次方

print(.3/.1) #2.9999999999999996
print(.3//.1) #2.0
```

## 数值比较
```python
x = 2
if 3 > x > 1:
   print(x) #2

if 1 < x > 0:
   print(x) #2
```

## 迭代列表

```python
names = ('Jack','Leo','Sony')
ages = (2001,2002,2003)
for a, n in zip(names, ages):
    print(a, n)
#Jack 2001
#Leo 2002
#Sony 2003

# 索引
for index, a in enumerate(names):
    print(index, a)
#0 Jack
#1 Leo
#2 Sony
```

## 列表推导式

已知一个列表，我们可以筛选出偶数列表方法：

```python
numbers = [1,2,3,4,5,6]
even = []
for number in numbers:
    if number%2 == 0:
        even.append(number)

#转变成如下：
even = [number for number in numbers if number%2 == 0]
```

## 字典推导

和列表推导类似，字典可以做同样的工作：

```python
names = ['Jack','Leo','Sony']
people = [{key: value for value, key in enumerate(names)}]
print(people)
>>> [{'Sony': 2, 'Leo': 1, 'Jack': 0}]
```

## 初始化列表的值

```python
items = [0]*3
print(items)
>>> [0,0,0]
```

## 列表转换为字符串

```
names = ["Leo", "Jack", "Lucy"]
print(", ".join(names))
>>> Leo, Jack, Lucy
```

## 从字典中获取元素

```python
data = {'user': 1, 'name': 'Max', 'age': 4}
is_admin = data.get('admin', False)
print(is_admin)
>>> False
```

## 切片

```python
x = [1,2,3,4,5,6]
#前3个
print(x[:3])
>>> [1,2,3]
#中间4个
print(x[1:5])
>>> [2,3,4,5]
#最后3个
print(x[-3:])
>>> [4,5,6]
#奇数项
print(x[::2])
>>> [1,3,5]
#偶数项
print(x[1::2])
>>> [2,4,6]
```

## 一行代码解决FizzBuzz

有一个简单的编程练习叫FizzBuzz，问题引用如下：

写一个程序，打印数字1到100，3的倍数打印“Fizz”来替换这个数，5的倍数打印“Buzz”，对于既是3的倍数又是5的倍数的数字打印“FizzBuzz”。

这里就是一个简短的，有意思的方法解决这个问题：
```python
for x in range(101):print("fizz"[x%3*4::]+"buzz"[x%5*4::]or x)
```

## 集合

除了python内置的数据类型外，在collection模块同样还包括一些特别的用例，在有些场合Counter非常实用。
```python
from collections import Counter
print(Counter("hello"))
>>> Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})
```

## 迭代工具

和collections库一样，还有一个库叫itertools，对某些问题真能高效地解决。其中一个用例是查找所有组合，他能告诉你在一个组中元素的所有不同的组合方式
```python
from itertools import combinations
names = ["Leo", "Jack", "Lucy"]
for name in combinations(names, 2):
    print(name)
>>> ('Leo', 'Jack')
>>> ('Leo', 'Lucy')
>>> ('Jack', 'Lucy')
```

## False == True

在Python中，True和False是全局变量，因此：
```python
False = True
if False:
   print("Hello")
else:
   print("World")
>>> Hello
```
