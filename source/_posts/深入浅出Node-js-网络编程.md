---
title: 《深入浅出Node.js》-网络编程
date: 2018-05-30 00:12:53
categories: Node
tags:
- 网络
- TCP
- UDP
- OSI    
---

# 第七章 网络编程

Node 中提供了 net，dgram，http，https 四个模块，分别用来处理 TCP，UDP，HTTP，HTTPS，适用于客户端和服务器。

## TCP

TCP 传输控制协议，在 OSI 模型中属于传输层，许多应用层的协议基于 TCP 构建，比如 HTTP，SMTP，IMAP 等。回顾一下 OSI 模型。

- 第 7 层：**应用层**为操作系统或网络应用程序提供访问网络服务的接口。应用层协议的代表包括： HTTP，HTTPS，FTP，TELNET，SSH，SMTP，POP3等。
- 第 6 层：**表示层**把数据转换为接受者能够兼容并且适合传输的内容，比如数据加密，压缩，格式转换等。
- 第 5 层：**会话层**负责数据传输中设置和维持网络设备之间的通信连接。管理主机之间的会话进程，还可以利用在数据中插入校验点来实现数据的同步。
- 第 4 层：**传输层**把传输表头加至数据形成数据包，完成端到端的数据传输。传输表头包含了协议等信息，比如: TCP，UDP 等。
- 第 3 层：**网络层**负责对子网间的数据包进行寻址和路由选择，还可以实现拥塞控制，网际互联等功能。网络层的协议包括：IP，IPX 等。
- 第 2 层：**数据链路层**在不可靠的物理介质上提供可靠的传输，主要主要为：物理地址寻址、数据封装成帧、流量控制、数据校验、重发等。
- 第 1 层：**物理层**在局域网上传送数据帧，负责电脑通信设备与网络媒体之间的互通，包括针脚，电压，线缆规范，集线器，网卡，主机适配等。

<!--more-->

TCP 是面向连接的协议，其显著特征是在传输之前需要 3 次握手。只有建立会话，服务端与客户端才能互相发送数据，在建立会话的过程中，服务端和客户端分别提供一个 socket，这两个 socket 共同形成连接。服务端与客户端通过 socket 实现两者之间连接的操作。

### 创建 TCP 服务端

```javascript
var net = require('net')
var server = net.createServer(function (socket) {
  // 新的连接
  socket.on('data', function () {
    socket.write('Hello')
  })
  // 断开连接
  socket.on('end', function () {
    console.log('Socket end')
  })
  socket.write('Welcome')
})
server.listen(8124, function () {
  console.log('server bound')
})
```
使用 telnet 工具作为客户端对刚才创建的服务器进行连接。

```shell
$ telnet 127.0.0.1 8124
// 随意输入任意字符
$ Hello
```
同样的，我们也可以对 Domain Socket 进行监听

```javascript
server.listen('/tmp/echo.sock')
```

通过 net 模块自行构建客户端进行会话 client.js:

```javascript
var net = require('net')
var client = net.connect({ port: 8124 }, function() {
  //'connect' listener
  console.log('client connected')
  client.write('world!\r\n')
})
client.on('data', function(data) {
  console.log(data.toString())
  client.end()
})
client.on('end', function() {
  console.log('client disconnected')
})
```
注意，如果是 Domain Socket，在填写选项时，填写 path 即可。

```javascript
var client = net.connect({path: '/tmp/echo.sock'})
```

### TCP 服务的事件

上述代码分为服务端事件和连接事件。

(1) 服务端事件

对于 net.createServer() 创建的服务器而言，它是一个 EventEmitter 实例，它的自定义事件有如下几种。

- listening：在调用 server.listen() 绑定端口或 Domain Socket 后触发，可以写作 server.listen(port, listeningListener)。
- connection：每个客户端 socket 连接到服务器时触发，可以写作 net.createServer()。
- close：服务器关闭时触发。server.close() 会停止接受新的 socket，但是保存已有的连接，等待所有的连接断开后触发。
- error：服务器发生异常时触发。

