---
title: Web 安全学习
date: 2018-03-01 19:57:53
categories: 安全
tags:
- xss
- csrf
---

去年一家专门做企业安全的公司来我们公司做测试和培训，经过他们一周多的测试，找到了公司多个项目中存在的很多问题，惊奇地发现，我们组的前端项目竟然没有发现一个漏洞。虽然没有找到并不代表没有，但是从中也能看出我们组在这方面还是有些实力的。而我对安全方面可以说是没有多少积累，最近抽时间学习一下 web 安全相关的知识。

## XSS

XSS(Cross Site Script) 跨站脚本攻击，是攻击者利用网站漏洞在网站上注入恶意客户端代码，以获取访问权限，冒充用户，修改 HTML 内容等。恶意内容一般包括 JavaScript，主要方式是获取用户的隐私数据，例如 cookie，session 等。

XSS 攻击可以分为 3 类：存储型、反射型、基于 DOM。

<!--more-->

### 存储型 XSS

存储型 XSS 是指恶意脚本永久存储在目标服务器上，当客户端请求数据时，脚本从服务器上传回并且执行。存储型 XSS 一般存在于 form 表单提交等交互功能，比如发帖留言，提交文本信息等。攻击者将内容经正常的功能提交于数据库存储，当前端页面获得后端从数据库中读取的注入代码时，将其渲染并且执行。

存储型 XSS 需要满足以下 3 个条件：

- 请求提交的数据后端没有转义直接入库。
- 后端从数据库中读取的数据没有转义直接输出给前端。
- 前端拿到数据后没有转义直接渲染 DOM。

因此防止存储型 XSS 需要前端和后端共同努力。

- 后端获取前端数据后，将所有的字段统一进行转义处理。
- 后端输出给前端的数据统一进行转义处理。
- 前端渲染 DOM 的时候对后端返回的数据进行转义处理。

### 反射型 XSS 

服务器接受客户端的请求包，不会存储请求包的内容，只是简单的把用户数据 “反射” 给客户端造成反射型 XSS。常见的有用户搜索，错误信息的处理，这种攻击方式具有一次性。

反射型 XSS 有以下特征：

- 即时性，不经过服务器存储，直接通过 HTTP 请求完成攻击，拿到用户隐私数据
- 攻击者需要诱骗用户点击

下面写一个简单的示例：

```html
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>xss demo</title>
</head>
<body>
    <input ><button>搜索</button>
    <div>搜索结果为： 
        <div id="result"></div>
    </div>
    <script>
        const $ = document.querySelector.bind(document)
        let input = $('input')
        let button = $('button')
        let result = $('#result')
        button.onclick = function () {
            result.innerHTML = input.value
        }
    </script>
</body>
</html>
```

在页面 input 中输入 `<img src="" onerror="alert(document.cookie)">`，可以看到页面弹出警告框，并且显示用户 cookie。

### 基于 DOM 的 XSS

基于 DOM 的 XSS 是指恶意脚本修改页面结构，比如一些免费 wifi 用来植入悬浮广告。

### 基于字符集的 XSS

现阶段很多开源的库都专门针对 XSS 进行转义处理，默认抵御大多数 XSS 攻击，但是还是有很多方法绕过转义规则。假如页面不设置字符集的话，浏览器有自动识别编码的机制，所以黑客通过使用非常规字符集来达到 XSS 注入的功能。

### XSS 攻击检测方法

常用的有以下几种，你也可以根据页面 DOM 结果对其进行修改

```javascript
><script>alert(document.cookie)</script>
='><script>alert(document.cookie)</script>
"><script>alert(document.cookie)</script>
<script>alert(document.cookie)</script>
%3Cscript%3Ealert('XSS')%3C/script%3E
<script>alert('XSS')</script>
<img src="javascript:alert('XSS')">
<img src="http://xxx.com/yyy.png" onerror="alert('XSS')">
<div style="height:expression(alert('XSS'),1)"></div>（这个仅限IE有效）
```

### XSS 预防

XSS 之所以会发生，是因为用户输入的数据变成了代码。所以我们需要对数据进行 HTML Encode 处理，将其中的特殊字符进行编码。

| HTML character | HTML Encoded |
|:-:| :-: |
| < | `&lt;`|
| > | `&gt;` |
| & | `&amp;` |
| ' | `&#039;` |
| " | `&quot;` |
| 空格 | `&nbsp;` |

1. 将重要的 cookie 标记为 HTTP Only。
2. 只允许用户输入期望的数据。
3. 对数据进行 HTML Encode 处理。
4. 过滤或者移除特殊的 HTML 标签，如果 `<script>`，`<iframe>`，`<img>` 等。
5. 过滤特殊的 JavaScript 事件，比如 `onclick`，`onerror`，`onfocus` 等。


## CSRF 

CSRF(Cross-Site Request Forgery) 跨站请求伪造攻击，是指攻击者通过盗用用户登录信息，模拟发送各种请求。攻击者借助聊天软件、论坛、微博等发送链接（有些伪装成短域名），迫使用户去执行攻击者预设的操作。如果当前用户具有管理员权限的话，CSRF 攻击将危及到整个 Web 应用程序。与 XSS 相比，XSS 是利用用户对指定网站的信任，CSRF 是利用网站对用户浏览器的信任。

### CSRF 原理

