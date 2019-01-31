---
title: '[真] Node多线程'
date: 2019-01-31 19:52:19
categories: Node
tags:
- cluster
- worker_threads
---

> 本文测试使用环境：
系统：macOS Mojave 10.14.2
CPU：4 核 2.3 GHz
Node: 10.15.1

## 从 Node 线程说起

一般人理解 Node 是单线程的，所以 Node 启动后线程数应该为 1，我们做实验看一下。

```javascript
setInterval(() => {
  console.log(new Date().getTime())
}, 3000)
```

<img src="/assets/img/node_thread.png" alt="node_thread" style="max-width: 650px">

可以看到 Node 进程占用了 7 个线程。为什么会有 7 个线程呢？

我们都知道，Node 中最核心的是 v8 引擎，在 Node 启动后，会创建 v8 的实例，这个实例是多线程的。

- 主线程：编译、执行代码。
- 编译/优化线程：在主线程执行的时候，可以优化代码。
- 分析器线程：记录分析代码运行时间，为 Crankshaft 优化代码执行提供依据。
- 垃圾回收的几个线程。

<!--more-->

所以大家常说的 Node 是单线程的指的是 JavaScript 的执行是单线程的，但 Javascript 的宿主环境，无论是 Node 还是浏览器都是多线程的。


> Node 有两个编译器：
full-codegen：简单快速地将 js 编译成简单但是很慢的机械码。
Crankshaft：比较复杂的实时优化编译器，编译高性能的可执行代码。


### 某些异步 IO 会占用额外的线程

还是上面那个例子，我们在定时器执行的同时，去读一个文件：

```javascript
const fs = require('fs')

setInterval(() => {
    console.log(new Date().getTime())
}, 3000)

fs.readFile('./index.html', () => {})
```
<img src="/assets/img/node_thread_1.png" alt="node_thread" style="max-width: 650px">

线程数量变成了 11 个，这是因为在 Node 中有一些 IO 操作（DNS，FS）和一些 CPU 密集计算（Zlib，Crypto）会启用 Node 的线程池，而线程池默认大小为 4，因为线程数变成了 11。

我们可以手动更改线程池默认大小：

```javascript
process.env.UV_THREADPOOL_SIZE = 64
```

一行代码轻松把线程变成 71 :blush:

<img src="/assets/img/node_thread_2.png" alt="node_thread" style="max-width: 850px">


## cluster 是多线程吗？

Node 的单线程也带来了一些问题，比如对 cpu 利用不足，某个未捕获的异常可能会导致整个程序的退出等等。因为 Node 中提供了 cluster 模块，cluster 实现了对 child_process 的封装，通过 fork 方法创建子进程的方式实现了多进程模型。比如我们最常用到的 pm2 就是其中最优秀的代表。

我们看一个 cluster 的 demo：

```javascript
const cluster = require('cluster');
const http = require('http');
const numCPUs = require('os').cpus().length;

if (cluster.isMaster) {
  console.log(`主进程 ${process.pid} 正在运行`);
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code, signal) => {
    console.log(`工作进程 ${worker.process.pid} 已退出`);
  });
} else {  
  // 工作进程可以共享任何 TCP 连接。
  // 在本例子中，共享的是 HTTP 服务器。
  http.createServer((req, res) => {
    res.writeHead(200);
    res.end('Hello World');
  }).listen(8000);
  console.log(`工作进程 ${process.pid} 已启动`);
}
```

这个时候看下活动监视器：

<img src="/assets/img/node_thread_3.png" alt="node_thread" style="max-width: 600px">

一共有 9 个进程，其中一个主进程，cpu 个数 * cpu 核数 = 2 * 4 = 8 个 子进程。

所以无论 child_process 还是 cluster，都不是多线程模型，而是多进程模型。虽然开发者意识到了单线程模型的问题，但是没有从根本上解决问题，而且提供了一个多进程的方式来模拟多线程。从前面的实验可以看出，虽然 Node （V8）本身是具有多线程的能力的，但是开发者并不能很好的利用这个能力，更多的是由 Node 底层提供的一些方式来使用多线程。Node 官方说：

>You can use the built-in Node Worker Pool by developing a C++ addon. On older versions of Node, build your C++ addon using NAN, and on newer versions use N-API. node-webworker-threads offers a JavaScript-only way to access Node's Worker Pool.

但是对于 JavaScript 开发者，一直没有一个标准的、好用的方式来使用 Node 的多线程能力。


