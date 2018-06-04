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

TCP 与 UDP 都属于网络传输层协议，如果要构造高效的网络应用，就应该从传输层进行着手。但是一般使用应用层协议就能满足我们大部分开发需求。Node 提供基本的 http 和 https 模块用于 HTTP 和 HTTPS 的封装。

```javascript
var http = require('http')
http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/plain'})
  res.end('Hello World')
}).listen(1337, '127.0.0.1')
console.log('Server running at http://127.0.0.1:1337/')
```

### HTTP

HTTP 构建于 TCP 之上，属于应用层协议。

使用 curl 查看网络通信的报文信息。

```shell
$ curl -v http://127.0.0.1:1337
* About to connect() to 127.0.0.1 port 1337 (#0)
*   Trying 127.0.0.1...
* Connected to 127.0.0.1 (127.0.0.1) port 1337 (#0)
> GET / HTTP/1.1
> User-Agent: curl/7.29.0
> Host: 127.0.0.1:1337
> Accept: */*
> 
< HTTP/1.1 200 OK
< Date: Mon, 04 Jun 2018 15:34:30 GMT
< Connection: keep-alive
< Transfer-Encoding: chunked
< 
Hello World
* Connection #0 to host 127.0.0.1 left intact
* Closing connection #0 
```

报文解析：

(1) TCP 三次握手

```shell
* About to connect() to 127.0.0.1 port 1337 (#0)
*   Trying 127.0.0.1...
* Connected to 127.0.0.1 (127.0.0.1) port 1337 (#0)
```
(2) 客户端向服务端发送请求报文

```shell
> GET / HTTP/1.1
> User-Agent: curl/7.29.0
> Host: 127.0.0.1:1337
> Accept: */*
> 
```
(3) 服务器响应客户端内容

```shell
< HTTP/1.1 200 OK
< Date: Mon, 04 Jun 2018 15:34:30 GMT
< Connection: keep-alive
< Transfer-Encoding: chunked
< 
Hello World
```

(4) 结束会话

```shell
* Connection #0 to host 127.0.0.1 left intact
* Closing connection #0 
```

从上述报文信息中可以看出 HTTP 的特点：基于请求响应式的，以一问一答的方式实现服务，虽然基于 TCP 会话，但是本身并无会话的特点。

### http 模块

Node 的 http 模块包含对 HTTP 处理的封装，在 Node 中，HTTP 服务继承自 TCP 服务（net 模块），它能够与多个客户端保持连接，采用事件驱动的形式，并不为每一个连接创建额外的线程或者进程，占用很低的内存，并且实现高并发。

HTTP 服务与 TCP 服务的区别在于，开启 keepalive 后，一个 TCP 会话可以用于多次请求和响应，TCP 以 connection 为单位进行服务，HTTP 服务以 request 为单位进行服务。http 模块即是将 connection 到 request 的过程进行了封装。

除此之外，http 模块将连接所用的 socket 的读写抽象为 ServerRequest 和 ServerResponse 对象，它们分别对应请求和响应操作。在请求产生的过程中，http 模块拿到连接中传来的数据，调用二进制模块 http_parser 进行解析，在解析完请求报文的报头后，触发 request 事件，调用用户的业务逻辑。

(1) HTTP 请求

对于 TCP 连接的读操作，http 模块将其封装为 ServerRequest 对象。报头通过 http_parser 进行解析。

```shell
> GET / HTTP/1.1
> User-Agent: curl/7.29.0
> Host: 127.0.0.1:1337
> Accept: */*
> 
```
- req.method 属性： GET
- req.url 属性： /
- req.httpVersion 属性： 1.1
其余报头是很规律的 key: Value 格式，被解析后放置在 req.headers 属性上传递给业务逻辑调用。

```shell
headers: {
  'user-agent': 'curl/7.29.0',
  host: '127.0.0.7:1337',
  accept: '*/*'
}
```
报文体部分则抽象为一个只读流对象，如果业务逻辑需要读取报文体中的数据，则要在这个数据流结束后才能进行操作。

```javascript
function (req, res) {
  var buffers = []
  req.on('data', function (trunk) {
    buffers.push(trunk)
  }).on('end', function () {
    var buffer = Buffer.concat(buffers)
    res.end('')
  })
}
```

(2) HTTP 响应

HTTP 响应对象封装了底层连接的写操作，可以将其看作一个可写的流对象，通过 res.setHeader() 和 res.writeHead() 响应报文头部信息。

```javascript
res.writeHead(200, {'Content-Type': 'text/plain'})
```
转化为报文如下：

```shell
< HTTP/1.1 200 OK
< Content-Type: text/plain
```

