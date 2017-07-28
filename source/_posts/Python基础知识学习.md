---
title: Python 基础知识学习
date: 2016-08-31 22:38:42
tags: 
- Python
categories: Python
---
<img src="/assets/img/Python_logo.png" alt="我是一只的图片">

# Python 数据类型
---
这里只列举一些Python与Java和JavaScript不一样的地方，如果你有任何语言基础，相信看完这篇文章就可以轻松写Python程序。
<!-- more -->

## 字符串 

Py字符串可以用单引号 **'...'**，双引号**"..."**，三引号 **'''...'''** 表示, 可以把单引号放在双引号里面。如下：

```python
>>> print("I'm OK") 
I'm OK

>>> print('I\'m OK') #使用转义字符
I'm OK

```
如果字符串里面有很多字符都需要转义，就需要加很多\，为了简化，Python还允许用r'...'表示'...'内部的字符串默认不转义

```python
>>> print('\\\\')
\\

>>> print(r'\\\\')
\\\\

```
如果字符串内部有很多换行，用\n写在一行里不好阅读，为了简化，Python允许用'''...'''的格式表示多行内容

```python
>>> print('''Hello
... World!
... I'm Leo!''')

Hello
World!
I'm Leo!
```
注意这里的 **'**没有使用转义字符也能打印出来，不过安全起见，可以写成如下形式：

```python
>>> print(r'''Hello
... World!
... I'm Leo!''')

Hello
World!
I'm Leo!
```
表示既能识别换行，又能默认不转义。这个用处大大地，可以做一些多行文本的处理，如果有保留内容样式的需求，也能够很好地满足。

### 字符串格式化
在Python中，采用的格式化方式和C语言是一致的，用%实现

```python
>>> 'Hello, %s' % 'world'
'Hello, world'

>>> 'Hello, %s, %d time' % ('world', 3)
'Hello, world, 3 time'

```
在字符串内部，%s表示用字符串替换，%d表示用整数替换，有几个%?占位符，后面就跟几个变量或者值，顺序要对应好。如果只有一个%?，括号可以省略。

常见的占位符有：
%d——整数 
%f——浮点数
%s——字符串
%x——十六进制整数

格式化整数和浮点数还可以指定是否补0和整数与小数的位数

```python
>>> '%2d - %02d' % (2,1)
' 2 - 01'

>>> '%2.f' % 3.14
' 3'

>>> '%.2f' % 3.1415
'3.14'
```
如果你不太确定应该用什么，%s永远起作用，它会把任何数据类型转换为字符串：

```python
>>> 'Age: %s. Gender: %s' % (25, True)
'Age: 25. Gender: True'
```
如果字符串里面的%是一个普通字符怎么办？这个时候就需要转义，用%%来表示一个%

```python
>>> 'growth rate: %d %%' % 7
'growth rate: 7 %'
```

## 布尔值
布尔值与JavaScript和Java的区别就是 **True** 和 **False** 开头大写，除此之外，逻辑运算是用 and, or和not进行运算。暂时只知道这点区别。

```python
>>> age=1
>>> if age >= 18:
...     print('adult')
... else:
...     print('teenager')
...
teenager
```

## 空值
Py里面的空值用 **None** 表示，逻辑运算时，None相当于False

```python
>>> None==None
True
>>> if(not None):
...     print('Leo')
...
Leo
>>> not None
True
```

## 变量
Python中变量名必须是大小写英文、数字和 _ 的组合，且不能用数字开头。
Py定义一个变量异常简单，只需要写变量名 =XX 即可。由于Py是动态语言，所以变量的数据类型可以随意切换。

## 常量
在Java中一般使用final关键字定义常量, final常量一般在声明的同时赋初值，也可以在构造函数中赋初值，为了节省内存空间，我们常将变量声明为静态的(static)

```Java
static final double PI=3.1415926;
```
在JavaScript中，ES6标准也增加了对常量的支持，使用const关键字

```javascript
const MY_FAV = 7;
```
Python中没有真正意义的常量，不过如果你见到全部用大写字母表示的值，最好谨慎一些。

