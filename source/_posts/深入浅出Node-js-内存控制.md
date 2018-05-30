---
title: 《深入浅出Node.js》-内存控制
date: 2018-05-27 21:14:20
categories: Node
tags:
- 内存
- JavaScript
- V8       
---

# 第五章 内存控制

本章学习 V8 的垃圾回收机制以及如何高效使用内存，内存泄漏以及如何排查内存泄漏。

## V8 的垃圾回收机制与内存限制

关于 JavaScript 中常用的垃圾回收机制，可以参考这篇文章 [JavaScript 垃圾回收](https://lz5z.com/JavaScript%E5%9E%83%E5%9C%BE%E5%9B%9E%E6%94%B6/)。

### V8 的内存限制

一般后端开发语言中，在基本的内存使用上都没有什么限制，而 Node 中将 JavaScript 的使用内存做出如下限制：64 位操作系统约为 1.4G，32 位操作系统约为 0.7G。在这样的限制下，Node 无法直接操作大内存对象，比如将一个 2GB 文件读取到内存中进行字符串分析，即使物理内存有 32 GB。

### V8 的对象分配

在 V8 中，所有的 JavaScript 对象都是通过堆来进行内存分配的，Node 中可以通过 [process.memoryUsage()](http://nodejs.cn/api/process.html#process_process_memoryusage) 查看内存使用情况。

```shell
$ node
> process.memoryUsage()
> { rss: 24244224,
    heapTotal: 9232384,
    heapUsed: 5041608,
    external: 11497 }
```

<!--more-->

其中 heapTotal 和 heapUsed 是 V8 堆内存使用情况，前者是已经申请到的堆内存，后者是当前内存使用量。external 代表 V8 管理的，绑定到 Javascript 的 C++ 对象的内存使用情况。rss 代表进程常驻内存部分, 是给这个进程分配了多少物理内存(占总分配内存的一部分) 这些物理内存中包含堆，栈，和代码段。进程中的内存总共有几部分，一部分是 rss，其余部分在交换区（swap）或者文件系统（filesystem）中。

当我们在代码中声明变量并且赋值的时候，使用的对象就分配在堆中，如果已经申请到的堆内存不够分配时，就继续申请，直到超过 V8 的限制为止。

在 Node 环境中使用下面两个参数可以调整启动时内存限制的大小：

```shell
node --max-nex-space-size=1024 app.js // 单位为KB
node --max-old-space-size=2000 app.js // 单位为MB
```

### V8 垃圾回收机制

V8 采用分代式的垃圾回收机制，主要将内存分为新生代和老生代。新生代中对象存活时间较短，老生代中对象存活时间较长或者常驻内存。 `--max-old-space-size` 和 `--max-new-space-size` 就是用于设置老生代和新生代内存大小。

(1) Scavenge 算法

新生代对象主要通过 Scavenge 算法进行垃圾回收，在 Scavenge 的具体实现中，主要采取 Cheney 算法。

Cheney 算法是一种采用复制的方式实现的垃圾回收算法，它将堆内存一分为二，每份空间称为 semispace，两份堆内存一个处于使用中，一个处于闲置状态。处于使用状态的的空间称为 From 空间，处于闲置状态的空间称为 To 空间。当我们分配对象时，首先在 From 空间分配，当开始进行垃圾回收时，会检查 From 中存活的对象，将其复制到 To 空间中，非存活对象占用的空间将被释放。

Scavenge 的缺点是只能使用一半的堆内存，但是由于 Scavenge 只复制存活的对象，所以在面对声明周期较短的场景时，非常有优势。因此在 V8 新生代内存中垃圾回收使用 Scavenge 算法。

在 V8 分代式垃圾回收机制下，From 空间中存活的对象在复制到 To 空间之前要进行检查，将一些满足条件的对象移动到老生代内存中。

(2) Mark-Sweep & Mark-Compact

V8 在老生代内存中，主要采用标记清除法和标记紧缩法进行垃圾回收。

Mark-Sweep 在标记阶段遍历堆中所有的对象，并标记活着的对象，在随后的清除阶段，只清除没有被标记的对象。Mark-Sweep 存在的问题是进行一次标记清除回收后，内存会出现不连续的状态。

为了解决 Mark-Sweep 中内存碎片的问题，Mark-Compact 被提出来了。Mark-Compact 是标记整理或者标记紧缩的意思。 Mark-Compact 在 Mark-Sweep 的基础上演变而来，它们的差别在于，清除完标记对象后，在整理的过程中，将活着的对象向一端移动，移动完成后，直接清理掉边界的内存。

(3) Incremental Marking 

为了避免出现 JavaScript 应用逻辑与垃圾回收器中看到的不一致的情况，垃圾回收的 3 种算法都要将应用逻辑暂停下路，待执行完垃圾回收后再恢复执行逻辑。
增量标记是在 V8 为了降低垃圾回收时带来的停顿时间，V8 从停顿阶段入手，将原来要一口气完成的动作拆分为许多部分，每完成一部分，让 JavaScript 应用逻辑执行一小会儿，垃圾回收与应用逻辑交替执行直到标记阶段完成。

### 查看垃圾回收日志

通过在启动参数中添加 `--trace_gc`，当进行垃圾回收时，会打印出垃圾回收的信息。

通过在启动参数中添加 `--prof`，可以得到 V8 执行时的性能分析数据，其中包含垃圾回收执行所占用的时间。 

## 如何高效实用内存

### 作用域

在 JavaScript 中能形成作用域的有函数调用，with 以及 全局作用域。比如在下面代码中：

```javascript
var foo = function () {
  var local = {}  
}
```
foo() 在每次被调用的时候都会创建对于的作用域，执行完后作用域销毁，作用域内声明的局部变量也随之销毁。在这个示例中，local 对象会分配在新生代内存 From 中，作用域释放后，local 被垃圾回收。

(1) 标识符查找

标识符可以理解为变量名，在 JavaScript 执行时，它会首先查找当前作用域，如果找不到，将会向上级作用域查找，直到查到为止。这种不断向上级作用域查找的方式也叫做作用域链。

(2) 变量主动释放

全局变量如果不主动删除，可能会导致对象常驻内存（老生代），可以通过 delete 操作符来删除引用关系。或者将变量重新赋值，让旧的对象脱离引用关系。

```javascript
global.foo = 'I am a global object'
delete global.foo
//或者重新赋值
global.foo = undefined
```

### 闭包(closure)

闭包是一种反作用域链的方式，通过高阶函数，实现外部作用域访问内部作用域中的变量的方法。

```javascript
var foo = function () {
  var bar = function () {
    var local = "局部变量"
    return function () {
      return local
    }
  }
  var baz = bar()
  console.log(baz())
}
```
一般来说，bar() 函数执行完毕后，局部变量 local 就会被垃圾回收，但是 bar() 函数返回了一个匿名函数，而且匿名函数还具备访问 local 的条件，所以只要执行匿名函数的 baz 存在，local 就不会被垃圾回收。

### 小结

在正常的 JavaScript 执行中，无法立即回收的内存有闭包和全局变量，因此在使用的时候要多加小心，避免老生代内存不断增多的现象。

## 内存指标

### 查看内存使用情况

(1) process.memoryUsage() 
(2) os 模块的 totalmem() 和 freemem() 可以查看操作系统总内存和闲置内存。

### 堆外内存

通过 process.memoryUsage() 可以发现堆中的内存使用量总是小于进程的常驻内存使用量的，这就意味着 Node 中内存的使用并非全部通过 V8 进行分配。那些不通过 V8 进行分配的内存成为堆外内存。比如 Buffer 对象使用的就是堆外内存。

## 内存泄漏

造成内存泄漏的主要原因有：缓存，队列消费不及时，作用域未释放。

### 缓存

在 Node 中，一旦一个对象被当做缓存用，那就意味着它将会常驻老生代内存，老生代内存的堆积会导致垃圾回收在进行扫描时，对这些对象做无用功。

下面是我们经常都会写的代码：

```javascript
var cache = {}
var get = function (key) {
  if (cache[key]) {
    return cache[key]
  } else {
    // get from otherwise
    cache[key] = value
    return value
  }
}
```

上述代码十分容易理解，创建缓存以内存换取 CPU 执行时间，但是要注意一定要限定缓存对象的大小，再加上完善的过期策略防止内存无限制增长。

### 缓存的解决方案

直接将内存作为缓存的方案要十分慎重，除了要限制缓存大小外，还需要考虑的事情是进程直接无法共享内存。解决方案是使用进程外缓存，比如 Redis 和 Memcached。

### 关注队列状态

Node 通过生产者-消费者模式构建消息队列，假如队列的消费速度低于队列的生成速度，很容易造成堆积。举一个例子，有的应用会收集日志，假如采用数据库来记录日志，由于数据库构于文件系统之上，写入的效率低于文件直接写入，于是会形成数据库写入操作的堆积，而 JavaScript 中相关的作用域得不到释放，从而导致内存泄漏。

解决方法：

1. 使用更快消费速度的技术。比如日志使用文件系统读写代替数据库。
2. 监控队列的长度，一旦堆积，监控系统产生警报并通知相关人员。
3. 任意的异步调用都应该包含超时机制，一旦在限定时间内未完成响应，通过回掉函数传递超时异常，使异步调用有可控的响应时间。
4. Bagpipe 中提供超时模式和拒绝模式，启动超时模式时，函数超时就返回超时错误，启动拒绝模式时，当队列拥塞时，新来的调用会直接响应拥塞错误。

## 内存泄漏排查

[node-heapdump](https://github.com/bnoordhuis/node-heapdump) 允许对 V8 堆内存抓取快照，用于事后分析。

[node-memwatch](https://github.com/lloyd/node-memwatch)

```javascript
var memwatch = require('memwatch')
memwatch.on('leak', function (info) {
  console.log('leak:')
  console.log(info)
})
memwatch.on('stats', function (stats) {
  console.log('stats:')
  console.log(stats)
})
```

### stats 事件

在进程中使用 node-memwatch 之后，每次进行垃圾回收的时候，都会触发一次 stats 事件，这个事件将会传递内存的统计信息。

```javascript
{
  "num_full_gc": 17,  // 第 17 次进行全队垃圾回收
  "num_inc_gc": 8, // 第几次增量垃圾回收
  "heap_compactions": 8, // 第几次对老生代进行整理
  "estimated_base": 2592568, // 预估基数
  "current_base": 2592568, // 当前基数
  "min": 2499912, // 最小
  "max": 2592568, // 最大
  "usage_trend": 0
}
```

### leak 事件

leak 事件记录 Node 中存在的内存泄漏。如果经过 5 次垃圾回收，内存仍然没有释放，这意味着可能存在内存泄漏，node-memwatch 会发出一个 leak 事件。

```javascript
{ start: Fri, 29 Jun 2012 14:12:13 GMT,
  end: Fri, 29 Jun 2012 14:12:33 GMT,
  growth: 67984,
  reason: 'heap growth over 5 consecutive GCs (20s) - 11.67 mb/hr' }
```

growth 显示了 5 次垃圾回收的过程中内存增长了多少。

## 大内存应用

Node 中使用 Stream 模块处于处理大文件

Stream 模块