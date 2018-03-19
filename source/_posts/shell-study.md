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

### readonly

```shell
x=123
readonly x
x=312 #-bash: a: readonly variable
```

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

查找字符串

```shell
string="Hello World"
echo `expr index "$string" llo` # 3
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

## Shell 参数

创建脚本 `test.sh`

```shell
#!/bin/bash
# author:lizhen

echo "Shell 传递参数";
echo "执行的文件名：$0";
echo "第一个参数为：$1";
echo "第二个参数为：$2";
echo "第三个参数为：$3";
echo "参数个数：$#";
echo "参数字符串：$*";
echo "所有参数：$@";
echo "进程ID号: $$";
```

为脚本设置执行权限，并执行

```shell
chmod +x test.sh
./test.sh 1 2 4

# Shell 传递参数
# 执行的文件名：./test.sh
# 第一个参数为：1
# 第二个参数为：2
# 第三个参数为：3
# 参数个数：4
# 参数字符串：1 2 3 4
# 所有参数：1 2 3 4
# 进程ID号: 27694
```

## Shell 运算符

原生 bash 不支持数学运算符，但是可以通过其他命令实现，比如 expr。

### 算术运算符

```shell
val=`expr 2 + 2` # 注意空格
echo val # 4
echo `expr 2 - 2` # 0
echo `expr 2 \* 2` # 4 # 乘号前面必须要有反斜杠
echo `expr 2 / 2` # 1
echo `expr 3 % 2` # 1
echo `expr 2 == 2` # 1
echo `expr 2 != 2` # 0
```

### 关系运算符

```shell
[ $a -eq $b ] # -eq 相等
[ $a -ne $b ] # -ne 不等
[ $a -gt $b ] # -gt 大于
[ $a -lt $b ] # -lt 小于
[ $a -ge $b ] # -ge 大于等于
[ $a -le $b ] # -le 小于等于
```

```shell
a=$1
b=$2
echo $a
echo $b
if [ $a -eq $b ]
then
   echo "$a -eq $b : a 等于 b"
else
   echo "$a -eq $b: a 不等于 b"
fi
```

```shell
./test.sh 10 20
# 10 
# 20
# "10 -eq 20: a 不等于 b"
```

### 布尔运算符

```shell
#!/bin/bash
# author:lizhen

a=10
b=20

# 非运算 !
if [ $a != $b ]
then
   echo "$a != $b : a 不等于 b"
else
   echo "$a != $b: a 等于 b"
fi

# 或运算 -o
if [ $a -lt 100 -o $b -gt 100 ]
then
   echo "$a 小于 100 或 $b 大于 100 : true"
else
   echo "$a 小于 100 或 $b 大于 100 : false"
fi

# 与运算 -a
if [ $a -lt 100 -a $b -gt 15 ]
then
   echo "$a 小于 100 且 $b 大于 15 : true"
else
   echo "$a 小于 100 且 $b 大于 15 : false"
fi
```

### 逻辑运算符

```shell
a=10
b=20
# 逻辑AND &&
if [[ $a -lt 100 && $b -gt 100 ]]
then
   echo "true"
else
   echo "false"
fi

# 逻辑OR ||
if [[ $a -lt 100 || $b -gt 100 ]]
then
   echo "true"
else
   echo "false"
fi
```

### 字符串运算符

```shell
a="abc"
b="cde"
[ $a = $b ] # 字符串相等
[ $a != $b ] # 字符串不等
[ -z $a ] # 字符串长度为0
[ -n $a ] # 字符串长度不为0
[ $a ] # 字符串不为空
```

## echo 命令

```shell
echo "\"Are you OK?\"" # 转义字符
echo "$a" # 变量
echo -e "I\'m \nOK" # -e 开启转义
echo -e "I\'m OK \c" # -e 开启转义 \c 不换行
echo "Are you OK?" > tesh.sh # 显示结果到文件
echo '$a\"' # $a\" # 原样输出字符串，不转义不去变量 单引号
echo `date` # 显示时间
```

## printf 命令

```shell
# printf format-string [arguments...]

printf "%-10s %-8s %-4s\n" 姓名 性别 体重kg  
printf "%-10s %-8s %-4.2f\n" 郭靖 男 66.1234 
printf "%-10s %-8s %-4.2f\n" 杨过 男 48.6543 
printf "%-10s %-8s %-4.2f\n" 郭芙 女 47.9876 
```

%s %c %d %f都是格式替代符

%-10s 指一个宽度为10个字符（-表示左对齐，没有则表示右对齐），任何字符都会被显示在10个字符宽的字符内，如果不足则自动以空格填充，超过也会将内容全部显示出来。

%-4.2f 指格式化为小数，其中.2指保留2位小数。

## test 命令

test 命令用于检查某个条件是否成立，它可以进行数值、字符和文件三个方面的测试。

### 数值测试

```shell
a=10
b=20
if test $[a] -eq $[b] # 如果 a 等于 b
then
  echo "$a 等于 $b"
