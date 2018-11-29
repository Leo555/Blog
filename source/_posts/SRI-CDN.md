---
title: 使用 SRI 解决 CDN 劫持
date: 2018-11-25 13:05:48
categories: HTML
tags:
- CDN
- intergrity
---

## SRI 简介

[SRI](https://developer.mozilla.org/zh-CN/docs/Web/Security/%E5%AD%90%E8%B5%84%E6%BA%90%E5%AE%8C%E6%95%B4%E6%80%A7) 全称 Subresource Integrity - 子资源完整性，是指浏览器通过验证资源的完整性（通常从 CDN 获取）来判断其是否被篡改的安全特性。

通过给 link 标签或者 script 标签增加 integrity 属性即可开启 SRI 功能，比如：

```html
<script type="text/javascript" src="//s.url.cn/xxxx/xxx.js?_offline=1" integrity="sha256-mY9nzNMPPf8oL3CJss7THIEoXAC2ToW1tEX0NBhMvuw= sha384-ncIKElSEk2OR3YfjNLRSY35mzt0CUwrpNDVS//iD3dF9vxrWeZ7WPlAPJTqGkSai" crossorigin="anonymous"></script>
```

integrity 值分成两个部分，第一部分指定哈希值的生成算法（sha256、sha384 及 sha512），第二部分是经过 base64 编码的实际哈希值，两者之间通过一个短横（-）分割。integrity 值可以包含多个由空格分隔的哈希值，只要文件匹配其中任意一个哈希值，就可以通过校验并加载该资源。上述例子中我使用了 sha256 和 sha384 两张 hash 方案。


<!--more-->

> 备注：`crossorigin="anonymous"` 的作用是引入跨域脚本，在 HTML5 中有一种方式可以获取到跨域脚本的错误信息，首先跨域脚本的服务器必须通过 Access-Controll-Allow-Origin 头信息允许当前域名可以获取错误信息，然后是当前域名的 script 标签也必须声明支持跨域，也就是 crossorigin 属性。link、img 等标签均支持跨域脚本。如果上述两个条件无法满足的话， 可以使用 `try catch` 方案。

## 为什么要使用 SRI

在 Web 开发中，使用 CDN 资源可以有效减少网络请求时间，但是使用 CDN 资源也存在一个问题，CDN 资源存在于第三方服务器，在安全性上并不完全可控。

CDN 劫持是一种非常难以定位的问题，首先劫持者会利用某种算法或者随机的方式进行劫持（狡猾大大滴），所以非常难以复现，很多用户出现后刷新页面就不再出现了。之前公司有同事做游戏的下载器就遇到这个问题，用户下载游戏后解压不能玩，后面通过文件逐一对比找到原因，原来是 CDN 劫持导致的。怎么解决的呢？听说是找 xx 交了保护费，后面也是利用文件 hash 的方式，想必原理上也是跟 SRI 相同的。

所幸的是，目前大多数的 CDN 劫持只是为了做一些夹带，比如通过 iframe 插入一些贴片广告，如果劫持者别有用心，比如 xss 注入之类的，还是非常危险的。

开启 SRI 能有效保证页面引用资源的完整性，避免恶意代码执行。

## 浏览器如何处理 SRI

- 当浏览器在 script 或者 link 标签中遇到 integrity 属性之后，会在执行脚本或者应用样式表之前对比所加载文件的哈希值和期望的哈希值。
- 当脚本或者样式表的哈希值和期望的不一致时，浏览器必须拒绝执行脚本或者应用样式表，并且必须返回一个网络错误说明获得脚本或样式表失败。


## 使用 SRI

通过使用 webpack 的 html-webpack-plugin 和 webpack-subresource-integrity 可以生成包含 integrity 属性 script 标签。

```javascript
import SriPlugin from 'webpack-subresource-integrity';
 
const compiler = webpack({
    output: {
        crossOriginLoading: 'anonymous',
    },
    plugins: [
        new SriPlugin({
            hashFuncNames: ['sha256', 'sha384'],
            enabled: process.env.NODE_ENV === 'production',
        })
    ]
});
```

那么当 script 或者 link 资源 SRI 校验失败的时候应该怎么做呢？

比较好的方式是通过 script 的 onerror 事件，当遇到 onerror 的时候重新 load 静态文件服务器之间的资源：

```javascript
<script type="text/javascript" src="//11.url.cn/aaa.js"
        integrity="sha256-xxx sha384-yyy"
        crossorigin="anonymous" onerror="loadjs.call(this, event)"></script>
```

loadjs:

```javascript
function loadjs (event) {
  // 上报
  ...
  // 重新加载 js
  return new Promise(function (resolve, reject) {
    var script = document.createElement('script')
    script.src = this.src.replace(/\/\/11.src.cn/, 'https://x.y.z') // 替换 cdn 地址为静态文件服务器地址
    script.onload = resolve
    script.onerror = reject
    document.getElementsByTagName('head')[0].appendChild(script);
  })
}
```

这种方式的缺点是目前 onerror 中的 event 参数无法区分究竟是什么原因导致的错误，可能是资源不存在，也可能是 SRI 校验失败，不过目前来看，除非有统计需求，无差别对待并没有多大问题。

除此之外，我们还需要使用 [script-ext-html-webpack-plugin](https://www.npmjs.com/package/script-ext-html-webpack-plugin) 将 onerror 事件注入进去：

```javascript
const ScriptExtHtmlWebpackPlugin = require('script-ext-html-webpack-plugin');

module.exports = {
  //...
  plugins: [
    new HtmlWebpackPlugin(),
    new SriPlugin({
      hashFuncNames: ['sha256', 'sha384']
    }),
    new ScriptExtHtmlWebpackPlugin({
      custom: {
        test: /.js*/,
        attribute: 'onerror="loadjs.call(this, event)" onsuccess="loadSuccess.call(this)"'
      }
    })
  ]
}
```

然后将 loadjs 和 loadSuccess 两个方法注入到 html 中，可以使用 inline 的方式。

还在知乎上看到一位大神另辟蹊径，通过 jsonp 的方式解决 CDN 劫持。个人感觉这种方式目前能够完美应对 CDN 劫持的主要原因是运营商通过文件名匹配的方式进行劫持，作者的方式就是通过 onerror 检测拦截，并且去掉资源文件的 js 后缀以应对 CDN 劫持。

[应对流量劫持，前端能做哪些工作？](https://www.zhihu.com/question/35720092)




