---
title: 《深入浅出Node.js》-WebSocket
date: 2018-06-08 11:58:26
categories: Node
tags:
- WebSocket
---

## 构建 WebSocket 服务

WebSocket 与 Node 之间的配合可以说是天作之合：WebSocket 客户端基于事件的编程模型与 Node 中自定义事件相差无几；WebSocket 实现了客户端与服务器之间的长连接，而 Node 在与大量客户端之间保持高并发连接方面非常擅长。

WebSocket 有以下好处：

1. 客户端与服务器之间只需要建立一个 TCP 连接，可以使用更少的连接。
2. WebSocket 服务器可以推送数据到客户端，比 HTTP 请求响应模型更灵活。
3. WebSocket 协议头更加轻量，减少数据传输。
4. WebSocket 既可以发送文本，也可以发送二进制数据。
5. WebSocket 没有同源限制，客户端可以与任意服务器通信。
6. 建立在 TCP 协议之上，与 HTTP 协议有很好的兼容性，默认端口也是 80 和 443。

<!--more-->

WebSocket 在客户端的应用示例：

```javascript
var ws = new WebSocket("wss://127.0.0.1:12010/updates")

ws.onopen = function(evt) { 
  setInterval(function() {
    if (socket.bufferedAmount == 0)
      socket.send(getUpdateData())
  }, 50)
}

ws.onmessage = function(evt) {
  console.log( "Received Message: " + evt.data);
  ws.close()
}

ws.onclose = function(evt) {
  console.log("Connection closed.")
}
```

上述客户端代码与服务器建立 WebSocket 连接后，每 50 毫秒向服务器发送一次数据。并且通过 onmessage 接受服务端传来的数据。

在 WebSocket 之前，服务器与客户端通信最高效的是 Comet 技术，实现原理依赖于长轮询或 iframe 流。长轮询是客户端向服务器发起请求，服务器只有在超时或者数据响应时断开连接（res.end()），客户端在收到数据或者超时后重新发起请求，这个请求拖着长长的尾巴，所以用彗星命名。

使用 WebSocket 技术，客户端只需要保持一个 TCP 连接即可完成双向通信，无需频繁断开连接和重发请求。

WebSocket 协议主要分两个部分：握手和数据传输。

### WebSocket 握手

客户端建立连接时，通过 HTTP 发起报文请求：

```javascript
GET /chat HTTP/1.1
Host: server.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Protocol: chat, superchat
Sec-WebSocket-Version: 13 
```

其中 Upgrade 表示请求服务器升级协议为 WebSocket；Sec-WebSocket-Protocol 和 Sec-WebSocket-Version 表示协议和版本号；Sec-WebSocket-Key 用于安全校验，是一个随机生成的 Base64 编码的字符串，与服务器响应首部的 Sec-WebSocket-Accept 是配套使用的，为 WebSocket 提供基本防护。其对应的算法如下：

将 Sec-WebSocket-Key 跟 `258EAFA5-E914-47DA-95CA-C5AB0DC85B11` 拼接，通过 SHA1 计算出摘要，并转成 base64 字符串。

```javascript
var crypto = require('crypto')
var magic = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
var val = crypto.createHash('sha1')
				.update(secWebSocketKey + magic)
				.digest('bash64')
```

服务器处理完请求后，响应的报文如下：

```javascript
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
Sec-WebSocket-Protocol: chat 
```

客户端收到响应后，会校验 Sec-WebSocket-Accept 的值，如果成功，就开始接下来的数据传输。

### WebSocket 数据传输

握手顺利完成后，就开始 WebSocket 数据帧协议，协议升级过程如下图：

<img src="/assets/img/webSocket-upgrade.png" alt="webSocket-upgrade">

握手完成后，客户端的 onopen() 将会被触发。服务器端没有 onopen() 方法，为了完成 TCP socket 事件到 WebSocket 事件的封装，需要在接收数据时进行处理，WebSocket 的数据帧协议在底层的 data 事件上封装完成的：

```javascript
WebSocket.prototype.setSocket = function (socket) {
  this.socket = socket
  this.socket.on('data', this.receiver)
}
```

客户端调用 send() 发送数据时，服务端出发 onmessage()；当服务器调用 send() 发送数据时，客户端的 onmessage() 触发。send() 发送的数据会被协议封装为一帧或者多帧，然后逐帧发送。

为了安全考虑，客户端需要对发送的数据帧进行掩码处理，服务器一旦收到无掩码帧的数据，连接将关闭；而服务器的数据则不需要掩码处理。

### 客户端 [API](https://developer.mozilla.org/zh-CN/docs/Web/API/WebSocket)

(1) WebSocket 对象作为构造函数，用于新建 WebSocket 实例。

```javascript
var ws = new WebSocket('ws://localhost:8080')
```

(2) readyState 

- CONNECTING	0	连接还没开启。
- OPEN	1	连接已开启并准备好进行通信。
- CLOSING	2	连接正在关闭的过程中。
- CLOSED	3	连接已经关闭，或者连接无法建立。

(3) 事件

```javascript
ws.onopen = function () {}
ws.onclose = function () {}
ws.onmessage = function () {
  // 服务器返回的数据可能是文本，也可能是二进制	
}
ws.onerror = function () {}
```


### 基于 Node 的 WebSocket 服务端实现

[socket.io](https://socket.io/)

```javascript
var app = require('express')()
var http = require('http').Server(app)
var io = require('socket.io')(http)

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html')
})

io.on('connection', function(socket){
  console.log('a user connected')
})

http.listen(3000, function(){
  console.log('listening on *:3000')
})
```

## 总结

在所有的 WebSocket 服务器实现中，Node 最贴近 WebSocket 的使用方式：

- 基于事件的编程接口
- 基于 JavaScript，API 在服务端与客户端高度相似

另外，Node 基于事件驱动的方式使得它应对 WebSocket 这类长连接的应用场景时可以轻松处理大量并发请求。