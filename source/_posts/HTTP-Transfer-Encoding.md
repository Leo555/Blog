---
title: HTTP 协议 Transfer-Encoding
date: 2018-07-09 00:08:27
categories: 网络
tags:
- HTTP
- Transfer-Encoding  
---

## 简介

Transfer-Encoding (传输编码) 是常见的 HTTP 头 字段，表示将实体安全传递给用户所采用的编码形式。与另外一个更为常见的 Content-Encoding 不同，Content-Encoding 表示内容编码，通常用于对实体内容进行压缩编码，比如 gzip，deflate 等。而 Transfer-Encoding 不会减少实体内容传输大小，但是会改变实体传输的形式。Content-Encoding 和 Transfer-Encoding 二者是相辅相成的，对于一个 HTTP 报文，很可能同时进行了内容编码和传输编码。

在 HTTP 请求头中，Transfer-Encoding 被称为 TE，表示浏览器预期接受的传输编码方式，可使用 Response 头 Transfer-Encoding 字段中的值，比如 chunked；另外还可用 "trailers" 这个值来表明浏览器希望在最后一个大小为 0 的块之后还接收到一些额外的字段。

<!--more-->

## HTTP 长连接

HTTP/1.0 后期引入长连接的概念，通过 `Connection: keep-alive` 实现，服务端和客户端通过这个头部告诉对方发送完数据后不需要断开 TCP 连接，后面可以继续使用。HTTP/1.1 则将其变为默认规则，只要不发送 `Connection: close`，所有的连接均保持为长连接。

### 长连接存在的问题

持久链接需要服务器在开始发送消息体前发送 Content-Length 消息头字段，但是对于动态生成的内容来说，在内容创建完之前是不可知的。在 [HTTP 协议中的 Transfer-Encoding](https://imququ.com/post/transfer-encoding-header-in-http.html) 这篇文章中，作者举了两个例子来阐述长连接存在的问题。使用 node 创建 server。

```javascript
require('net').createServer(function(sock) {
  sock.on('data', function(data) {
    sock.write('HTTP/1.1 200 OK\r\n')
    sock.write('\r\n')
    sock.write('hello world!')
    sock.destroy()
  })
}).listen(8080, '127.0.0.1')
```

使用 `sock.destroy()` ，则每次发送完请求后，就关闭 TCP 连接，假如去掉 `sock.destroy()`，服务变成长连接，但是请求的状态一直在 pending，因此浏览器无法确认数据是否传输完成，只能一直等待。通过设置 `Content-Length` 来解决这个问题。

```javascript
require('net').createServer(function(sock) {
  sock.on('data', function(data) {
    sock.write('HTTP/1.1 200 OK\r\n')
    sock.write('Content-Length: 12\r\n')
    sock.write('\r\n')
    sock.write('hello world!')
  })
}).listen(8080, '127.0.0.1')
```

这样浏览器能正常接收响应数据，通过 `Content-Length` 判断实体已经结束，但是如果 `Content-Length` 计算错误会导致数据异常，并且对于动态生成的内容来说，在内容创建完之前其长度是不可知的。

## [Transfer-Encoding: chunked (分块传输编码)](https://zh.wikipedia.org/wiki/%E5%88%86%E5%9D%97%E4%BC%A0%E8%BE%93%E7%BC%96%E7%A0%81)

`Transfer-Encoding` 的出现正是为了解决这个问题。如果一个 HTTP 消息（请求消息或应答消息）的 Transfer-Encoding 消息头的值为 chunked，那么，消息体由数量未定的块组成，并以最后一个大小为 0 的块为结束。分块传输编码只在 HTTP/1.1 中提供。

使用方式也很简单，在响应头部加上 `Transfer-Encoding: chunked` 后，就表示这个报文采用分块编码。每一个非空的块都以该块包含数据的字节数（字节数以十六进制表示）开始，跟随一个 CRLF （回车及换行），然后是数据本身，最后以一个大小为 0 的块 + CRLF 结束。

```javascript
require('net').createServer(function(sock) {
  sock.on('data', function(data) {
    sock.write('HTTP/1.1 200 OK\r\n')
    sock.write('Transfer-Encoding: chunked\r\n')
    sock.write('\r\n')

    sock.write('24\r\n') // (36 字符 => 十六进制: 0x24)
    sock.write('This is the data in the first chunk \r\n')

    sock.write('1b\r\n') // (27 字符 => 十六进制: 0x1b)
    sock.write('and this is the second one \r\n')

    sock.write('3\r\n') // (3 字符 => 十六进制: 0x03)
    sock.write('con\r\n')

    sock.write('8\r\n') // (8 字符 => 十六进制: 0x08)
    sock.write('sequence\r\n')

    sock.write('0\r\n') // 块大小为 0 表示数据传输结束
    sock.write('\r\n')  // 消息最后以 CRLF 结尾
  })
}).listen(8080, '127.0.0.1')
```
用浏览器访问 `http://localhost:8080/` 可以看到 "This is the data in the first chunk and this is the second one consequence"。

## Transfer-Encoding 其它定义方法

1. `Transfer-Encoding: chunked`：数据以一系列分块的形式进行发送。 Content-Length 首部在这种情况下不被发送。
2. `Transfer-Encoding: compress`：采用 Lempel-Ziv-Welch (LZW) 压缩算法，这种内容编码方式已经被大部分浏览器弃用。
3. `Transfer-Encoding: deflate`：采用 zlib 结构 (在 RFC 1950 中规定)，和 deflate 压缩算法(在 RFC 1951 中规定)。
4. `Transfer-Encoding: gzip`：表示采用 Lempel-Ziv coding (LZ77) 压缩算法，以及 32 位 CRC 校验的编码方式。这个编码方式最初由 UNIX 平台上的 gzip 程序采用。
5. `Transfer-Encoding: identity`：用于指代自身（例如：未经过压缩和修改）。除非特别指明，这个标记始终可以被接受。
 
## 参考资料

- [分块传输编码](https://zh.wikipedia.org/wiki/%E5%88%86%E5%9D%97%E4%BC%A0%E8%BE%93%E7%BC%96%E7%A0%81)
- [HTTP 协议中的 Transfer-Encoding](https://imququ.com/post/transfer-encoding-header-in-http.html)
- [Transfer-Encoding](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/Transfer-Encoding)