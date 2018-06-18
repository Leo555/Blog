---
title: 《深入浅出Node.js》-玩转进程
date: 2018-06-18 17:28:28
categories: Node
tags:
- child_process
- Cluster    
---

# 第九章 玩转进程


Node 基于 V8 引擎构建，采用单线程模型，所有的 JavaScript 将会运行在单个进程的单个线程上，它带来的好处是：没有多线程中常见的锁以及线程同步的问题，操作系统在调度时也能减少上下文切换，提高 CPU 使用率。但是如今 CPU 基本均是多核的，真正的服务器往往还有多个 CPU，一个 Node 进程只能利用一个核，这带来硬件资源的浪费。另外，Node 运行在单线程之上，一个单线程抛出异常而没有被捕获，将会导致进程的崩溃。

严格来说，Node 并非真正的单线程，Node 自身中还有 I/O 线程存在，这些 I/O 线程由底层 libuv 处理，这部分线程对于 JavaScript 而言是透明的，只有 C++ 扩展时才会关注到，JavaScript 代码运行在 V8 上，是单线程的。

<!--more-->

## 服务器变迁

1. 同步：最早服务器是同步模型，一次只能处理一个请求，其它请求都需要等待当前请求处理完毕。假如每次响应耗时为 N 秒，这类服务的 QPS 为 1/N。
2. 复制进程：每一个连接使用一个进程来服务，采用进程的复制实现，代价非常昂贵。假如进程数上限为 M，这类服务的 QPS 为 M/N。
3. 多线程：一个线程处理一个请求，线程相对进程开销要小很多，线程直接可以共享数据，利用线程池减少创建和销毁线程的开销。假如线程占用的资源为进程的 1/L，它的 QPS 为 M*L/N。
4. 事件驱动：Node 和 Nginx 采用事件驱动的方式实现，避免了不必要的内存开销和上下文切换。事件驱动模型存在的主要问题是 CPU 利用率不高和程序健壮性不能保证。
5. 协程：基于协程实现的服务器，比如 Golang 目前也非常流行，协程是用户级别线程，它对于内核透明，完全由用户自己进行程序之间的调用。详细内容可以参考我这篇文章[Python 协程](https://lz5z.com/Python%E5%8D%8F%E7%A8%8B/)。

## 多进程架构

Node 提供 child_process 模块来实现多核 CPU 的利用。child_process.fork() 函数来实现进程的复制。

worker.js 代码如下：

```javascript
var http = require('http')
http.createServer(function(req, res) {
  res.writeHead(200, { 'Content-Type': 'text/plain' })
  res.end('Hello World\n')
}).listen(Math.round((1 + Math.random()) * 1000), '127.0.0.1')
```
通过 `node worker.js` 启动它，会监听 1000 到 2000 之间的一个随机端口。

master.js 代码如下：

```javascript
var fork = require('child_process').fork
var cpus = require('os').cpus()
for (var i = 0; i < cpus.length; i++) {
  fork('./worker.js')
}
```
这段代码根据 CPU 数量复制出对应的 Node 进程数，Linux 系统下通过 ps aux | grep worker.js 查看进程的数量。

```shell
$ ps aux | grep worker.js
lizhen 1475 0.0 0.0 2432768 600 s003 S+ 3:27AM 0:00.00 grep worker.js
lizhen 1440 0.0 0.2 3022452 12680 s003 S 3:25AM 0:00.14 /usr/local/bin/node ./worker.js
lizhen 1439 0.0 0.2 3023476 12716 s003 S 3:25AM 0:00.14 /usr/local/bin/node ./worker.js
lizhen 1438 0.0 0.2 3022452 12704 s003 S 3:25AM 0:00.14 /usr/local/bin/node ./worker.js
lizhen 1437 0.0 0.2 3031668 12696 s003 S 3:25AM 0:00.15 /usr/local/bin/node ./worker.js 
```
这种通过 Master 启多个 Worker 的模式就是主从模式，进程被分为主进程和工作进程。主进程不负责具体的业务，而是负责调度和管理工作进程，它是趋于稳定的。

通过 fork() 复制的进程都是独立的进程，这个进程中有着独立的 V8 实例，它需要至少 30ms 的启动时间和至少 10MB 的内存。因此 fork 依然是昂贵的。

### 创建子进程

child_process 模块给予 Node 可以随意创建子进程的能力，详细的使用方法可以参考这篇文章：[Node.js 中 child_procss 模块](https://lz5z.com/Node.js%E4%B8%ADchild_procss%E6%A8%A1%E5%9D%97/)。

1. spawn() 启动一个子进程执行命令。
2. exec() 启动子进程执行命令，通过回调函数获取子进程状态。
3. execFile() 启动一个子进程执行可执行文件。
4. fork() 通过制定需要执行的 JavaScript 文件创建 Node 子进程。

```javascript
var cp = require('child_process')
cp.spawn('node', ['worker.js'])
cp.exec('node worker.js', function (err, stdout, stderr) {
 // some code
})
cp.execFile('worker.js', function (err, stdout, stderr) {
 // some code
})
cp.fork('./worker.js')
```

### 进程之间的通信

首先来看一个示例：
 
parent.js

```javascript
var cp = require('child_process')
var n = cp.fork(__dirname + '/sub.js')
n.on('message', function (m) {
  console.log('PARENT got message:', m)
})
n.send({hello: 'world'})
```
sub.js

```javascript
process.on('message', function (m) {
  console.log('CHILD got message:', m)
})
process.send({foo: 'bar'})
```
通过 fork() 或者其它 API，创建子进程之后，为了实父子程之间的通信，父进程与子进
程之间会创建 IPC 通道。通过过 IPC 通道，父子进程之间才能通过 message 和 send() 传递信息。

> 进程间通信原理：
> IPC 全称是 Inter-Process Communication，即进程间通信，Node 实现 IPC 使用管道(pipe)技术，具体实现细节由 libuv 提供。在 Windows 下由命名管道（named pipe）实现，Linux 下采用 Unix Domain Socket 实现。表现在应用层上的进程间通信只有简单的 message 事件和 send() 方法。父进程在实际创建子进程之前，会创建 IPC 通道并监听它，然后才真正创建出子进程，并且通过环境变量 NODE_CHANNEL_FD 告诉子进程这个 IPC 通道的**文件描述符**。子进程通过这个文件描述符去连接这个已存在的 IPC 通道，从而完成父子进程之间的连接。

<img src="/assets/img/process_ipc.png" alt="process_ipc">

由于 IPC 管道是用命名管道或者 Domain Socket 创建的，与网络 socket 比较类似，属于双向通行。不同的是它们在系统内核中就完成了进程间的通信，而不是通过网络层，非常高效。

### 句柄传递

通常我们启用多个 Node 进程的时候，假如每个进程都监听 80 端口，会导致 EADDRINUSE 异常，解决方案是让每个进程监听不同的端口，其中主进程监听 80，对外接收所有的网络请求，再将这些请求代理到不同的端口的进程上。

<img src="/assets/img/process_80.png" alt="process_80">

通过代理不仅能解决端口重复监听的问题，还能适当的做负载均衡。由于进程每接收一个连接都会用掉一个文件描述符，因此代理方案中客户端连接到代理进程，代理进程连接到工作进程的过程需要用掉两个文件描述符，操作系统的文件描述符是有限的，代理方式需要一倍数量的文件描述符影响了系统的扩展能力。

为了解决上述问题，Node 引入了进程间传递句柄的功能。

```javascript
child.send(message, [sendHandle])
```
句柄是一种可以用来标识资源的引用，比如句柄可以标识一个服务器端的 socket 对象，一个客户端的 socket 对象，一个 UDP scoket，一个管道等。

发送句柄意味着主进程接收到 socket 请求后，直接将 socket 发送给工作进程，而不是重新与工作进程之间建立新的 socket 连接来转发数据。

主进程 parent.js：

```javascript
var child = require('child_process').fork('child.js')
// Open up the server object and send the handle
var server = require('net').createServer()
server.on('connection', function(socket) {
  socket.end('handled by parent\n')
})
server.listen(1337, function() {
  child.send('server', server)
})
```
子进程 child.js：

```javascript
process.on('message', function(m, server) {
  if (m === 'server') {
    server.on('connection', function(socket) {
      socket.end('handled by child\n')
    })
  }
})
```
通过 node 启动查看效果：

```shell
// 先启动服务器
$ node parent.js
// 使用 curl 工具
$ curl "http://127.0.0.1:1337"
handled by parent
$ curl "http://127.0.0.1:1337"
handled by child
$ curl "http://127.0.0.1:1337"
handled by child
$ curl "http://127.0.0.1:1337"
handled by parent
```
可以看出父子进程都有可能处理客户端请求。

尝试将服务发送给多个子进程。

```javascript
// parent.js
var cp = require('child_process')
var child1 = cp.fork('child.js')
var child2 = cp.fork('child.js')
// Open up the server object and send the handle
var server = require('net').createServer()
server.on('connection', function(socket) {
  socket.end('handled by parent\n')
})
server.listen(1337, function() {
  child1.send('server', server)
  child2.send('server', server)
})
```
子进程将进程 ID 打印出来。

```javascript
// child.js
process.on('message', function(m, server) {
  if (m === 'server') {
    server.on('connection', function(socket) {
      socket.end('handled by child, pid is ' + process.pid + '\n')
    })
  }
})
```
通过 curl 测试依然是相同的结果，请求可能被父进程处理，也可能被不同的子进程处理。并且这些都是在 TCP 层面完成的事情。我们尝试将其改成 HTTP 层来处理。

```javascript
// parent.js
var cp = require('child_process')
var child1 = cp.fork('child.js')
var child2 = cp.fork('child.js')
// Open up the server object and send the handle
var server = require('net').createServer()
server.listen(1337, function() {
  child1.send('server', server)
  child2.send('server', server)
  // 关闭
  server.close()
})
```
对子进程进行改动

```javascript
// child.js
var http = require('http')
var server = http.createServer(function(req, res) {
  res.writeHead(200, { 'Content-Type': 'text/plain' })
  res.end('handled by child, pid is ' + process.pid + '\n')
})
process.on('message', function(m, tcp) {
  if (m === 'server') {
    tcp.on('connection', function(socket) {
      server.emit('connection', socket)
    })
  }
})
```
重新启动 parent.js 后，再次测试，所有的请求都是由子进程处理了。整个过程中，服务的过程发生了一次改变：

<img src="/assets/img/process_handle.png" alt="process_handle">

主进程发送完句柄并且关闭监听之后，成了下图的结构：

<img src="/assets/img/process_handle_1.png" alt="process_handle_1">
 
1. 句柄发送与还原
2. 端口共同监听

## 集群稳定之路