else
  echo "$a 不等于 $b"
fi
```

代码中的 [] 表示执行基本的算数运算。

```shell
a=10
b=10
echo "$[a+b]" # 20 # 不能有空格
```

### 字符串测试

```shell
a="abc"
b="ABC"
if test $a = $b
then 
  echo "字符串相等"
else 
  echo "字符串不等"
fi    
```

### 文件测试

```shell
# -e 文件名  如果文件存在则为真
# -r 文件名  如果文件存在且可读则为真
# -w 文件名  如果文件存在且可写则为真
# -x 文件名  如果文件存在且可执行则为真
# -s 文件名  如果文件存在且至少有一个字符则为真
# -d 文件名  如果文件存在且为目录则为真
# -f 文件名  如果文件存在且为普通文件则为真
# -c 文件名  如果文件存在且为字符型特殊文件则为真
# -b 文件名  如果文件存在且为块特殊文件则为真

if test -e ./test.sh
then 
  echo "test.sh 文件存在"
else
  echo "文件不存在"
fi
```

## Shell 流程控制

### 条件控制

```shell
# if 
if condition
then 
  command1
  command2
  ...
  commandN
fi  

# if else-if else
if condition1
then
    command1
elif condition2 
then 
    command2
else
    commandN
fi
```

### for 循环

```shell
for var in item1 item2 ... itemN
do
    command1
    command2
    ...
    commandN
done

# for 循环
for var in item1 item2 ... itemN; do command1; command2… done;
# for 循环
for loop in 1 2 3 4 5
do
    echo "The value is: $loop"
done
```

### while 循环

```shell
while condition
do 
  command
done
# while 循环
int=1
while(( $int<=5 ))
do
  echo $int
  let "int++"
done
```

### 无限循环

```shell
while true
do 
  command
done
```


### case

```shell
case 值 in
模式1)
    command1
    command2
    ...
    commandN
    ;;
模式2）
    command1
    command2
    ...
    commandN
    ;;
esac

# case
echo '输入 1 到 4 之间的数字:'
echo '你输入的数字为:'
read aNum
case $aNum in
    1)  echo '你选择了 1'
    ;;
    2)  echo '你选择了 2'
    ;;
    3)  echo '你选择了 3'
    ;;
    4)  echo '你选择了 4'
    ;;
    *)  echo '你没有输入 1 到 4 之间的数字'
    ;;
esac
```

case工作方式如上所示。取值后面必须为单词in，每一模式必须以右括号结束。取值可以为变量或常数。匹配发现取值符合某一模式后，其间所有命令开始执行直至 ;;。

取值将检测匹配的每一个模式。一旦模式匹配，则执行完匹配模式相应命令后不再继续其他模式。如果无一匹配模式，使用星号 * 捕获该值，再执行后面的命令。

### break

```shell
while :
do
    echo -n "输入 1 到 5 之间的数字:"
    read aNum
    case $aNum in
        1|2|3|4|5) echo "你输入的数字为 $aNum!"
        ;;
        *) echo "你输入的数字不是 1 到 5 之间的! 游戏结束"
            break
        ;;
    esac
done
```

### continue

```shell
while :
do
    echo -n "输入 1 到 5 之间的数字: "
    read aNum
    case $aNum in
        1|2|3|4|5) echo "你输入的数字为 $aNum!"
        ;;
        *) echo "你输入的数字不是 1 到 5 之间的!"
            continue
            echo "游戏结束"
        ;;
    esac
done
```

esac
case的语法和C family语言差别很大，它需要一个esac（就是case反过来）作为结束标记，每个case分支用右圆括号，用两个分号表示break。

## Shell 函数

```shell
funWithReturn(){
    echo "输入的两个数字进行相加运算..."
    echo "输入第一个数字: "
    read aNum
    echo "输入第二个数字: "
    read anotherNum
    echo "两个数字分别为 $aNum 和 $anotherNum !"
    return $(($aNum+$anotherNum))
}
funWithReturn
echo "输入的两个数字之和为 $? !"
```

函数返回值在调用该函数后通过 $? 来获得。
注意：所有函数在使用前必须定义。这意味着必须将函数放在脚本开始部分，直至shell解释器首次发现它时，才可以使用。调用函数仅使用其函数名即可。

### 函数参数

```shell
funWithParam(){
    echo "第一个参数为 $1 !"
    echo "第二个参数为 $2 !"
    echo "第十个参数为 $10 !"
    echo "第十个参数为 ${10} !"
    echo "第十一个参数为 ${11} !"
    echo "参数总数有 $# 个!"
    echo "作为一个字符串输出所有参数 $* !"
}
funWithParam 1 2 3 4 5 6 7 8 9 34 73
```

## Shell 重定向

```shell
command > file # 将输出重定向到 file
command < file # 将输入重定向到 file
command >> file # 将输出以追加的方式重定向到 file
```
