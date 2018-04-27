---
title: JavaScript 常见的内存泄漏
date: 2018-04-23 22:07:24
categories: JavaScript
tags:
- JavaScript
- 内存泄漏
- Memory Leaks
---

## 什么是内存泄漏

JavaScript 是一种垃圾回收语言，垃圾回收语言通过周期性地检查之前被分配的内存是否可以从应用的其它部分访问来帮助开发者管理内存。内存泄露是指当一块内存不再被应用程序使用的时候，由于某种原因，这块内存没有返还给操作系统或者内存池的现象。内存泄漏可能会导致应用程序卡顿或者崩溃。

<!--more-->

### 查看内存泄漏

在 chrome 中可以通过 performance 中的 Memory record 来查看，选中 Memory 后点击左边的 Record，然后模拟用户的操作，一段时间后点击 stop，在面板上查看这段时间的内存占用情况。如果内存基本平稳，则无内存泄漏情况；如果内存占用不断飙升，内可能出现内存泄漏的情况。

在 Node 环境中，可以输入 `process.memoryUsage()` 查看 Node 进程的内存占用情况。

- rss（resident set size）：进程的常驻内存部分。
- heapTotal："堆"占用的内存，包括用到的和没用到的。
- heapUsed：用到的堆的部分。
- external： V8 引擎内部的 C++ 对象占用的内存。

判断内存泄漏，以 heapUsed 字段为准。

## 常见的内存泄漏

《JavaScript高级程序设计》中提到了一种内存泄漏：由于 IE9 之前的版本对 JS 对象和 DOM 对象中使用的垃圾回收机制，会导致如果闭包的作用域链中保存着一个 HTML 元素，那该元素将无法销毁。

```javascript
function assignHandler () {
  var element = document.getElementById('someElement')
  element.onclick = function () {
    alert(element.id)
  }    
}
```

以上代码创建了一个作为 element 元素事件处理程序的闭包，而这个闭包则又创建了一个循环引用，匿名函数中保存了一个对 element 对象的引用，因此无法减少 element 的引用数。只要匿名函数在，element 的引用数至少是 1，因此它所占用的内存就永远无法回收。

解决办法：

```javascript
function assignHandler () {
  var element = document.getElementById('someElement')
  var id = element.id
  element.onclick = function () {
    alert(id)
  }
  element = null
}
```

>注意: 上述问题在现代浏览器上并不会出现

### 意外的全局变量

在 JavaScript 非[严格模式](https://lz5z.com/JavaScript%E4%B8%A5%E6%A0%BC%E6%A8%A1%E5%BC%8F/)中，未定义的变量会自动绑定在全局对象上（window/global），比如：

```javascript
function foo () {
  bar = 'something'    
}
foo()
```

foo 执行的时候，由于内部变量没有定义，所以相当于 `window.bar = 'something'`，函数执行完毕，本应该被销毁的变量 bar 却永久的保留在内存中了。

解决办法，使用[严格模式](https://lz5z.com/JavaScript%E4%B8%A5%E6%A0%BC%E6%A8%A1%E5%BC%8F/)。

虽然全局变量上绑定的变量无法被垃圾回收，但是有时需要使用全局变量去存储临时信息，这个时候要格外小心，并在变量使用完毕后设置为 null，以回收内存。

```javascript
window.bar = null
delete window.bar
```

下面写一个 demo：

```javascript
function test() {
  for (let i = 0; i < 100; i++) {
    console.log(new Date().getTime())
    window[`${new Date().getTime()}`] = new Array(1000000).join('x')
  }
}

function grow() {
  test()
  setTimeout(grow, 1000)
}
document.onload = grow()
```

将这段脚本放置于浏览器中，打开 chrome performance，记录一段时间后，发现内存线条如下：

<img src="/assets/img/js-memory-leak.png" alt="js-memory-leak">

同时打开 chrome 任务管理器，会看到代表当前页面的标签页所占用的内存不断飙升。

### JS 错误引用 DOM 元素

```javascript
var nodes = '';
(function () {
  var item = {
    name: new Array(1000000).join('x')
  }
  nodes = document.getElementById('nodes')
  nodes.item = item
  nodes.parentElement.removeChild(nodes)
 })()
```

这里的 dom 元素虽然已经从页面上移除了，但是 js 中仍然保存这对该 dom 元素的引用，导致内存不能释放。

打开 chrome 控制台 Memory，点击 `Take snapshot`：

<img src="/assets/img/js-memory-leak-profile.png" alt="js-memory-leak-profile">

点击生成的 Snapshot，通过关键字 `str` 进行 filter：

<img src="/assets/img/js-memory-leak-snapshot.png" alt="js-memory-leak-snapshot">

从上图可知，代码运行结束后，内存中的长字符串依然没有被垃圾回收。

### 闭包循环引用

[闭包](https://lz5z.com/JavaScript%E9%97%AD%E5%8C%85/)是指函数能够访问父环境中定义的变量。

```javascript
(function() {
  var bar = null
  var foo = function() {
    var originalBar = bar
    var unused = function() {
      return originalBar
    }
    bar = {
      longStr: new Array(1000000).join('x'),
      someMethod() {
        console.log(new Date().getTime())
      }
    }
  }
  setInterval(foo, 100)
})()
```

上面代码中的 unused 是一个闭包，因为其内部引用了父环境中的变量 originalBar，虽然它被没有使用，但 v8 引擎并不会把它优化掉，因为 JavaScript 里存在 eval 函数，所以 v8 引擎并不会随便优化掉暂时没有使用的函数。

需要注意的一点是： **闭包的作用域一旦创建，它们有同样的父级作用域，作用域是共享的**。

bar 引用了someMethod，someMethod 这个函数与 unused 这个闭包共享一个闭包上下文。所以 someMethod 也引用了 originalBar 这个变量。

因此引用链如下：

GCHandler -> foo -> bar -> someMethod -> originalBar -> someMethod(old) -> originalBar(older)-> someMethod(older)

造成了闭包的循环引用。

<img src="/assets/img/js-memory-leak-clouser.png" alt="js-memory-leak-clouser">

## 参考资料

- [javascript典型内存泄漏及chrome的排查方法](https://segmentfault.com/a/1190000008901861)
- 《JavaScript高级程序设计》
- [4种JavaScript内存泄漏浅析及如何用谷歌工具查内存泄露](https://github.com/wengjq/Blog/issues/1)
- [4 Types of Memory Leaks in JavaScript and How to Get Rid Of Them](https://auth0.com/blog/four-types-of-leaks-in-your-javascript-code-and-how-to-get-rid-of-them/)