## 真 - Node 多线程

直到 Node 10.5.0 的发布，官方才给出了一个实验性质的模块 [worker_threads](http://nodejs.cn/api/worker_threads.html) 给 Node 提供真正的多线程能力。

先看下简单的 demo：

```javascript
const {
  isMainThread,
  parentPort,
  workerData,
  threadId,
  MessageChannel,
  MessagePort,
  Worker
} = require('worker_threads');

function mainThread() {
  for (let i = 0; i < 5; i++) {
    const worker = new Worker(__filename, { workerData: i });
    worker.on('exit', code => { console.log(`main: worker stopped with exit code ${code}`); });
    worker.on('message', msg => {
      console.log(`main: receive ${msg}`);
      worker.postMessage(msg + 1);
    });
  }
}

function workerThread() {
  console.log(`worker: workerDate ${workerData}`);
  parentPort.on('message', msg => {
    console.log(`worker: receive ${msg}`);
  }),
  parentPort.postMessage(workerData);
}

if (isMainThread) {
  mainThread();
} else {
  workerThread();
}
```
 
上述代码在主线程中开启五个子线程，并且主线程向子线程发送简单的消息。


由于 worker_thread 目前仍然处于实验阶段，所以启动时需要增加 `--experimental-worker` flag，运行后观察活动监视器：

<img src="/assets/img/node_thread_4.png" alt="node_thread" style="max-width: 600px">

不多不少，正好多了五个子线程。:blush:


### [worker_thread](https://nodejs.org/api/worker_threads.html) 模块

worker_thread [核心代码](https://github.com/nodejs/node/blob/master/lib/worker_threads.js)

worker_thread 模块中有 4 个对象和 2 个类。

- isMainThread: 是否是主线程，源码中是通过 `threadId === 0` 进行判断的。
- MessagePort: 用于线程之间的通信，继承自 EventEmitter。
- MessageChannel: 用于创建异步、双向通信的通道实例。
- threadId: 线程 ID。
- Worker: 用于在主线程中创建子线程。第一个参数为 filename，表示子线程执行的入口。
- parentPort: 在 worker 线程里是表示父进程的 MessagePort 类型的对象，在主线程里为 null
- workerData: 用于在主进程中向子进程传递数据（data 副本）


来看一个进程通信的例子：

```javascript
const assert = require('assert');
const {
  Worker,
  MessageChannel,
  MessagePort,
  isMainThread,
  parentPort
} = require('worker_threads');
if (isMainThread) {
  const worker = new Worker(__filename);
  const subChannel = new MessageChannel();
  worker.postMessage({ hereIsYourPort: subChannel.port1 }, [subChannel.port1]);
  subChannel.port2.on('message', (value) => {
    console.log('received:', value);
  });
} else {
  parentPort.once('message', (value) => {
    assert(value.hereIsYourPort instanceof MessagePort);
    value.hereIsYourPort.postMessage('the worker is sending this');
    value.hereIsYourPort.close();
  });
}
```

更多详细用法可以查看[官方文档](https://nodejs.org/api/worker_threads.html)。


### 多进程 vs 多线程

根据大学课本上的说法：“进程是资源分配的最小单位，线程是CPU调度的最小单位”，这句话应付考试就够了，但是在实际工作中，我们还是要根据需求合理选择。

下面对比一下多线程与多进程：

| 属性 | 多进程 | 多线程 | 比较 |
| :-| :------: | :------: | :-|
| 数据 | 数据共享复杂，需要用IPC；数据是分开的，同步简单 | 因为共享进程数据，数据共享简单，同步复杂| 各有千秋 |
| CPU、内存 | 占用内存多，切换复杂，CPU利用率低 | 占用内存少，切换简单，CPU利用率高 | 多线程更好 |
| 销毁、切换 | 创建销毁、切换复杂，速度慢 | 创建销毁、切换简单，速度很快 | 多线程更好 |
| coding | 编码简单、调试方便 | 编码、调试复杂 | 多进程更好 |
| 可靠性 | 进程独立运行，不会相互影响 | 线程同呼吸共命运 | 多进程更好 |
| 分布式 | 可用于多机多核分布式，易于扩展 | 只能用于多核分布式 | 多进程更好 |

上述比较仅表示一般情况，并不绝对。

work_thread 让 Node 有了真正的多线程能力，算是不小的进步。



