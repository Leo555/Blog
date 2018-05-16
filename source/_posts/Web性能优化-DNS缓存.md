---
title: Web 性能优化-缓存-DNS 缓存
date: 2018-05-16 13:32:17
categories: 性能
tags:
- DNS
- HttpDNS
- LDNS
---

## 缓存梗概

缓存技术几乎存在于网络技术发展的各个角落，从数据库到服务器，从服务器到网络，再从网络到客户端，缓存随处可见。跟前端有关的缓存技术主要有：DNS 缓存，HTTP 缓存，浏览器缓存，HTML5 缓存（localhost/manifest）和 service worker 中的 cache api。

## DNS 缓存

当用户在浏览器中输入网址的地址后，浏览器要做的第一件事就是解析 DNS：

(1) 浏览器检查缓存中是否有域名对应的 IP，如果有就结束 DNS 解析过程。浏览器中的 DNS 缓存有时间和大小双重限制，时间一般为几分钟到几个小时不等。DNS 缓存时间过长会导致如果 IP 地址发生变化，无法解析到正确的 IP 地址；时间过短会导致浏览器重复解析域名。

(2) 如果浏览器缓存中没有对应的 IP 地址，浏览器会继续查找操作系统缓存中是否有域名对应的 DNS 解析结果。我们可以通过在操作系统中设置 hosts 文件来设置 IP 与域名的关系。

<!--more-->

(3) 如果还没有拿到解析结果，操作系统就会把域名发送给本地区的域名服务器（LDNS），LDNS 通常由互联网服务提供商（ISP）提供，比如电信或者联通。这个域名服务器一般在城市某个角落，并且性能较好，当拿到域名后，首先也是从缓存中查找，看是否有匹配的结果。一般来说，大多数的 DNS 解析到这里就结束了，所以 LDNS/ISP DNS 承担了大部分的域名解析工作。如果缓存中有 IP 地址，就直接返回，并且会被标记为**非权威服务器应答**。

> 第三步有一点需要注意的是，如果用户在自己电脑里设置了 DNS，比如 Google 的 `8.8.8.8` 或者 CloudFlare 新出的 [`1.1.1.1`](https://blog.cloudflare.com/announcing-1111/)，将不会通过 ISP DNS 服务器解析。

(4) 如果前面三步还没有命中 DNS 缓存，那只能到 Root Server 域名服务器中请求解析了。根域名服务器拿到请求后，首先判断域名是哪个顶级域名下的，比如 `.com`, `.cn`, `.org` 等，全球一共 13 台顶级域名服务器。根域名服务器返回对应的顶级域名服务器（gTLD Server）地址。

(5) 本地域名服务器（LDNS）拿到地址后，向 gTLD Server 发送请求，gTLD 服务器查找并且返回此域名对应的 Name Server 域名服务器地址。这个 Name Server 通常就是用户注册的域名服务器，例如用户在某个域名服务提供商申请的域名，那么这个域名解析任务就由这个域名提供商的服务器来完成。

> 这个过程的解析方式为递归搜索。比如：`https://movie.lz5z.com`，本地域名服务器首先向顶级域名服务器（com 域）发送请求，com 域名服务器将域名中的二级域 `lz5z` 的 IP 地址返回给 LDNS，LDNS 再向二级域名服务器发送请求进行查询，之后不断重复直到 LDNS 得到最终的查询结果。

(6) Name Server 域名服务器会查询存储的域名和 IP 的映射关系表，在正常情况下都根据域名得到目标 IP 地址，连同一个 TTL 值返回给 LDNS。LDNS 会缓存这个域名和 IP 的对应关系，缓存时间由 TTL 值控制。LDNS 会把解析结果返回给用户，DNS 解析结束。


### 清除 DNS 缓存

(1) chrome: `chrome://net-internals/#dns`
(2) 本地 DNS ：Windows: `ipconfig /flushdns`; Linux 和 mac 根据不同的版本有不同的方式


### 减少 DNS 解析我们能做什么？

(1) 减少 DNS 查询，避免重定向。
(2) DNS 预解析：

- 可以通过 meta 信息告诉浏览器，页面需要做 DNS 预解析。 

```html
<meta http-equiv="x-dns-prefetch-control" content="on" />
```

- 通过 link 标签强制 DNS 预解析

```html
<link rel="dns-prefetch" href="https://lz5z.com" />
``` 

(3) 域名发散/域名收敛

- 域名发散

PC 端因为浏览器有域名并发请求限制（chrome 为 6 个），也就是同一时间，浏览器最多向同一个域名发送 6 个请求，因此 PC 端使用域名发散策略，将 http 静态资源放入多个域名/子域名中，以保证资源更快加载。常见的办法为使用 cdn。

- 域名收敛

将静态资源放在同一个域名下，减少 DNS 解析的开销。域名收敛是移动互联网时代的产物，在 LDNS 没有缓存的情况下，DNS 解析占据一个请求的大多数时间，因此，采用尽可能少的域名对整个页面加载速度有显著的提高。

(4) HttpDNS 

DNS 请求使用的是 UDP 协议，虽然没有 TCP 三次握手的开销，但是可能导致弱网环境下（2G，3G）数据丢失的问题。还记得之前[Web 性能优化-页面重绘和回流（重排）](https://lz5z.com/Web%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96-%E9%A1%B5%E9%9D%A2%E9%87%8D%E7%BB%98%E5%92%8C%E5%9B%9E%E6%B5%81/)中提到的 Google 1s 终端首屏渲染标准，假如 DNS 解析出现问题，那可能几秒甚至几十秒都首屏不了了。而且国内牛 X 的运营商的品质你也是知道的，随便劫持一下 DNS 就让你的 web 应用不见天日。

为了应对以上两个问题，HttpDNS 应运而生，原理也非常简单，将 DNS 这种容易被劫持的协议，转而使用 HTTP 协议请求 Domain 与 IP 地址之间的映射。获得正确的 IP 地址后，就不用担心 ISP 篡改数据了。

国内腾讯云和阿里云都有相应的解决方案

- [移动解析HttpDNS](https://cloud.tencent.com/product/hd)
- [HTTPDNS](https://cn.aliyun.com/product/httpdns)

Google 的方案则更近一步，使用 https 协议。
- [DNS-over-HTTPS](https://developers.google.com/speed/public-dns/docs/dns-over-https)


## 参考资料

- [DNS域名解析过程](http://www.cnblogs.com/xrq730/p/4931418.html)
- [无线性能优化：域名收敛](http://taobaofed.org/blog/2015/12/16/h5-performance-optimization-and-domain-convergence/)
- [提升页面访问速度的前端优化大法：DNS预解析](https://www.cloudxns.net/Support/detail/id/1273.html)
- [也谈 HTTPS - HTTPDNS + HTTPS](https://www.jianshu.com/p/6c790b9652a2)