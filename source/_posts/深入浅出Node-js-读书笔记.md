---
title: 《深入浅出Node.js》-读书笔记
date: 2018-05-23 22:51:15
categories: Node
tags:
- JavaScript
- Node    
---

## 简介

不知不觉 Node 已经更新到第十个版本了，本人使用 Node 也有两年多时间，之前学习的东西一直零零散散，没有形成系统的知识体系，于是最近又抽时间回顾这本经典的 [《深入浅出Node.js》](https://book.douban.com/subject/25768396/)，阅读的过程中，难免有些东西不易理解或者容易忘记，因此选择博客的形式记录。

作者书写这本书的时候，Node 的稳定版本为 v0.10.13，当前最高版本为 v10.1.0，不过整个 Node 的核心体系在当时已经形成，因此对更高版本的理解问题不大。

## 第一章 Node 简介

Node 诞生于 2009 年 3 月，作者为 Ryan Dahl。作者选择 JavaScript 作为 Node 的实现语言主要因为：JavaScript 高性能（V8），符合事件驱动，没有后端历史包袱。

除了 HTML、WebKit 和显卡这些与 UI 相关技术没有支持外，整个 Node 的结构与 Chrome 非常相似，它们都是基于事件驱动的异步架构，浏览器通过事件驱动来服务界面上的交互，Node 通过事件驱动来服务 I/O。

<!--more-->

### Node 的特点

(1) 异步 I/O。在 Node 中，绝大多数的操作都是以异步的方式进行调用，从文件操作到网络请求都是如此。
(2) 事件与回调函数。Node 将前端浏览器中应用广泛的事件机制引入后端，配合异步 I/O。优点是事件编程轻量，低耦合，只用关注事务点等，缺点是多个事件之间的协作是一个问题。
(3) 单线程。Node 保持了 JS 单线程的特点，在 Node 中，JS 与其余线程无法共享状态。单线程好处了不用处理多线程之间的状态同步与通信，没有死锁的存在，也没有线程切换带来的性能开销。缺点是无法利用多核 CPU；错误会引起整个应用退出，应用健壮性值得考验；对大规模高 CPU 计算不友好。

在浏览器中，HTML5 制定了 Web Worker 标准来解决 JS 大规模计算导致的阻塞 UI 渲染的问题。而 Node 中，使用 child_process 创建子进程来应对单线程带来的问题。

(4) 跨平台。

### Node 应用场景

(1) I/O 密集型。I/O 密集的优势˞要在于 Node 利用事件循环的能力，而不是启动每一个线程为每一个请
求服务，资源占用极少。
(2) Node 是否适用于 CPU 密集型应用？首先 Node 的计算性能并不差，但是由于 JavaScript 单线程的原因，如果有长时间运算，将导致 CPU 不能释放，使后续 I/O 无法发起。
(3) 与遗留系统和平共处。比如和 Java 配合，Node 完成 Web 端的开发，Java 提供稳定的接口。
(4) 分布式应用。

## 第二章 模块机制

Node 的模块化采用 CommonJS 规范，关于 JavaScript 模块化的各种规范，可以参考 [前端模块化-CommonJS,AMD,CMD,ES6](https://lz5z.com/JavaScript%E6%A8%A1%E5%9D%97%E5%8C%96-CommonJS-AMD-CMD-ES6/)。

CommonJS 规范涵盖了模块，二进制，Buffer，字符集编码，I/O 流，进程环境，文件系统，socket，单元测试，Web服务器接口，包管理等。

### CommonJS 模块规范

(1) 模块引用

通过 require() 方法引入一个模块的 API 到当前上下文中。

```javascript
var math = require('math')
```
(2) 模块定义

在模块中，上下文提供 exports 对象用于导出当前模块的变量或者方法，并且它是唯一导出的出口。在模块中，还存在一个 module 对象，代表模块自身，而 exports 是 module 的属性。

```javascript
exports.add = function () {
  return eval(Array.prototype.join.call(arguments, '+'))  
}
```

(3) 模块标识

模块标识就是传递给 require() 的参数，它必须是符合小驼峰命名的字符串，或者以 `.` 和 `..` 开头的相对路径，或者绝对路径。

CommonJS 构建的这套模块导出和引入机制使得用户完全不必考虑变量污染，命名空间等方案相形见绌。

### Node 模块实现

Node 引入模块，需要经历三个步骤：路径分析，文件定位，编译执行。

Node 中的模块分为核心模块和文件模块。

(1) 核心模块在 Node 源码编译过程中，编译成为二进制文件，在 Node 启动阶段部分核心模块就被加载进内存，所以省去了文件定位和编译的时间，加载速度最快。

(2) 文件模块则是在运行时动态加载。

(3) 自定义模块是指非核心模块，也不是路径形式的文件模块。以文件或者包的形式存在，这类模块的查找是最费时的。

模块路径：Node 在定位文件模块的时候采用的一种查找策略。具体表现为一个路径组成的数组。比如我在自己的电脑 `/Users/lizhen/WorkSpaces/test` 目录下面创建文件 index.js：

内容如下：

```javascript
console.log(module.paths)
```

运行脚本输出结果如下：

```shell
[ '/Users/lizhen/WorkSpaces/test/node_modules',
  '/Users/lizhen/WorkSpaces/node_modules',
  '/Users/lizhen/node_modules',
  '/Users/node_modules',
  '/node_modules' ]
```

其路径寻址规则如下：从当前目录的 node_modules 中寻找 -> 父目录的 node_modules 中寻找 -> 递归一直到根目录的 node_modules。

它的生成方式与 JavaScript 原型链或者作用域链的查找方式十分类似。Node 会逐个尝试模块路径，直到找到模块或者查找到根目录位置。可以看出，当文件路径比较深的时候，模块查找会比较耗时。


Node 对引入过的模块都会进行缓存，无论是核心模块还是文件模块，require() 方法都采用缓存优先的方式进行加载，并且核心模块的优先级高于文件模块。

#### 文件定位

require() 在分析标识符的过程中，如果标识符不包括扩展名，Node 会按照 `.js`, `.json`, `.node` 的次序补足扩展名，依次尝试。

在尝试的过程中，需要调用 fs 模块同步阻塞式地判断文件是否存在，所以会引起性能问题。解决的办法是：1. `.node` 和 `.json` 文件标识符中带上扩展名。2. 同步配合缓存，可以大幅缓解 Node 单线程中阻塞调用的缺陷。

