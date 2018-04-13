---
title: JavaScript 循环与异步
date: 2018-04-11 14:03:53
categories: JavaScript
tags:
- JavaScript
- Loop
- async/await
---

## JS 中的循环与异步

JS 中有多种方式实现循环：`for; for in; for of; while; do while; forEach; map` 等等。假如循环里面的内容是异步并且 await 的，那异步代码究竟是像 `Promise.all`一样将循环中的代码一起执行，还是每次等待上一次循环执行完毕再执行呢？

## 首先看结论

forEach 和 map, some, every 循环是并行执行的，相当于 Promise.all，其它 for, for in, for of, while, do while 都是串行执行的。

先定义异步函数 foo 和可遍历数组 arr：

```javascript
const arr = Array.from({ length: 5 }, (v, k) => k)
const foo = i => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      console.log(i)
      resolve('')
    }, 1000)
  })
}
```
<!--more-->

并行执行：

```javascript
/**
 * forEach
 */
function e() {
  arr.forEach(async a => await foo(a))
}
/**
 * map
 */
function f() {
  arr.map(async a => await foo(a))
}
/**
 * every
 */
function g() {
  arr.every(a => {
    return (async() => {
      await foo(a)
    })()
  })
}
```

串行执行：

```javascript
/**
 * for
 */
async function a() {
  for (var i = 0; i < arr.length; i++) {
    await foo(arr[i])
  }
}
/**
 * for
 */
async function b() {
  for (let i = 0; i < arr.length; i++) {
    await foo(arr[i])
  }
}
/**
 * for of
 */
async function c() {
  for (let i of arr) {
    await foo(i)
  }
}
/**
 * for in
 */
async function d() {
  for (let i in arr) {
    await foo(i)
  }
}
/**
 * while
 */
async function h() {
  let i = 0
  while (i < 5) {
    await foo(i++)
  }
}
/**
 * do while
 */
async function i() {
  let i = 0
  do {
    await foo(i++)
  } while (i < 5)
}
```

## 如何让 forEach 或者 map 也能串行执行

首先查看 forEach 的 [polyfill](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach)，简化后可以理解为以下代码：

```javascript
Array.prototype.forEach = function(callback, thisArg) {
  var len = this.length
  var k = 0
  while (k < len) {
    var kValue
    if (k in this) {
      kValue = this[k]
      callback.call(thisArg, kValue, k, this)
    }
    k++
  }
}
```

可以看到本质上 forEach 还是通过 while 循环来实现的，假如我们想要一个异步的 forEach 的话，只需要将 callback 的调用改成 await 即可：

```javascript
Array.prototype.forEachAsync = async function(callback, thisArg) {
  var len = this.length
  var k = 0
  while (k < len) {
    var kValue
    if (k in this) {
      kValue = this[k]
      await callback.call(thisArg, kValue, k, this)
    }
    k++
  }
}
```

npm 上有一个更为完备的解决方案：[forEachAsync](https://github.com/FuturesJS/forEachAsync/blob/master/forEachAsync.js)

```javascript
const forEachAsync = require('forEachAsync').forEachAsync

forEachAsync(arr, function(a) {
  return foo(a)
}).then(function() {
  console.log('Done!')
})
```



就这么多。