---
title: async 和 defer 的区别
date: 2016-12-26 15:43:58
categories: JavaScript
tags:
- defer
- async
- script    
---

HTML 中的 `<script>` 元素定义了6个属性：

- async：可选，表示立即下载脚本，但不应该妨碍页面中其它的操作，比如下载其它资源或者等待加载其它脚本，只对外部脚本文件有效。
- charset：可选，src 属性指定的代码的字符集。多数浏览器会忽略它的值。
- defer：可选，表示脚本可以延迟到文档完全被解析和显示后再执行。只对外部脚本有效。
- language：已废弃。
- src：可选，表示要执行代码的外部文件。src 可以包含来自外部域的文件。
- type：可选，可以看成 language 的替代属性。表示编写代码使用的脚本语言的内容类型（MIME），默认值为 text/javascript。

要注意的是，带有 src 的 `<script>` 元素中不应该再包含额外的代码，如果包含了嵌入的代码，则只会下载外部文件，嵌入的代码不会执行。

## 标签的位置

按照惯例，所有的 `<script>` 都应该放入 `<head>` 中，但是这就意味着必须要等所有的 JavaScript 代码下载解析和执行完毕后才能开始呈现页面内容（浏览器在遇到 body 标签时，才开始呈现页面内容）。假如有很多 JavaScript 代码需要执行的话，就会导致浏览器窗口出现空白，因此比较好的做法是把 JavaScript 代码放在 `<body>` 的最后。

## 延迟脚本 defer

HTML4.01 中为 `<script>` 增加了 defer 属性，这个属性用来表明脚本执行的时候不会影响页面结构，也就是说脚本会延迟到整页面解析完毕后再运行。因此在 `<script>` 中设置 defer 属性，相当于告诉浏览器，立即下载，但延迟执行。

```html
<!DOCTYPE html>
<html>
    <head>
        <script defer src="./a.js"></script>
        <script defer src="./b.js"></script>
    </head>
    <body>
    </body>
</html>>
```

在这个例子中，虽然 `<script>` 放在了 head 中，但是其中包含的脚本将延迟到浏览器解析到 `</html>` 标签才会开始执行。HTML5 规范要求脚本按照他们出现的先后顺序执行，因此第一个延迟脚本 a.js 会优先于 b.js 执行，而这两个脚本会先于 [DOMContentLoaded](https://developer.mozilla.org/zh-CN/docs/Web/Events/DOMContentLoaded) 事件执行。在现实中，延迟脚本不一定会按照顺序执行，也不一定会在 DOMContentLoaded 事件触发之前执行，因此最好只包含一个延迟脚本。

defer 属性只适用于外部脚本文件，因此嵌入脚本的 defer 属性会被浏览器忽略，而且各个浏览器对 defer 属性的处理不尽相同，因此把延迟脚本放在页面底部仍是最佳选择。

> 在 XHTML 文档中，要把 defer 属性设置为 defer="defer"

## 异步脚本 async

HTML5 为 `<script>` 元素定义了 async 属性。async 只适用于外部脚本文件，并且告诉浏览器立即下载文件。但与 defer 不同的是，标记为 async 的脚本并不能保证按照指定它们的先后顺序执行。例如

```html
<html>
    <head>
        <scrpt async src="a.js"></scrpt>
        <scrpt async src="b.js"></scrpt>
    </head>
</html>
```

在上述代码中，b.js 可能会在 a.js 之前执行，因此，确保两者之间互不依赖非常重要，指定 async 属性的目的是不让页面等待两个脚本下载和执行，从而异步脚在页面其它内容。因此，建议异步脚本不要在加载期间修改 DOM。

异步脚本一定会在页面 [load](https://developer.mozilla.org/en-US/docs/Web/Events/load) 事件之前执行，但可能会在 DOMContentLoaded 事件触发之前或之后执行。

## defer vs async 

下面这张图能很好地说明 defer 与 async 之间的关系：

<img src="/assets/img/async_vs_defer.svg" alt="defer_vs_async">

从图中我们可以得出以下几点：

- defer 和 async 在下载时是一样的，都是异步的（相较 HTML 解析）。
- defer 会在 HTML 解析完成后执行的，async 则是下载完成后执行。
- defer 是按照加载顺序执行的，async 是哪个文件先加载完，哪个先执行。
- async 在使用的时候，可以用于完全无依赖的脚本，比如百度分析或者 Google Analytics。

## chrome 是怎么样做的

上面提到的只是规范，但是各个厂商的实现可能有所不同，chrome 浏览器首先会请求 HTML 文档，然后对其中的各种资源（图片、CSS、视频等）调用相应的资源加载器进行**异步网络请求**，同时进行 DOM 渲染，直到遇到 `<script>` 标签的时候，主进程才会停止渲染等待此资源加载完毕然后调用 V8 引擎对 js 解析，继而继续进行 DOM 解析。可以理解为如果加了 async 属性就相当于单独开了一个进程去独立加载和执行，而 defer 是和将 `<script>` 放到 body 底部一样的效果。

为验证我们设计测试代码如下：

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.5.2/animate.css" ref="stylesheet">
  <link href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.1.0/css/bootstrap.css" rel="stylesheet">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/backbone.js/1.3.3/backbone.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/quill/1.3.6/quill.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/react/16.3.2/umd/react.development.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.6.5/angular.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/vue/2.5.16/vue.js"></script>
</head>
<body>
 <h1>Hello World</h1>
</body>
</html>
```

### 放在 head 中

<img src="/assets/img/async_vs_defer_script.png" alt="async_vs_defer_script">

可以看到几个资源是异步加载并且执行后才开始出现首屏效果，首屏时间接近 1000ms，还是比较慢的。


### 放在 body 底部

<img src="/assets/img/async_vs_defer_body.png" alt="async_vs_defer_body">

放在 body 底部的时候，首屏出现的时间快了很多，大约在 500ms 左右，资源文件在 HTML 解析后按顺序加载执行。

### 放在 head 中并且使用 defer

<img src="/assets/img/async_vs_defer_head_defer.png" alt="async_vs_defer_head_defer">

defer 为延迟执行，但是下载是可以异步下载的，首屏时间不到 600ms，但是慢于 script 放于 body 底部。

### 放在 head 中并且使用 async 

<img src="/assets/img/async_vs_defer_head_async.png" alt="async_vs_defer_head_async">

async 为异步代码，所有的代码都是在页面解析完成后执行，但是执行顺序并非按照代码书写顺序。

### defer vs async

两个放在一起更能看出效果

<img src="/assets/img/async_vs_defer.png" alt="async_vs_defer">

## 参考资料

- 《JavaScript 高级程序设计》
- [浅谈script标签的defer和async](https://segmentfault.com/a/1190000006778717)