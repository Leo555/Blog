---
title: HTML meta 标签
date: 2017-12-02 15:22:13
categories: HTML
tags:
- HTML5
- meta
---

# 引言

最近做的一个关于电影的网站 [IMDB Top250](https://movie.lz5z.com/)，想对其进行 SEO 优化，用到 meta 信息的时候，很多知识都是 『似乎』、『好像』、『可能』 的感觉，回想自己一直没有系统的学习过 meta 相关的知识，这些东西虽然简单，但是很多时候能发挥出意想不到的效果，尤其对于 SEO 有非常重要的作用。

## meta 简介

meta 标签位于文档的头部，可提供有关页面的元信息（meta-information）。 meta 标签本身不包含任何内容，通过其属性定义了与文档相关联的内容。

meta 标签一共有五个属性值： charset、content、http-equiv、name、scheme。 其中 http-equiv 和 name 
必须与 content 配合组成键值对使用， charset 为 HTML5 属性， scheme 属性 HTML5 不支持。

<!--more-->

### charset

定义 HTML 文档编码方式，一般使用世界通用语言编码 UTF-8。

```html
<meta charset="UTF-8">
```

在 HTML4 中的写法是 

```html
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
```

### http-equiv

http-equiv 为枚举属性，与 content 属性组成键值对，一般用于服务器向浏览器传回一些特定的信息，以帮助浏览器编译和显示页面内容。虽然有些服务器会发送许多这种键值对，但是所有服务器都至少要发送一个：`content-type:text/html`。这将告诉浏览器准备接收一个 HTML 文档。

http-equiv 可枚举的值有： content-type, default-style, refresh。

```html
<meta http-equiv="refresh" content="3;URL=https://lz5z.com">
```

以上表示页面 3 秒后自动跳转。

### name

name 属性是用的最多的属性，常用的有 description，keywords，author，viewport，generator 等等。

其中 keywords 对应 content 用逗号分隔，description 为搜索引擎显示网页时候的简介。

viewport 用于指定视窗的属性，在移动端开发时显得尤为重要。

```html
<meta name="keywords" content="HTML5,meta">
<meta name="description" content="blabla">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
```

还有一些属性值，比如 referrer，robots，renderer。

(1) referrer 控制所有从该文档发出的 HTTP 请求中 HTTP Referer 头的内容：

```html
<meta name="referer" content="always">
```

referrer 对应的 content 属性可取的值：

- `no-referrer`	不要发送 HTTP Referer 首部。
- `origin`	发送当前文档的 origin。
- `no-referrer-when-downgrade`	当目的地是先验安全的(https->https)则发送 origin 作为 referrer ，但是当目的地是较不安全的 (https->http)时则不发送 referrer 。这个是默认的行为。
- `origin-when-crossorigin`	在同源请求下，发送完整的URL (不含查询参数) ，其他情况下则仅发送当前文档的 origin。
- `unsafe-URL`	在同源请求下，发送完整的URL (不含查询参数)。

> HTTP Referer 头：
> Referer 请求头字段允许由客户端指定资源的 URI 来自于哪一个请求地址，这对服务器有好处。Referer 请求头让服务器能够拿到请求资源的来源，可以用于分析用户的兴趣爱好、收集日志、优化缓存等等。同时也让服务器能够发现过时的和错误的链接并及时维护。

注意：动态地插入 `<meta name="referrer">` (通过 document.write 或者 appendChild) 是不起作用的。同样注意如果同时有多个彼此冲突的策略被定义，那么 no-referrer 策略会生效。

(2) robots 用来告诉搜索引擎的爬虫哪些页面需要索引，哪些不需要索引。

```html
<meta name="robots" content="all">
```

robots 对应的 content 可取的值：

- all：文件将被检索，且页面上的链接可以被查询。
- none：文件将不被检索，且页面上的链接不可以被查询。
- index：文件将被检索。
- follow：页面上的链接可以被查询。
- noindex：文件将不被检索，但页面上的链接可以被查询。
- nofollow：文件将被检索，但页面上的链接不可以被查询。

还有一些只有固定的搜索引擎支持的参数，比如 noodp，noarchive 等，这里就不说明了。

(3) renderer

renderer 并不是 w3c 标准，但却经常见于一些网页中，这个属性主要用于双核或者多核浏览器（猎豹浏览器，360浏览器）使用指定的内核处理自己的网页。目前大多数 「双核」 浏览器内部的两个内核分别是 IE 内核和 WebKit 内核，IE 内核主要用于兼容「老一辈」的网页，使其能够正常显示；WebKit 内核则用于渲染「新一代」的网页，从而发挥出更快的显示速度、更好的显示效果、更优异的脚本执行性能。

作为用户来说并不关心你使用哪个内核，简单易用才是王道，因此在网页中设置首选内核会让网页有更好的效果。

```html
<meta name="renderer" content="webkit">
<meta name="renderer" content="webkit|ie-stand">
```
`renderer` 对应的 content 用于指定浏览器内核，
webkit(WebKit 内核)、ie-stand(IE 内核-标准模式)、ie-comp(IE 内核-兼容模式)。我们也可以同时指定多个内核名称，之间以符号"|"进行分隔，此时浏览器将会按照从左到右的先后顺序选择其具备的渲染内核来处理当前网页。

IE8 有自己独特的写法 X-UA-Compatible 对于 IE8 之外的浏览器是不识别的。

```html
// Edge 模式通知 IE 以最高级别的可用模式显示内容
<meta http-equiv="X-UA-Compatible" content="edge"/>

// 如果 IE 有安装 Google Chrome Frame，那么就走安装的组件，如果没有就和上面一样。
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
```

>注： 如果设置浏览器内核为 Webkit (极速模式)，打开网页后却为 IE (兼容模式)，尝试刷新浏览器则会自动切换模式。

通常是这样设置的

```html
<meta name="renderer" content="webkit">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
```

(4) format-detection

防止 ios 把数字/字符串识别为电话/邮件/日期/地址

```html
<meta name="format-detection" content="telephone=no">
<meta name="format-detection" content="date=no">
<meta name="format-detection" content="address=no">
<meta name="format-detection" content="email=no">
```


# 参考资料

[MDN-meta](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/meta)
[关于控制 Referer 你想要知道的一切](http://web.jobbole.com/86648/)