(2) 连接事件

服务器可以与多个客户端保存连接，每个连接都是典型的可读可写的 Stream 对象。它的自定义事件有如下几种。

- data：当一端调用 write() 发送数据，另外一端触发 data 事件。
- end：当连接中的任一端发送 FIN 数据时，触发该事件。
- connect：客户端 socket 与服务器连接成功适触发。
- drain：rain 和 socket.write() 的返回值强关联，当任意一端调用 write()，当前这端会触发该事件。
- error：异常时触发。
- close：socket 关闭时触发。
- timeout：一定时间连接不再活跃时，该事件触发，通知用户当前连接已经闲置。

TCP socket 为可读可写 Stream 对象，可以用 pipe() 实现管道操作。如下代码实现 echo 服务器。

```javascript
var net = require('net')
var server = net.createServer(function(socket) {
  socket.write('Echo server\r\n')
  socket.pipe(socket)
})
server.listen(1337, '127.0.0.1')
```

TCP 对网络中的小数据包有一定的优化策略：Nagle 算法，用来减少网络中小数据包。Nagle 算法针对这种情况，要求缓冲区数据达到一定数量或者一定时间后才将其发出，并且 Nagle 算法合并小数据包，一次优化网络。但是可能造成数据延迟发送。

Node 中默认开启 Nagle 算法，可以调用 socket.setNoDelay(true) 关闭 Nagle 算法，使得 write() 可以立即发送数据到网络中。

## 构建 UDP 服务

UDP 又称为用户数据包服务，与 TCP 一样属于网络传输层。UDP 不是面向连接的，TCP 中一旦建立连接，所有的会话都是基于连接完成，客户端如果要与另一个 TCP 服务同学，需要另创建一个 socket 处理。在 UDP 中，一个 socket 可以与多个 UDP 服务通信。

UDP 提供面向事物的不可靠传输服务，在网络差的情况下存在丢包的问题，但是它无须连接，资源消耗低，处理快速且灵活，fico适用于那些偶尔丢一两个数据包也不会产生问题的场景，比如音频、视频等。DNS 服务基于 UDP 实现。

### 创建 UDP socket

UDP socket 既可以作为服务端，又可以作为客户端。

```javascript
var dgram = require('dgram')
var socket = dgram.createSocket('upd4')
```
(1) 创建 UDP 服务器

通过调用 dgram.bind(port, [address]) 方法创建 UDP 服务器，接收网路消息。

```javascript
var dgram = require('dgram')
var server = dgram.createSocket('udp4')
server.on('message', function(msg, rinfo) {
  console.log('server got: ' + msg + ' from ' +
    rinfo.address + ':' + rinfo.port)
})
server.on('listening', function() {
  var address = server.address()
  console.log('server listening ' +
    address.address + ':' + address.port)
})
server.bind(41234)
```

(2) 创建 UDP 客户端

```javascript
var dgram = require('dgram')
var message = Buffer.alloc(13, 'Hello Node.js')
var client = dgram.createSocket('udp4')
client.send(message, 0, message.length, 41234, 'localhost',
  function(err, bytes) {
    client.close()
  }
)
```

客户端执行后，服务端输出：

```shell
$ node main.js
$ server listening 0.0.0.0:41234
$ server got: Hello Node.js from 127.0.0.1:61286
```
当 socket 在客户端时，可以调用 send() 方法发生消息到网络。

```javascript
socket.send(buf, offset, length, port, address, [callback])
```

(3) UDP socket 事件

UDP 相对于 TCP 更简单，它只是一个 EventEmitter 的实例，而非 Stream 的实例。它自定义事件如下：

- message：当 UDP socket 侦听网卡端口后，接收到消息时触发该事件。
- listening：当 UDP 开始侦听时触发该事件。
- close：调用 close() 方法时触发该事件，并不再触发 message 事件。
- error：发生异常时触发该事件。

## 构建 HTTP 服务

## 构建 WebSocket 服务

## 网络服务与安全

## 总结