1. 用户登录信任网站 A，通过验证后，在浏览器中产生 cookie，记录登录状态。
2. 用户在没有登出的情况下登录危险的网站 B。
3. 网站 B 要求访问网站 A，发出一个请求。
4. 浏览器带着 A 产生的 Cookie 访问网站 A，此时 A 不知道中请求是用户发出的还是 B 发出的，A 根据 Cookie 中的信息处理该请求，网站 B 达到了模拟用户请求的目的。

要完成一次 CSRF 攻击，用户必须依次完成两个步骤：

1. 登录受信任网站 A，并在本地生成 Cookie。
2. 在不登出 A 的情况下，访问危险网站 B。

### CRSF 例子

假如一家银行的转账操作的 URL 地址是：`http://lz5z.com/withdraw?account=AccountName&amount=1000&for=PayeeName`，恶意网站 B 中放置一段代码：`<img src=http://lz5z.com/withdraw?account=lizhen&amount=1000&for=BadGuy>`。由于 img、script、iframe 标签不受同源策略现在，假如用户在未登出 A 的情况下打开了 B 网站，在 Cookie 未过期的情况下，用户就会损失 1000 块。

### CSRF 防御

1. 正确使用 GET、POST 请求和 cookie。
2. 检查请求报头中的 Referer 参数。Referer 用来标明请求来源于哪个地址。检查 Referer 字段存在局限性，因其完全依赖浏览器发送正确的 Referer 字段，虽然 HTTP 协议对此字段的内容有明确的规定，但浏览器具体实现的时候可能存在问题，比如早期 IE 中就存在 Referer 可以被修改的 bug。
3. 在非 GET 请求中添加校验 token。
4. 关键请求增加验证码。缺点是用户多次输入验证码，用户体验较差。
5. 渲染表单的时候，为每一个表单生成一个 csrfToken，提交表单的时候，后端做 csrf 验证。
6. 对每个用户创建 token，将其存放于服务端的 session 和客户端的 cookie 中，对每次请求，都检查二者是否一致。缺点是如果用户被 xss 攻破，黑客可能同时获取用户的 cookie。

## DDoS 攻击

DDos(Distributed Denial of Service) 分布式拒绝服务。原理是利用大量的请求造成资源过载，导致服务不可用。DDoS 攻击从层次上可以分为网络层攻击和应用层攻击。

### 网络层 DDoS

网络层 DDoS 攻击包括 SYN Flood、ACK Flood、UDP Flood、ICMP Flood 等。

1. SYN Flood 攻击：主要利用 TCP 三次握手过程中存在的问题，TCP 三次握手过程是要建立连接的双方发送 SYN，SYN + ACK，ACK 数据包，攻击者构造 IP 去发送 SYN 包时，服务器返回的 SYN + ACK 就得不到应答，此时服务器会尝试重新发送，并且至少有 30s 的等待时间，导致资源和服务不可用。
2. ACK Flood 攻击：TCP 连接建立后，所有的数据传输 TCP 都是带有 ACK 标志的，主机收到 ACK 标志的数据包后，需要检查数据包状态合法性。当攻击程序每秒发送 ACK 的速率达到一定程度时，使主机和防火墙负载变大。
3. UDP Flood 攻击：当大量 UDP 数据包发送给受害系统时，可能会导致带宽饱和从而使得合法服务无法请求访问受害系统。
4. ICMP Flood 攻击：ICMP（互联网控制消息协议）洪水攻击是通过向未良好设置的路由器发送广播信息占用系统资源的做法。

### 应用层 DDoS

应用层 DDoS 攻击不是发生在网络层，是发生在 TCP 建立握手成功之后，应用程序处理请求的时候，现在很多常见的 DDoS 攻击都是应用层攻击。

1. CC 攻击：Challenge Collapasar，就是针对消耗资源比较大的页面不断发起不正常的请求，导致资源耗尽。
2. DNS Flood：攻击者向服务器发送大量的域名解析请求，通常请求解析的域名是随机生成或者是网络世界上根本不存在的域名，域名解析的过程给服务器带来了很大的负载。
3. HTTP 慢连接攻击：针对 HTTP 协议，先建立起 HTTP 连接，设置一个较大的 Conetnt-Length，每次只发送很少的字节，让服务器一直以为 HTTP 头部没有传输完成，这样连接一多就很快会出现连接耗尽。


### 防御方式

1. 防火墙：通过设置防火墙规则，比如允许或者拒绝特点通讯协议、端口或者 IP 地址。
2. 交换机：通过使用交换机的访问控制，比如限速、假 IP 过滤、流量整形，深度包检测等功能，可以检测并过滤拒绝服务攻击。
3. 路由器：与交换机类似。
4. 流量清洗：当流量被送到 DDoS 防护清洗中心时，通过采用抗 DDoS 软件处理，将正常流量与恶意流量区分。


## 参考资料

- [跨站脚本](https://zh.wikipedia.org/zh-cn/跨網站指令碼)
- [常见 Web 安全攻防总结](https://zoumiaojiang.com/article/common-web-security/)
- [跨站请求伪造](https://zh.wikipedia.org/wiki/%E8%B7%A8%E7%AB%99%E8%AF%B7%E6%B1%82%E4%BC%AA%E9%80%A0)
- [拒绝服务攻击](https://zh.wikipedia.org/wiki/%E9%98%BB%E6%96%B7%E6%9C%8D%E5%8B%99%E6%94%BB%E6%93%8A)



