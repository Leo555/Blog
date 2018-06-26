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
2. 



