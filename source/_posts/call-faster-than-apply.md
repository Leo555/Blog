---
title: 为什么 call 的速度快于 apply
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

<!--more-->

### 测试环境：

系统：macOS Sierra
CPU：2.6 GHz Intel Core i5
内存：8 GB 1600 MHz DDR3
Node: 8.1.0


### 测试结果：

```
apply x 951,707 ops/sec ±0.46% (87 runs sampled)
call x 969,699 ops/sec ±0.52% (91 runs sampled)
Fastest is call
```

可见虽然 call 比 apply 要快一些，但是差别并不是很大，那么在浏览器上面表现如何呢？

<img src="/assets/img/call_vs_apply.jpg" alt="call_vs_apply_in_browsers">

你也可以点击下面的 button 在自己的浏览器上查看运行效果。

{% raw %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>call vs apply</title>
    <script defer src="https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.4/lodash.min.js"></script>
    <script defer src="https://cdnjs.cloudflare.com/ajax/libs/platform/1.3.4/platform.min.js"></script>
    <script defer src="https://cdnjs.cloudflare.com/ajax/libs/benchmark/2.1.4/benchmark.min.js"></script>
    <script>
    window.onload = () => {
        let log = document.getElementById("log")
        let btn = document.getElementById("btn")
        const applyFun = str => {
            return [].slice.apply(str, [1])
        }
        const callFun = str => {
            return [].slice.call(str, 1)
        }
        const logMessage = arg => {
            let eDiv = document.createElement("div")
            eDiv.innerHTML = typeof arg === "string" ? arg : arg.toString()
            log.appendChild(eDiv)
        }
        const prepare = () => {
            log.innerHTML = ''
            btn.disabled = true
        }

        window.run = () => {
            prepare()
            const suite = new Benchmark.Suite
            // add tests
            suite.add('apply', function() {
                applyFun('apple')
            }).add('call', function() {
                callFun('apple')
            }).on('cycle', function(event) {
                logMessage(String(event.target))
            }).on('complete', function() {
                logMessage('Fastest is ' + this.filter('fastest').map('name'))
                btn.disabled = false
            }).run({
                'async': true
            })
        }
    }
    </script>
</head>
<body>
    <button id="btn" onclick="run()">run test</button>
    <span id="log"></span>
    <hr>
</body>
</html>
{% endraw %}

可以看到几个浏览器中都是 call 的速度要快于 apply，不过都没有特别明显。其中 Safari 的速度让我大吃一惊，直接比其它几个浏览器快了一个数量级。看来 WWDC 2017 发布会上苹果吹的牛没有那么大啊，不过也可能 mac 从硬件层面对 Safari 进行优化。


### 为什么 call 要快于 apply

SO 上面解释的比较详细，在语言设计的时候，apply 需要执行的步数就比 call 要多：无论 call 还是 apply，最终都是调用一个叫做 `[[Call]]` 的内部函数，而 apply 相对于 call 多做了一些参数处理，如参数判断、格式化等。


### 困惑

SO 上面提到 call 的性能是 apply 的 4 倍甚至 30 倍，为什么在我这里的测试只有一丁点差距呢？
突然想到是否参数问题，于是去掉参数和增加参数，分别于 node 环境中测试，发现变化并不大，差距依然很小。那么猜想可能是 ES5 与 ES6 的差距导致的。

对比 [ES5](http://es5.github.io/#x15.3.4.3) 和 [ES6](http://www.ecma-international.org/ecma-262/6.0/#sec-function.prototype.apply) 中对这两个函数的定义，发现 Function.prototype.call 的变化并不大，主要变化发生在 Function.prototype.apply 上，从 ES5 的 9 步变成了 ES6 的 6步。主要变化发生在对参数处理的部分，其它关于内部函数调用的部分，看起来并没有太多差异。


### 总结

通过测试发现随着 ECMAScript 语言和 JavaScript 解释器性能不断增强，call vs apply 在性能上的差距越来越小， SO 上面提到的数倍甚至几十倍的差距，目前已经不存在了，因此在使用上可以随心所欲了。