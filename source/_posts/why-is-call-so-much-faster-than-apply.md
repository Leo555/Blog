---
title: 为什么 call 的速度远远快于 apply
date: 2017-06-29 16:43:04
categories: JavaScript
tags:
- JavaScript
- call
- apply
---

在 stackoverflow 看到一个有趣的问题: [Why is call so much faster than apply?](https://stackoverflow.com/questions/23769556/why-is-call-so-much-faster-than-apply) 于是使用 [benchmark.js](https://benchmarkjs.com/) 在 node 中自己测试了一下：

```javascript
const Benchmark = require('benchmark')
const suite = new Benchmark.Suite
const applyFun = function (str) {
    return [].slice.apply(str, [1])
}
const callFun = function (str) {
    return [].slice.call(str, 1)
}
// add tests
suite.add('apply', function () {
    applyFun('apple')
}).add('call', function () {
    callFun('apple')
}).on('cycle', function (event) {
    console.log(String(event.target))
}).on('complete', function () {
    console.log('Fastest is ' + this.filter('fastest').map('name'))
}).run({'async': true})
```

测试结果：

```
apply x 951,707 ops/sec ±0.46% (87 runs sampled)
call x 969,699 ops/sec ±0.52% (91 runs sampled)
Fastest is call
```

可见虽然 call 比 apply 要快一些，但是差别并不是很大，那么在浏览器上面表现如何呢？

<!--more-->