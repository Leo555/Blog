---
title: Web 性能优化-首屏和白屏时间
date: 2018-05-17 19:24:09
categories: 性能
tags: 
- 首屏
- 白屏
---

## 什么是首屏和白屏时间？

白屏时间是指浏览器从响应用户输入网址地址，到浏览器开始显示内容的时间。
首屏时间是指浏览器从响应用户输入网络地址，到首屏内容渲染完成的时间。

白屏时间 = 地址栏输入网址后回车 - 浏览器出现第一个元素
首屏时间 = 地址栏输入网址后回车 - 浏览器第一屏渲染完成

影响白屏时间的因素：网络，服务端性能，前端页面结构设计。
影响首屏时间的因素：白屏时间，资源下载执行时间。

以百度为例，将 chrome 网速调为 Fast 3G，然后打开 Performance 工具，点击 “Start profiling and reload page” 按钮，查看 Screenshots 如下图：

<!--more-->

<img src="/assets/img/first_and_write_screen.png" alt="first_and_write_screen">

## 白屏时间

通常认为浏览器开始渲染 `<body>` 或者解析完 `<head>` 的时间是白屏结束的时间点。

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>白屏</title>
    <script>
        // 不兼容 performance.timing 的浏览器
        window.pageStartTime = Date.now()
    </script>
        <!-- 页面 CSS 资源 -->
        <link rel="stylesheet" href="xx.css">
        <link rel="stylesheet" href="zz.css">
        <script>
            // 白屏结束时间
            window.firstPaint = Date.now()

            // 白屏时间
            console.log(firstPaint - performance.timing.navigationStart)
        </script>
</head>
<body>
    <h1>Hello World</h1>
</body>
</html>
```

白屏时间 = firstPaint - performance.timing.navigationStart || pageStartTime


## 首屏时间

关于首屏时间是否包含图片加载网上有不同的说法，个人认为，只要首屏中的图片加载完成，即是首屏完成，不在首屏中的图片可以不考虑。

计算首屏时间常用的方法有：

(1) 首屏模块标签标记法

由于浏览器解析 HTML 是按照顺序解析的，当解析到某个元素的时候，你觉得首屏完成了，就在此元素后面加入 `script` 计算首屏完成时间。

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>首屏</title>
    <script>
        // 不兼容 performance.timing 的浏览器
        window.pageStartTime = Date.now()
    </script>
</head>
<body>
    <!-- 首屏可见内容 -->
    <div class=""></div>
    <!-- 首屏可见内容 -->
    <div class=""></div>
    <script type="text/javascript">
            // 首屏屏结束时间
            window.firstPaint = Date.now()
            // 首屏时间
            console.log(firstPaint - performance.timing.navigationStart)
    </script>
    <!-- 首屏不可见内容 -->
    <div class=""></div>
    <!-- 首屏不可见内容 -->
    <div class=""></div>
</body>
</html>
```

(2) 统计首屏内加载最慢的图片/iframe

通常首屏内容中加载最慢的就是图片或者 iframe 资源，因此可以理解为当图片或者 iframe 都加载出来了，首屏肯定已经完成了。

由于浏览器对每个页面的 TCP 连接数有限制，使得并不是所有图片都能立刻开始下载和显示。我们只需要监听首屏内所有的图片的 onload 事件，获取图片 onload 时间最大值，并用这个最大值减去 navigationStart 即可获得近似的首屏时间。

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>首屏</title>
    <script>
        // 不兼容 performance.timing 的浏览器
        window.pageStartTime = Date.now()
    </script>
</head>
<body>
    <img src="https://lz5z.com/assets/img/google_atf.png" alt="img" onload="load()">
    <img src="https://lz5z.com/assets/img/css3_gpu_speedup.png" alt="img" onload="load()">
    <script>
        function load () {
            window.firstScreen = Date.now()
        }
        window.onload = function () {
            // 首屏时间
            console.log(window.firstScreen - performance.timing.navigationStart)
        }
    </script>
</body>
</html>
```

### [Performance API](https://developer.mozilla.org/zh-CN/docs/Web/API/Performance)

Performance 接口可以获取到当前页面与性能相关的信息。

在 chrome 中查看 performance.timing 对象：

<img src="/assets/img/performance-timing.png" alt="performance">

与浏览器对应的状态如下图：

<img src="/assets/img/performance.png" alt="performance">

左边红线代表的是网络传输层面的过程，右边红线代表了服务器传输回字节后浏览器的各种事件状态，这个阶段包含了浏览器对文档的解析，DOM 树构建，布局，绘制等等。

### DOMContentLoaded vs load

(1) DOMContentLoaded 是指页面元素加载完毕，但是一些资源比如图片还无法看到，但是这个时候页面是可以正常交互的，比如滚动，输入字符等。 jQuery 中经常使用的 `$(document).ready()` 其实监听的就是 DOMContentLoaded 事件。

(2) load 是指页面上所有的资源（图片，音频，视频等）加载完成。jQuery 中 `$(document).load()` 监听的是 load 事件。

```javascript
// load
window.onload = function () {}

// DOMContentLoaded
function ready (fn) {
    if (document.addEventListener) {
        document.addEventListener('DOMContentLoaded', function () {
            document.removeEventListener('DOMContentLoaded', arguments.callee, false)
            fn()
        }, false)
    } 
    // 如果 IE
    else if (document.attachEvent) {
        // 确保当页面是在iframe中加载时，事件依旧会被安全触发
        document.attachEvent('onreadystatechange', function() {
            if (document.readyState == 'complete') {
                document.detachEvent('onreadystatechange', arguments.callee)
                fn()
            }
        })
        // 如果是 IE 且页面不在 iframe 中时，轮询调用 doScroll 方法检测DOM是否加载完毕
        if (document.documentElement.doScroll && typeof window.frameElement === 'undefined') {
            try {
                document.documentElement.doScroll('left')
            } catch(error) {
                return setTimeout(arguments.callee, 20)
            }
            fn()
        }
    }
}
```


## 参考资料

- [前端优化-如何计算白屏和首屏时间](http://www.cnblogs.com/longm/p/7382163.html)
- [前端性能的几个基础指标](https://segmentfault.com/a/1190000005784687)
- [Performance - MDN](https://developer.mozilla.org/zh-CN/docs/Web/API/Performance)