setHeader 可以进行多次调用，但只有调用 writeHead 后，报文才会写入到连接中，此外，http 模块还会自动设置一些头信息。

```shell
< Date: Mon, 04 Jun 2018 15:34:30 GMT
< Connection: keep-alive
< Transfer-Encoding: chunked
< 
```

报文体则是通过调用 res.write() 和 res.end() 方法实现，区别在于 res.end() 会调用 write() 发送数据，然后发送信号告知服务器这次响应结束。

响应结束后，HTTP 服务器可能将当期连接用于下一次请求，或者关闭连接。另外，无法服务器在处理业务逻辑时是否发生异常，务必在结束时调用 res.end() 结束请求，否则客户端将一直处于等待的状态。当然也可以通过延迟 res.end() 的方式实现客户端与服务器之间的长连接，但结束时务必关闭连接。

(3) HTTP 服务的事件

HTTP 服务器抽象了一些事件，供应用层使用，服务器也是一个 EventEmitter 实例。

- connection 事件：HTTP 请求响应前触发，客户端与服务器建立底层的 TCP 连接时触发。
- request 事件：建立 TCP 连接后，http 模块底层将在数据流中抽象出 HTTP 请求和响应，当解析出 HTTP 请求头时，触发该事件。
- close 事件：调用 server.close() 方法停止接受新的连接，并且已有连接全部断开时触发。
- checkContinue 事件：客户端发送较大的数据时，并不会直接将数据发送，而是先发一个头部带 `Expect: 100-continue` 的请求到服务器，服务器将触发 checkContinue 事件。如果服务器没有监听这个事件，则会自动响应客户端 100 Continue 的状态码，表示接受数据上传。如果不接受，或者客户端数据较多时，响应 400 Bad Request 拒绝客户端继续发送数据。
- connect 事件：当客户端发起 CONNECT 请求时触发。而发起 CONNECT 请求通常在 HTTP 代理时出现，如果不监听该事件，发起请求的连接将会关闭。
- upgrade 事件：客户端要求升级连接协议时触发。
- clientError 事件：连接的客户端触发 error 事件时，这个错误会传递到服务器，此时触发该事件。

(4) HTTP 客户端

http 模块通过调用 http.request(options, connect) 构造客户端。与上文的 curl 大致相同：

```javascript
var options = {
  hostname: '127.0.0.1',
  port: 1334,
  path: '/',
  method: 'GET'
}
var req = http.request(options, function (res) {
  console.log('STATUS: ' + res.statusCode)
  console.log('HEADERS: ' + JSON.stringify(res.headers))
  res.setEncoding('utf8')
  res.on('data', function (chunk) {
    console.log(chunk)
  })
})
req.end()
```
执行：

```shell
$ node client.js
STATUS: 200
HEADERS: {"date":"Mon, 04 Jun 2018 15:34:30 GMT","connection":"keep-alive","transfer-encoding":"chunked"}
Hello World 
```
options 中选项有如下这些：

- host
- hostname
- port：默认 80
- localAddress：建立网络连接的本地网卡
- socketPath
- method：默认为 GET
- path：请求路径，默认为 /
- headers
- auth: Basic 认证，这个值将被计算成请求头中的 Authorization 部分。

(5) HTTP 代理

http 提供的 ClientRequest 对象也是基于 TCP 层实现的，在 keepalive 的情况下，一个底层的会话连接可以用于多次请求。为了重用 TCP 连接，http 模块包含一个默认的客户端代理对象 http.globalAgent。

http.globalAgent 对每个服务器端（host + port）创建的连接进行管理，默认情况下，每个请求最多可以创建 5 个连接，它的实质是一个连接池。

调用 HTTP 客户端对一个服务器发起 10 次 HTTP 请求时，其实质只有 5 个请求处于并发状态，后续的请求需要等待某个请求完成后才真正发出，与浏览器对同一域名的并发限制相同。

```javascript
var agent = new http.Agent({
  maxSockets: 10
})
var options = {
  hostname: '127.0.0.1',
  port: 1334,
  path: '/',
  method: 'GET',
  agent: agent
}
```
也可以设置 agent 选项为 false，以脱离连接池管理，使请求不受并发限制。

(6) HTTP 客户端事件

- response：客户端收到服务器的响应时触发。
- socket：当底层连接池中简历的连接分配给当前请求对象时触发该事件。
- connect：客户端向服务器发起 CONNECT 请求时，如果服务器响应了 200 状态码，客户端触发。
- upgrade：客户端发起 Upgrade 请求时，如果服务器响应了 101 Switching Protocols 状态，客户端触发。
- continue：客户端向服务器发起 Expect: 100-continue 头信息，服务服务器响应 100 Continue 状态，客户端触发。
