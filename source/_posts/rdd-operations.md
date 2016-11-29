---
title: Spark RDD 操作——Transformations
date: 2016-11-29 15:08:50
categories: Big Data
tags:
- Spark
- Scala
- RDD
---

# RDD 操作

Spark RDD 支持2种类型的操作: transformations 和 actions。transformations： 从已经存在的数据集中创建一个新的数据集，如 map。actions： 数据集上进行计算之后返回一个值，如 reduce。

在 Spark 中，所有的 transformations 都是 lazy 的，它们不会马上计算它们的结果，而是仅仅记录转换操作是应用到哪些基础数据集上的，只有当 actions 要返回结果的时候计算才会发生。

默认情况下，每一个转换过的 RDD 会在每次执行 actions 的时候重新计算一次。但是可以使用 persist (或 cache)方法持久化一个 RDD 到内存中，这样Spark 会在集群上保存相关的元素，下次查询的时候会变得更快，也可以持久化 RDD 到磁盘，或在多个节点间复制。
<!-- more -->

## 基础

在 Spark-shell 中运行如下脚本

```shell
scala> val lines = sc.textFile("test.txt")
scala> val lineLengths = lines.map(s => s.length)
scala> val totalLength = lineLengths.reduce((a, b) => a + b))
totalLength: Int = 30
```

第一步： 定义外部文件 RDD，lines 指向 test.txt 文件， 这个文件即没有加载到内存也没有做其他的操作，所以即使文件不存在也不会报错。
第二步： 定义 lineLengths，它是 map 转换(transformation)的结果。同样，lineLengths 由于 lazy 模式也没有立即计算。
第三步： reduce 是一个 action， 所以真正执行读文件和 map 计算是在这一步发生的。Spark 将计算分成多个 task，并且让它们运行在多台机器上。每台机器都运行自己的 map 部分和本地 reduce 部分，最后将结果返回给驱动程序。

如果我们想要再次使用 lineLengths，我们可以使用 persist 或者 cache 将 lineLengths 保存到内存中。

```shell
scala> lineLengths.persist()
scala> lineLengths.collect()
res7: Array[Int] = Array(5, 3, 15, 7)
```

# Transformations

## filter(func)

filter 返回一个新的数据集，从源数据中选出 func 返回 true 的元素。

```shell
scala> val a = sc.parallelize(1 to 9)
scala> val b = a.filter(x => x > 5)
scala> b.collect
res11: Array[Int] = Array(6, 7, 8, 9)
```

## flatMap(func)

与 map 类似，区别是原 RDD 中的元素经 map 处理后只能生成一个元素，而经 flatmap 处理后可生成多个元素来构建新 RDD， 所以 func 必须返回一个 Seq，而不是单个 item。

举例：对原RDD中的每个元素x产生y个元素（从1到y，y为元素x的值）

```shell
scala> val a = sc.parallelize(1 to 4, 2)
scala> val b = a.flatMap(x => 1 to x)
scala> b.collect
res12: Array[Int] = Array(1, 1, 2, 1, 2, 3, 1, 2, 3, 4)
```
## mapPartitions(func)

mapPartitions 是 map 的一个变种。map 的输入函数是应用于 RDD 中每个元素，而 mapPartitions 的输入函数是应用于每个分区，也就是把每个分区中的内容作为整体来处理的。 
它的函数定义为：

```scala
def mapPartitions[U](f: (Iterator[T]) => Iterator[U], preservesPartitioning: Boolean = false)(implicit arg0: ClassTag[U]): RDD[U]
```
f 即为输入函数，它处理每个分区里面的内容。每个分区中的内容将以 Iterator[T] 传递给输入函数 f，f 的输出结果是 Iterator[U]。最终的 RDD 由所有分区经过输入函数处理后的结果合并起来的。

```scala
scala> val rdd = sc.makeRDD(1 to 5, 2)
scala> val rdd2 = rdd.mapPartitions(x => {
     | 	var result = List[Int]()
     | 	var i = 0
     | 	while(x.hasNext) {
     | 	  i += x.next
     | 	}
     | 	result.::(i).iterator
     |})
scala> rdd2.collect()
res13: Array[Int] = Array(3, 12)

scala> rdd2.partitions.size()
res14: Int = 2
```

上述例子中 rdd2 将 rdd 每个分区中的数值累加。

## mapPartitionsWithIndex(func)