```python
PI = 3.14159265359
```
## 计算
Py中有两种除法，一种是浮点除法，一种是整除。
浮点除法 **/** 无论是否整除结果都是浮点数。

```python
>>> 10/3
3.3333333333333335
```
还有一种除法是//，称为地板除，两个整数的除法永远是整数，就像Java一样。

```python
>>> 10//3
3
```

## 数据类型转换

```python
>>> int('123')
123
>>> int(12.34)
12
>>> float('12.34')
12.34
>>> str(1.23)
'1.23'
>>> str(100)
'100'
>>> bool(1)
True
>>> bool('')
False

```

## list
list是一种有序的集合，可以随时添加和删除其中的元素。

```python
>>> students=[1,'xiao',True]
>>> len(students)
3
>>> students[0]
1
>>> students[2]
True

>>> students[3]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range

```
当索引超出了范围时，Python会报一个IndexError错误
如果要取最后一个元素，除了计算索引位置(len()-1)外，还可以用-1做索引，直接获取最后一个元素

```python
>>> students[-1]
True
```
常用操作有： append(), insert(index, value), pop(), pop(index), 

```python
>>> students.append('Leo') #追加一个元素
>>> students
[1, 'xiao', True, 'Leo']

>>> students.insert(2, False) #插入一个元素
>>> students
[1, 'xiao', False, True, 'Leo']

>>> students.pop() #删除末尾元素
'Leo'
>>> students
[1, 'xiao', False, True]
```

## tuple

中文名叫做元组，tuple也是有序列表，tuple初始化后就不能修改，使用起来更加安全。

```python
>>> names=('Jack', 'Lucy', 'Leo') #tuple定义的时候元素就必须确定下来
>>> names 
('Jack', 'Lucy', 'Leo')

>>> names=(True,) #如果只有一个元素, 要与小括号进行区分
>>> names
(True,)          #Python在显示只有1个元素的tuple时，也会加一个逗号

>>> t=() #定义一个空的tuple
>>> t
()
```
值得注意的是tuple所谓的不变，指的是每个元素的指向不变，如果指向的的对象发生了改变，tuple也是可变的。例如：

```python
>>> t = ('a', 'b', ['A', 'B'])
>>> t[2][0] = 'X'
>>> t[2][1] = 'Y'
>>> t
('a', 'b', ['X', 'Y'])
```

# 条件判断

## 写一个sample就什么都明白了

```python
age = 16
if age >= 18:
    print('adult')
elif age >= 6:
    print('teenager')
else:
    print('kid')
```

elif 是else if的缩写

```python
if x:
    print('True')
```
只要x是非零数值、非空字符串、非空list等，就判断为True，否则为False

## input
使用input可以获取用户的输入

```python
>>> age=input()
21
>>> age
'21'

```
不过可以看出input获取的值为字符串，所以可以使用int(age)进行数据类型转换

# 循环

## for in循环
for...in循环依次把list或tuple中的每个元素迭代出来, 并且代入变量，然后执行缩进块的语句。

```python
>>> for x in range(3):
...     print(x)
...
0
1
2

```
range() 可以生产一个整数序列, 通过list()函数可以转换为list。比如range(5)生成的序列是从0开始小于5的整数,
range(2, 4)生产序列从2开始，小于4的整数。

```python
>>> range(3)
range(0, 3)

>>> list(range(3))
[0, 1, 2]

>>> list(range(2,4))
[2, 3]

```


## while循环
while循环与Java和JS几乎没有什么区别，只是格式有点不一样

```python
sum = 0
n = 99
while n > 0:
    sum = sum + n
    n = n - 2
print(sum)
```

# dict和set

## dict

Python中的dict就是字典，相当于JavaScript和Java中的对象或者map。
总体来说，Python dict的使用方法与JavaScript对象相似。
我们首先来看一下如何定义一个Python字典

```python
>>> ages={'Leo':20,'Jack':25,'Lucy':34}
>>> ages
{'Leo': 20, 'Lucy': 34, 'Jack': 25}
>>> ages['Leo']
20

```
dict的优点是查找速度快，想象一下，你通过字典去查一个字，是不是先通过拼音或者偏旁找到这个字所在的页数，然后直接翻到这一页。所以无论找哪个字，这种查找速度都非常快，不会随着字典大小的增加而变慢。这就是dict的优势所在。

如果key不存在Python会报错   

```python
>>> ages['Pig']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'Pig'
```

可以通过in判断key是否存在

```python
>>> 'Leo' in ages
True

```

通过get获取key对应的value，如果key不存在，返回None。也可以自己指定key不存在时候的返回值。

```python
>>> ages.get('Lucy')
34
>>> ages.get('Lu')
>>> ages.get('Lu', 30)
30

```

和list比较，dict有以下几个特点：

1. 查找和插入的速度极快，不会随着key的增加而变慢；
2. 需要占用大量的内存，内存浪费多。

而list相反：

1. 查找和插入的时间随着元素的增加而增加；
2. 占用空间小，浪费内存很少。

所以，dict是用空间来换取时间的一种方法。


## set

set是一个没有重复元素的集合，这点和Java、JavaScript一样。用法也非常相近

```python
>>> s = set([1, 1, 2, 2, 3, 3])
>>> s
{1, 2, 3}

>>> s.add(4)
>>> s
{1, 2, 3, 4}

>>> s.remove(4)
>>> s
{1, 2, 3}

```
Python中的set可以做交集和并集,这点就比较强大了

```python
>>> s1 = set([1, 2, 3])
>>> s2 = set([2, 3, 4])
>>> s1 & s2
{2, 3}
>>> s1 | s2
{1, 2, 3, 4}

```

# 函数

## 内置函数

Python提供了很多内置函数，并且有详细的文档可以参考，地址：
[https://docs.python.org/3/library/functions.html](https://docs.python.org/3/library/functions.html)
后面会写一个内置函数讲解的的blog，敬请期待

## 定义函数

Python使用def定义一个函数

```python
def  my_abs(x):
    if x >= 0:
        return x
    else:
        return -x
```
1. 函数如果没有return语句，默认返回None
2. return None = return
3. 通过from ...(文件名) import ...(函数名)导入函数
4. 函数中还可以使用pass，表示什么都不做
5. 函数可以返回多值（tuple）

```python
>>> def cal(x, y):
...     add = x + y
...     sub = x - y
...     return add,sub
...
>>> a1, a2 = (5, 3)
>>> a1
5
>>> a1, a2
(5, 3)
```

## 参数

Python函数的参数相较Java和JavaScript强大很多，除了正常定义的必选参数外，还可以使用默认参数、可变参数和关键字参数，使得函数定义出来的接口，不但能处理复杂的参数，还可以简化调用者的代码。

### 默认参数

```python
def power(x, n=2):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s
power(5) #25

power(5, 2) #25

power(5, n=3) # 125
```

定义默认参数要牢记一点：默认参数必须指向不变对象！
这是为什么呢？我们举一个例子：

```python
def test(lang=[]):
  lang.append('python')
  return lang
```
当老实调用时，结果如你所愿

```python
print(test(['js','go']))  #['js', 'go', 'python']
print(test(['c','java']))  #['c', 'java', 'python']
```
但是如果多次使用默认参数调用时

```python
print(test())  #['python']
print(test())  #['python', 'python']
```
分析：
函数在定义的时候，默认参数lang的值就已经声明了，即空的 [],也就是说 默认参数 指向对象 [],在多次调用默认参数的情况下，就改变了默认参数指向对象的数据，默认参数 指向对象的数据变了，下次再调用时，默认参数已经变了，而不再是你希望的空的[]

为了便于理解等同下面这段：

```python
temp = []
def test(lang=temp):
  lang.append('python')
  return lang
```

重新修改代码：

```python
def test(lang=None):
  if lang is None:
    lang = []
  lang.append('python')
  return lang
```

总结：
定义函数默认参数时，函数默认参数必须指向不变对象，建议使用 None，str 这些不可变对象处理



### 可变参数

可变参数就是传入的参数个数是可变的，可以是1个、2个到任意个，还可以是0个。

假如要定义一个求和函数，传入参数个数不可知，用一般的方式定义

```python
def sum(numbers):
    sum = 0
    for n in numbers:
        sum = sum +n
    return sum
```

但是调用的时候，需要先组装出一个list或tuple：

```python
sum([1,2,3]) #6
sum((1,2,3)) #6
```

使用可变参数定义：

```python
def sum(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n
    return sum
```

调用的时候就可以传入任意参数了

```python
sum(1,2,3) #6
```

### 关键字参数

可变参数允许你传入0个或任意个参数，这些可变参数在函数调用时自动组装为一个tuple。而关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict。

```python
def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)
```

函数person除了必选参数name和age外，还接受关键字参数kw。在调用该函数时，可以只传入必选参数,也可以传入任意个数的关键字参数。

```python
person('Leo', 18)  #name: Leo age: 18 other: {}
person('Bob', 35, city='Beijing')  #name: Bob age: 35 other: {'city': 'Beijing'}
person('Adam', 45, gender='M', job='Engineer')   #name: Adam age: 45 other: {'gender': 'M', 'job': 'Engineer'}
```

---

