---
title: scala 学习笔记
date: 2016-10-02 19:28:00
tags: 
- scala
- Spark
categories: Big Data
---

<img src="/assets/img/scala.png" alt="我是一只的图片" width="20%">

# 安装Scala

到Scala官方下载地址下载：[http://scala-lang.org/download/](http://scala-lang.org/download/)

```
$ wget -c http://downloads.lightbend.com/scala/2.11.8/scala-2.11.8.tgz
$ tar zxf scala-2.11.8.tgz
$ cd scala-2.11.8
$ ./bin/scala
Welcome to Scala version 2.11.8 (Java HotSpot(TM) 64-Bit Server VM, Java 1.8.0_60).
Type in expressions to have them evaluated.
Type :help for more information.
scala>
```
<!-- more -->
## RELP

刚才我们已经启动了Scala RELP，它是一个基于命令行的交互式编程环境。我们可以在RELP中做一些代码尝试而不用启动IDE，这在我们思考问题时非常的方便。对于Java有一个好消息，JDK 9干始将内建支持RELP功能。

Scala是一个面向对象的函数式特性编程语言，它继承了Java的面向对特性，同时又从Haskell等其它语言那里吸收了很多函数式特性并做了增强。


## 环境变量

将scala文件夹移入平时装软件的地方，我常用的地方是 **/usr/local**, 重命名为scala，并打开bashrc文件配置环境变量。

```
$ sudo mv scala-2.11.8 /usr/local/scala
$ sudo gedit ~/.bashrc  
```

将scala配入环境变量

```
export SCALA_HOME=/usr/local/scala
export PATH=${SCALA_HOME}/bin:$PATH
```


# 变量、基础数据类型

Scala中变量不需要显示指定类型，但需要提前声明。这可以避免很多命名空间污染问题。Scala有一个很强大的类型自动推导功能，它可以根据右值及上下文自动推导出变量的类型。你可以通过如下方式来直接声明并赋值。

```
scala> val a = 1
a: Int = 1

scala> val b = true
b: Boolean = true

scala> val c = 1.0
c: Double = 1.0

scala> val a = 30 + "岁"
a: String = 30岁
```

### Immutable


函数式编程有一个很重要的特性：不可变性。Scala中除了变量的不可变性，它还定义了一套不可变集合scala.collection.immutable

val代表这是一个final variable，它是一个常量。定义后就不可以改变，相应的，使用var定义的就是平常所见的变量了，是可以改变的。从终端的打印可以看出，Scala从右值自动推导出了变量的类型。Scala可以如动态语言似的编写代码，但又有静态语言的编译时检查。这对于Java中冗长、重复的类型声明来说是一种很好的进步。

注：在RELP中，val变量是可以重新赋值的，这是｀RELP`的特性。在平常的代码中是不可以的。


### 基础数据类型

Scala中基础数据类型有：Byte、Short、Int、Long、Float、Double，Boolean，Char、String。和Java不同的是，Scala中没在区分原生类型和装箱类型，如：int和Integer。它统一抽象成Int类型，这样在Scala中所有类型都是对象了。编译器在编译时将自动决定使用原生类型还是装箱类型。


#### 字符串

Scala中的字符串有3种。

1. 分别是普通字符串，它的特性和Java字符串一致。
2. 连线3个双引号在Scala中也有特殊含义，它代表被包裹的内容是原始字符串，可以不需要字符转码。这一特性在定义正则表达式时很有优势。
3. 还有一种被称为“字符串插值”的字符串，他可以直接引用上下文中的变量，并把结果插入字符串中。

```
scala> val c2 = '李'
c2: Char = 李

scala> val s1 = "Hello 李"
s1: String = Hello 李

scala> val s2 = s"Hello ${c2}"
s2: String = Hello 李

scala> val s3 = s"""Hello"李"\n${c2}Leo"""
s3: String =
Hello"李"
李Leo
```
## 运算符和命名

Scala中的运算符其实是定义在对象上的方法（函数），你看到的诸如：3 + 2其实是这样子的：3.+(2)。+符号是定义在Int对象上的一个方法。支持和Java一至的运算符（方法）：

注：在Scala中，方法前的.号和方法两边的小括号在不引起歧义的情况下是可以省略

* 比较运算: ==、!=  
* 逻辑运算: !、|、&、^  
* 位运算: >>、<<

在Scala中，修正了（算更符合一般人的常规理解吧）==和!=运算符的含义。在Scala中，==和!=是执行对象的值比较，相当于Java中的equals方法。而对象的引用比较需要使用eq和ne两个方法来实现。

## 控制语句（表达式）

Scala中支持if、while、for comprehension（for表达式)、match case（模式匹配）四大主要控制语句。Scala不支持switch和?:两种控制语句，但它的if和match case会有更好的实现。


### if

Scala支持if语句，其基本使用和Java、Python中的一样。但不同的时，它是有返回值的。

注：Scala是函数式语言，函数式语言还有一大特性就是：表达式。函数式语言中所有语句都是基于“表达式”的，而“表达式”的一个特性就是它会有一个值。所有像Java中的? :3目运算符可以使用if语句来代替。
```
scala> if (true) "真" else "假"
res0: String = 真

scala> val f = if (false) "真" else "假"
f: String = 假

scala> val unit = if (false) "真"
unit: Any = ()

scala> val unit2 = if (true) "真" 
unit2: Any = 真
```

可以看到，if语句也是有返回值的，将表达式的结果赋给变量，编译器也能正常推导出变量的类型。unit和unit2变量的类型是Any，这是因为else语句的缺失，Scala编译器就按最大化类型来推导，而Any类型是Scala中的根类型。()在Scala中是Unit类型的实例，可以看做是Java中的Void。


### while

Scala中的while循环语句：

```
while (条件) {
  语句块
}
```


### for comprehension

Scala中也有for表达式，但它和Java中的for不太一样，它具有更强大的特性。通常的for语句如下：

```
for (变量 <- 集合) {
  语句块
}
```

Scala中for表达式除了上面那样的常规用法，它还可以使用yield关键字将集合映射为另一个集合：

```
scala> val list = List(1, 2, 3, 4, 5)
list: List[Int] = List(1, 2, 3, 4, 5)

scala> val list2 = for (item <- list) yield item + 1
list2: List[Int] = List(2, 3, 4, 5, 6)
```

还可以在表达式中使用if判断：
```
scala> val list3 = for (item <- list if item % 2 == 0) yield item
list3: List[Int] = List(2, 4)
```

还可以做flatMap操作，解析2维列表并将结果摊平（将2维列表拉平为一维列表）：
```
scala> val llist = List(List(1, 2, 3), List(4, 5, 6), List(7, 8, 9))
llist: List[List[Int]] = List(List(1, 2, 3), List(4, 5, 6), List(7, 8, 9))

scala> for {
     |   l <- llist
     |   item <- l if item % 2 == 0
     | } yield item
res3: List[Int] = List(2, 4, 6, 8)
```
看到了，Scala中for comprehension的特性是很强大的。Scala的整个集合库都支持这一特性，包括：Seq、Map、Set、Array……

Scala没有C-Like语言里的for (int i = 0; i < 10; i++)语法，但Range（范围这个概念），可以基于它来实现循环迭代功能。在Scala中的使用方式如下：

```
scala> for (i <- (0 until 10)) {
     |   println(i)
     | }
0
1
2
3
4
5
6
7
8
9
```

Scala中还有一个to方法：
```		
scala> (for (i <- (0 to 10)) print(" " + i))
 0 1 2 3 4 5 6 7 8 9 10
```

你还可以控制每次步进的步长，只需要简单的使用`by`方法即可：

```scala
scala> for (i <- 0 to 10 by 2) print(" " + i)
 0 2 4 6 8 10
```

**match case**
模式匹配，是函数式语言很强大的一个特性。它比命令式语言里的`switch`更好用，表达性更强。

```scala
scala> def level(s: Int) = s match {
     |   case n if n >= 90 => "优秀"
     |   case n if n >= 80 => "良好"
     |   case n if n >= 70 => "良"
     |   case n if n >= 60 => "及格"
     |   case _ => "差"
     | }
level: (s: Int)String

scala> level(51)
res28: String = 差

scala> level(93)
res29: String = 优秀

scala> level(80)
res30: String = 良好
```

可以看到，模式匹配可以实现`switch`相似的功能。但与`switch`需要使用`break`明确告知终止之后的判断不同，Scala中的`match case`是默认**break**的。只要其中一个`case`语句匹配，就终止之后的所以比较。且对应`case`语句的表达式值将作为整个`match case`表达式的值返回。

## 集合

在Scala中，常用的集合类型有：`List`、`Set`、`Map`、`Tuple`、`Vector`等。

**List**

Scala中`List`是一个不可变列表集合，它很精妙的使用递归结构定义了一个列表集合。

```scala
scala> val list = List(1, 2, 3, 4, 5)
list: List[Int] = List(1, 2, 3, 4, 5)
```

除了之前使用`List`object来定义一个列表，还可以使用如下方式：

```scala
scala> val list = 1 :: 2 :: 3 :: 4 :: 5 :: Nil
list: List[Int] = List(1, 2, 3, 4, 5)
```

`List`采用前缀操作的方式（所有操作都在列表顶端（开头））进行，`::`操作符的作用是将一个元素和列表连接起来，并把元素放在列表的开头。这样`List`的操作就可以定义成一个递归操作。添加一个元素就是把元素加到列表的开头，List只需要更改下头指针，而删除一个元素就是把List的头指针指向列表中的第2个元素。这样，`List`的实现就非常的高效，它也不需要对内存做任何的转移操作。`List`有很多常用的方法：

```scala
scala> list.indexOf(3)
res6: Int = 2

scala> 0 :: list
res8: List[Int] = List(0, 1, 2, 3, 4, 5)

scala> list.reverse
res9: List[Int] = List(5, 4, 3, 2, 1)

scala> list.filter(item => item == 3)
res11: List[Int] = List(3)

scala> list
res12: List[Int] = List(1, 2, 3, 4, 5)

scala> val list2 = List(4, 5, 6, 7, 8, 9)
list2: List[Int] = List(4, 5, 6, 7, 8, 9)

scala> list.intersect(list2)
res13: List[Int] = List(4, 5)

scala> list.union(list2)
res14: List[Int] = List(1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9)

scala> list.diff(list2)
res15: List[Int] = List(1, 2, 3)
```

Scala中默认都是**Immutable collection**，在集合上定义的操作都不会更改集合本身，而是生成一个新的集合。这与Java集合是一个根本的区别，Java集合默认都是可变的。

**Tuple**

Scala中也支持**Tuple**（元组）这种集合，但最多只支持22个元素（事实上Scala中定义了`Tuple0`、`Tuple1`……`Tuple22`这样22个`TupleX`类。和大多数语言的Tuple类似（比如：Python），Scala也采用小括号来定义元组。

```scala
scala> val tuple1 = (1, 2, 3)
tuple1: (Int, Int, Int) = (1,2,3)

scala> tuple1._2
res17: Int = 2

scala> val tuple2 = Tuple2("Leo", "Li" )
tuple2: (String, String) = (Leo,Li)
```

可以使用`xxx._[X]`的形式来引用`Tuple`中某一个具体元素，其`_[X]`下标是从1开始的，一直到22（若有定义这么多）。

**Set**

`Set`是一个不重复且无序的集合，初始化一个`Set`需要使用`Set`对象：

```scala
scala> val set = Set("Scala", "Java", "C++", "Javascript", "C#", "Python", "PHP") 
set: scala.collection.immutable.Set[String] = Set(Scala, C#, Python, Javascript, PHP, C++, Java)

scala> set + "Go"
res21: scala.collection.immutable.Set[String] = Set(Scala, C#, Python,Javascript, PHP, C++, Java, Go)

scala> set filterNot (item => item == "PHP")
res22: scala.collection.immutable.Set[String] = Set(Scala, C#, Python, Javascript, C++, Java)
```

**Map**

Scala中的`Map`默认是一个**HashMap**，其特性与Java版的`HashMap`基本一至，除了它是`Immutable`的：

```scala
scala> val map = Map("a" -> "A", "b" -> "B")
map: scala.collection.immutable.Map[String,String] = Map(a -> A, b -> B)

scala> val map2 = Map(("b", "B"), ("c", "C"))
map2: scala.collection.immutable.Map[String,String] = Map(b -> B, c -> C)
```

Scala中定义`Map`时，传入的每个`Entry`（**K**、**V**对）其实就是一个`Tuple2`（有两个元素的元组），而`->`是定义`Tuple2`的一种便捷方式。

```scala
scala> map + ("z" -> "Z")
res23: scala.collection.immutable.Map[String,String] = Map(a -> A, b -> B, z -> Z)

scala> map.filterNot(entry => entry._1 == "a")
res24: scala.collection.immutable.Map[String,String] = Map(b -> B)

scala> val map3 = map - "a"
map3: scala.collection.immutable.Map[String,String] = Map(b -> B)

scala> map
res25: scala.collection.immutable.Map[String,String] = Map(a -> A, b -> B)
```


Scala的immutable collection并没有添加和删除元素的操作，其定义`+`（`List`使用`::`在头部添加）操作都是生成一个新的集合，而要删除一个元素一般使用 `-` 操作直接将**Key**从`map`中减掉即可。

（注：Scala中也`scala.collection.mutable._`集合，它定义了不可变集合的相应可变集合版本。一般情况下，除非一此性能优先的操作（其实Scala集合采用了共享存储的优化，生成一个新集合并不会生成所有元素的复本，它将会和老的集合共享大元素。因为Scala中变量默认都是不可变的），推荐还是采用不可变集合。因为它更直观、线程安全，你可以确定你的变量不会在其它地方被不小心的更改。）

## Class

Scala里也有`class`关键字，不过它定义类的方式与Java有些区别。Scala中，类默认是**public**的，且类属性和方法默认也是**public**的。Scala中，每个类都有一个**“主构造函数”**，主构造函数类似函数参数一样写在类名后的小括号中。因为Scala没有像Java那样的“构造函数”，所以属性变量都会在类被创建后初始化。所以当你需要在构造函数里初始化某些属性或资源时，写在类中的属性变量就相当于构造初始化了。

在Scala中定义类非常简单：

```scala
class Person(name: String, val age: Int) {
  override def toString(): String = s"name：$name, age: $age"
}
```

默认，Scala主构造函数定义的属性是**private**的，可以显示指定：`val`或`var`来使其可见性为：**public**。

Scala中覆写一个方法必需添加：`override`关键字，这对于Java来说可以是一个修正。当标记了`override`关键字的方法在编译时，若编译器未能在父类中找到可覆写的方法时会报错。而在Java中，你只能通过`@Override`注解来实现类似功能，它的问题是它只是一个可选项，且编译器只提供警告。这样你还是很容易写出错误的“覆写”方法，你以后覆写了父类函数，但其实很有可能你是实现了一个新的方法，从而引入难以察觉的BUG。

实例化一个类的方式和Java一样，也是使用`new`关键字。

```scala
scala> val me = new Person("Leo", 18)
me: Person = name: Leo, age: 18

scala> println(me)
name: Leo, age: 18

scala> me.name
<console>:20: error: value name is not a member of Person
       me.name
          ^

scala> me.age
res11: Int = 30
```









---