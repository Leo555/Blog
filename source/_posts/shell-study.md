---
title: Shell 学习
date: 2018-03-07 22:51:37
categories: Linux
tags:
- Shell
---

## Shell 变量

- 变量默认都是字符串类型
- 变量名和等号之间不能有空格
- 命名：只能使用英文字母，数字和下划线，首个字符不能以数字开头
- 查看变量 set 命令，删除变量 `unset variable_name`
- `set -u` 调用未声明变量报错（默认无提示）

### 变量叠加

```shell
x=123
x="$x"456
x=${x}789
echo $x # 123456789
```

<!--more-->

### Shell 字符串

Shell 字符串可以用单引号，也可以用双引号，也可以不用引号。

```shell
str='Hello World'
name='Jack'
str="Hello, ${name}"
str="Hello, "$name""
str="Hello, \"$name\"! "
```

其中双引号中可以出现变量和转义符。

```shell
string="abcd"
echo ${#string} # 获取字符串长度
```

提取子字符串
以下实例从字符串第 2 个字符开始截取 4 个字符：

```shell
string="Hello World"
echo ${string:1:4} # 输出 ello
```


## Shell 数组

Shell 中只支持一维数组

```shell
names=('leo' 'jack' 'tim')
names[3]='petter' # 可以不使用连续的下标，而且下标的范围没有限制
echo ${names[0]} # leo
echo ${names[@]} # 获取全部元素
echo ${#names[@]} # 获取数组长度
echo ${#names[*]} # 获取数组长度
echo ${#names[0]} # 获取第一个元素长度
```


## Shell 注释

Shell 没有多行注释

```shell
#--------------------------------------------
# 这是一个注释
# author：lizhen
# site：https://lz5z.com
# slogan：人生苦短，我再睡会
#--------------------------------------------
##### config start #####
#
#
# blabla
# 
#
##### config end  #####
```

# 未完待续