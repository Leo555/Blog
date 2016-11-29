---
title: Spark RDD 操作
date: 2016-11-29 15:08:50
categories: Big Data
tags:
- Spark
- Scala
- RDD
---

# RDD 操作

RDD 支持 2 种类型的操作: transformations 和 actions。transformations： 从已经存在的数据集中创建一个新的数据集，如 map。actions： 数据集上进行计算之后返回一个值，如 reduce。

在 Spark 中，所有的 transformations 都是 lazy 的，它们不会马上计算它们的结果，而是仅仅记录转换操作是应用到哪些基础数据集上的，只有当 actions 要返回结果的时候计算才会发生。

默认情况下，每一个转换过的 RDD 会在每次执行 actions 的时候重新计算一次。然而，你也可以使用 persist (或 cache)方法持久化一个 RDD 到内存中。在这个情况下，Spark 会在集群上保存相关的元素，在你下次查询的时候会变得更快。在这里也同样支持持久化 RDD 到磁盘，或在多个节点间复制。
<!-- more -->

## 基础

在 Spark-shell 中运行如下脚本

```shell
scala> val lines = sc.textFile("test.txt")
lines: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[10] at textFile at <console>:21

scala> val lineLengths = lines.map(s => s.length)
lineLengths: org.apache.spark.rdd.RDD[Int] = MapPartitionsRDD[11] at map at <console>:23

scala> val totalLength = lineLengths.reduce((a, b) => a + b))
totalLength: Int = 30
```

第一步： 定义外部文件 RDD，定义 lines 指向 test.txt 文件， 这个文件即没有加载到内存也没有做其他的操作，所以即使文件不存在也不会报错。
第二步： 定义 lineLengths，它是 map 转换(transformation)的结果。同样，lineLengths 由于 lazy 模式也没有立即计算。
第三步： reduce 是一个 action， 所以真正执行读文件和 map 计算是在这一步发生的。Spark 将计算分成多个 task，并且让它们运行在多个机器上。每台机器都运行自己的 map 部分和本地 reduce 部分。然后仅仅将结果返回给驱动程序。

如果我们想要再次使用 lineLengths，我们可以使用 persist 或者 cache 将 lineLengths 保存到内存中。

```shell
scala> lineLengths.persist()
res6: lineLengths.type = MapPartitionsRDD[11] at map at <console>:23

scala> lineLengths.collect()
res7: Array[Int] = Array(5, 3, 15, 7)
```
