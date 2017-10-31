---
title: 迁移 github pages 到 coding.net
date: 2017-10-27 15:37:59
categories: 杂记
tags:
- github pages
- coding.net
- SSL
---

由于众所周知的原因，github 在国内时不时不能访问，虽然有各种办法可以跨越屏障，但是你不能用预测未来会发生哪些事情，于是决定将博客迁移到国内，[coding](https://coding.net) 是一个不错的选择，主要有以下几个优点。

- 国内速度更快
- 自带 SSL，且免费
- 五个免费的私人仓库
- 功能较全: pages, webIDE, CI 等
- 经过一段时间迭代，产品经得起考验

<!--more-->

## 步骤

首先直接从 github 把 blog 项目导入到 coding，项目名称命名为 [name].coding.me，相当于 github 上面的 [name].github.io。

进入项目代码，点击左侧 『代码 -> Pages 服务』，选择静态 Pages 服务，coding 部署来源仅支持 coding-pages 分支和 master 分支，所以选择 master 分支。

<img src="/assets/img/coding.png" alt="我是一只图片">

这时，通过 [name].coding.me 就能够访问页面了，但是这还远远不够，我们还需要添加自定义域名和开启 SSL 服务。

## 自定义域名 SSL

首先确保项目根目录中有 CNAME 文件，里面是自己的域名，比如我的域名 **lz5z.com**，然后在 coding 页面自定义域名中输入此域名，并且开启强制 HTTPS 访问。

<img src="/assets/img/coding_pages.png" alt="我是一只图片">

然后去自己域名服务商那里修改 DNS Server，我的域名在万网购买，于是在万网控制台添加一个 CNAME 记录和一个 A 记录，加上之前 github pages 添加的主机记录，截图如下。

<img src="/assets/img/coding_dns.png" alt="我是一只图片">

红色部分为新添加的记录，如果不知道 coding.net 的 ip 地址的话，可以手动 ping 一下。

由于之前使用 cloudflare 的免费 SSL 服务而将 DNS Server 的地址指向了 cloudflare，这个时候把地址改回万网默认配置即可。

经过漫长的等待，DNS 解析生效，此时通过 https://lz5z.com 访问，发现域名已经生效了，但是存在两个问题：

- 国内地址访问网站， SSL 没有问题，但是国外访问时 SSL 会报错，在 chrome 中有一个不能忍受的警告。
- 每次访问博客地址的时候，首先会看到一个 coding 的广告，然后再重定向到自己要访问的地址，这也是不能忍受的。

### 解决 SSL 证书错误

国外地址访问网站报 SSL 不合法主要是因为这个原因：

> 注意：申请 SSL/TLS 证书需要通过 Let's Encrypt 的 HTTP 方式验证域名所有权。如果您的域名在境外无法访问 Coding Pages 的服务器，将导致 SSL/TLS 证书申请失败。

查阅资料发现大家的解决方式都是设置双线解析，也就是国外访问通过 github pages，国内访问通过 coding.net，因此要为域名设置解析路线，如果域名服务商自定义解析路线，可以选择免费的 [DNSPod](https://www.dnspod.cn/) 做 DNS 解析。

DNSPod 提供双线解析的原理我不是很明白，而且比较困惑的是 github pages 自定义域名原生是不资辞 SSL 的，之前的做法是使用 cloudflare 的 SSL 服务进行重定向，假如使用双线解析的话，那国外地址为什么能够看到合法的 SSL 呢？

而且按照网上的做法改了 DNS 解析后，并没有发生双线解析，无论是国外还是国内都是解析到 coding.net，但是解决了国外地址访问报 SSL 证书错误的问题。着实很奇怪，以下是我的做法。

### DNSPod

注册 -> 登录 -> 实名认证 -> 进入控制台 -> 添加域名

添加域名的时候 DNSPod 会自动监测域名之前的解析情况，然后用 DNSPod 服务器提供的 DNS 地址替代万网提供的地址。

DNSPod DNS 记录如下：

<img src="/assets/img/coding_dnspod.png" alt="我是一只图片">

更改万网 DNS Server 为 DNSPod:

<img src="/assets/img/coding_dnsserver.png" alt="我是一只图片">

再次经过漫长的等待，DNS 生效后，无论国内国外访问网站都是合法的 SSL，excited！

### 解决 coding 广告后重定向

每次新建隐私窗口打开网站都是先看 coding 的广告，然后再重定向到之前的地址，这是极差的用户体验，不过 coding 官方提供了解决办法，简单的就是购买 coding 的会员，免费的办法就是在网站首页任意位置放置「Hosted by Coding Pages」的文字版或图片版，具体办法参考 coding pages 服务的说明。添加之后勾选 **已放置 Hosted by Coding Pages**，等待一天或者两天就生效了。

## 总结

这次切换 github pages 到 coding.net 真的费时费力，不过好在现在网页能够正常访问，而且速度也比之前快很多，所以还是比较满意的。