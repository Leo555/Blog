---
title: Web 性能优化-缓存-HTTP 缓存
date: 2018-05-16 16:39:55
categories: 性能
tags:
- HTTP
- Cache
---

## 浏览器缓存

HTTP 缓存通常要配合客户端（浏览器）使用才能发挥效果，所以又被称之为浏览器缓存，是 Web 性能优化的一大利器。

### 缓存类型

浏览器缓存分为强缓存和协商缓存。

(1) 强缓存：浏览器在加载资源的时候，根据资源的 HTTP Header 判断它是否命中强缓存，如果命中，浏览器直接从自己的缓存中读取资源，不会发请求到服务器。

(2) 协商缓存：当强缓存没有命中的时候，浏览器向服务器发送请求，服务器端依据资源的另外一些  HTTP Header 验证这个资源是否命中协商缓存，如果协商缓存命中，服务器会将这个请求返回 304，浏览器从缓存中加载这个资源；若未命中请求，服务端返回 200 并将资源返回客户端，浏览器更新本地缓存数据。

<!--more-->

另外一种分类方式，可以将浏览器缓存分成 HTTP 协议缓存和非 HTTP 协议缓存。

(1) 非 HTTP 协议缓存：使用 HTML Meta 标签，开发者可以告诉浏览器是否缓存当前页面。

```html
<META HTTP-EQUIV="Pragma" CONTENT="no-cache">
<META HTTP-EQUIV="Expires" CONTENT="0">
```

上述代码告诉浏览器当前页面不能被缓存，每次访问都要去服务端拉取。只有部分浏览器支持，缓存代理服务器不支持。

(2) HTTP 协议缓存：通过在 HTTP 协议头里面定义一些字段来告诉浏览器当前资源是否缓存，比如  Cache-Control, Expires, Last-Modified, Etag 等。

## HTTP 缓存


### HTTP/1.0 缓存字段

(1) **Pragma**：设置资源是否缓存，no-cache 表示不缓存。在 HTTP/1.1 中被 Cache-Control 替代，所以优先级低于 Cache-Control。

(2) **Expires**：设置资源过期时间，Expires 的值对应一个 GMT(格林尼治时间) 来告诉浏览器资源什么时间过期。缺点是如果客户端与服务端时间相差很大，会导致时间计算不精确，在 HTTP/1.1 中被 max-age 取代。

### HTTP/1.1 相关字段

(1) **[Cache-Control](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/Cache-Control)**：设置一个相对的时间，在缓存判定的时候，由浏览器进行判断。Cache-Control 的值可以是 public, private, no-cache, no-store, no-transform 等。

- max-age(单位为 s) 设定缓存最大的有效时间，`Cache-Control: max-age=3600` 表示该资源在浏览器端一个小时内均有效。

- s-maxage(单位是 s) 设定共享缓存时间，比如 CDN 或者代理。
- no-store 网络资源不缓存，每次都到服务器上拉取。
- no-cache 表示网络资源可以缓存一份，但使用前必须询问服务器此资源是不是最新的。
- public 表明响应可以被任何对象（客户端，代理服务器等）缓存。
- private 表明响应只能被单个用户缓存，其它用户或者代理服务器不能缓存这些数据。


(2) **Last-Modified/If-Modified-Since:**：

- Last-Modified 表示响应资源最后修改时间，需要与 Cache-Control 共同使用，是检查服务端资源更新的一种方式。

- If-Modified-Since 表示资源过期时（超过 max-age），发现资源具有 Last-Modified 声明，则再次向web服务器请求时带上头 If-Modified-Since，表示请求时间。web 服务器收到请求后发现 Header 中有 If-Modified-Since 则与被请求资源的最后修改时间进行比对。若最后修改时间较新，说明资源又被改动过，则响应整片资源内容（写在响应消息包体内），HTTP 200；若最后修改时间较旧，说明资源无新修改，则响应HTTP 304 (无需包体，节省浏览)，告知浏览器继续使用所保存的cache。

(3) **Etag/If-None-Match**：

- Etag 是根据资源内容生成的一段 hash 字符串，标识资源的状态，由服务端产生。浏览器将这串字符串传回服务器，验证资源是否发生修改。

- If-None-Match 表示当资源过期时（超过 max-age），发现资源有 Etag 声明，向 web 服务器发送请求时带上 If-None-Match （Etag 值）。web 服务器收到请求后发现 Header 中带有 If-None-Match 则与被请求资源的相应校验串进行对比，决定返回 200 或者 304。


### Last-Modified vs Etag

Etag 可以解决 Last-Modified 存在的一些问题：

- 某些服务器不能精确得到资源的最后修改时间，这样就无法通过最后修改时间判断资源是否更新。
- 如果资源修改非常频繁，而 Last-modified 只能精确到秒。
- 一些资源的最后修改时间改变了，但是内容没改变，使用 ETag 就认为资源还是没有修改的。

## 浏览器行为

(1) F5 刷新页面时，会跳过强缓存，检查协商缓存。
(2) ctrl + F5 强制刷新页面时，之间从服务端加载数据，跳过强缓存和协商缓存。


## 参考资料

- [HTTP Headers](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers)
- [浅谈浏览器http的缓存机制](https://www.cnblogs.com/vajoy/p/5341664.html)
- [Web缓存相关知识整理](https://segmentfault.com/a/1190000009638800)
- [浅谈Web缓存](http://www.alloyteam.com/2016/03/discussion-on-web-caching/)
- [详谈Web缓存](https://segmentfault.com/a/1190000006741200)