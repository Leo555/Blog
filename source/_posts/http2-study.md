---
title: HTTP/2 学习
date: 2018-03-07 21:35:06
categories: 网络
tags:
- HTTP
- HTTP2
---

## HTTP/2.0 简介

1. HTTP/2 标准于 2015 年发布，目前大部分主流浏览器均已提供支持。
2. HTTP/2 没有改变 HTTP 的应用语义，其请求方法、状态码、URI 等核心概念与 HTTP/1.1 保持一致。
3. HTTP/2 采用了二进制而非明文来打包、传输客户端—服务器间的数据。
4. HTTP/2 的前身是 [SPDY 协议](https://zh.wikipedia.org/wiki/SPDY)。
5. HTTP/2 中 TLS 为可选，但是大厂商如 chrome 和 firefox 表示只会实现基于 TLS 的 HTTP/2。所以要部署 HTTP/2，首先要升级 HTTPS。
6. HTTP/2 通过以下举措，减少网络延迟，提供浏览器加载速度：
    - 对 HTTP 头字段进行数据压缩(即 HPACK 算法)；
    - HTTP/2 服务端推送(Server Push)；
    - 请求管线化；
    - 修复 HTTP/1. 0版本以来未修复的队头阻塞问题；
    - 对数据传输采用多路复用，让多个请求合并在同一 TCP 连接内。

<!--more-->

## HTTP/2 测试

[Akamai http2 demo](https://http2.akamai.com/demo) 这个 Akamai 公司建立的官方 demo，左右两边分别为 HTTP/1.1 和 HTTP/2，两边都同时请求 300 多张图片，从加载时间可以看出 HTTP/2 在速度上的绝对优势。

chrome 商店中有一个工具 [HTTP/2 and SPDY indicator](https://chrome.google.com/webstore/detail/http2-and-spdy-indicator/mpbpobfflnpcgagjijhmgnchggcjblin) 用来查看当前网站是否基于 HTTP/2，添加到 chrome 后如果蓝色闪电亮了说明支持 HTTP/2。

## HTTP/2 新特性

HTTP/2 所有性能增强的核心在于新的二进制分帧层，它定义了如何封装 HTTP 消息并在客户端与服务器之间传输。HTTP/1.x 协议解析基于纯文本，而 HTTP/2 将所有传输的信息分割为更小的消息和帧，并采用二进制格式对它们编码。二进制只有 0 和 1 的组合实现起来方便且健壮。

### 帧、消息、流和 TCP 连接

有别于 HTTP/1.1 在连接中的明文请求，HTTP/2 将一个 TCP 连接分为若干个流（Stream），每个流中可以传输若干消息（Message），每个消息由若干最小的二进制帧（Frame）组成。这也是 HTTP/1.1 与 HTTP/2 最大的区别。 HTTP/2 中，每个用户的操作行为被分配了一个流编号(stream ID)，这意味着用户与服务端之间创建了一个 TCP 通道；协议将每个请求分区为二进制的控制帧与数据帧部分，以便解析。

### 多路复用

在 HTTP/1.1 协议中 「浏览器客户端在同一时间，针对同一域名下的请求有一定数量限制。超过限制数目的请求会被阻塞」这也是我们在站点中使用 CDN 的主要原因。

多路复用原理上还是基于以上 TCP 连接通道，通过单一的 TCP 连接发起和响应多重请求机制。

### 首部压缩 - HPACK 算法 

在 HTTP/1.x 中，header 中带有大量信息，而且每次都要重复发送，HTTP/2 中引入 HPACK 算法用于对 HTTP 头部做压缩。其原理在于：

- 客户端与服务端共同维护一份静态字典（Static Table），其中包含了常见头部名及常见头部名称与值的组合的代码；
- 客户端和服务端根据先入先出的原则，维护一份可动态添加内容的共同动态字典（Dynamic Table）；
- 客户端和服务端共同支持基于相同内容得静态哈夫曼码表的哈夫曼编码（Huffman Coding）。

### 服务器推送 - Server Push

HTTP/2 引入了服务器推送，可以在客户端请求资源之前发送数据，这允许服务器直接提供浏览器渲染页面所需资源，而无须浏览器在收到、解析页面后再提起一轮请求，节约了加载时间。除此之外，服务器还能够缓存数据，在同源策略下，不同页面共享缓存资源成为可能。

### 重置

HTTP/1.1 的有一个缺点是：当一个含有确切值的 Content-Lengt h的 HTTP 消息被送出之后，你就很难中断它了。当然，通常你可以断开整个 TCP 链接（但也不总是可以这样），但这样导致的代价就是需要通过三次握手来重新建立一个新的TCP连接。

一个更好的方案是只终止当前传输的消息并重新发送一个新的。在 HTTP/2 里面，我们可以通过发送 RST_STREAM 帧来实现这种需求，从而避免浪费带宽和中断已有的连接。

## 参考文档

- [HTTP,HTTP2.0,SPDY,HTTPS你应该知道的一些事](http://www.alloyteam.com/2016/07/httphttp2-0spdyhttps-reading-this-is-enough/#prettyPhoto)
- [HTTP/2 资料汇总](https://imququ.com/post/http2-resource.html)
- [HTTP/2.0 相比1.0有哪些重大改进？](https://www.zhihu.com/question/34074946)
- [HTTP/2](https://zh.wikipedia.org/wiki/HTTP/2)
- [http2讲解](https://ye11ow.gitbooks.io/http2-explained/)