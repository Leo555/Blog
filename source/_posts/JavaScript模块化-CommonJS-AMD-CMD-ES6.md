---
title: 前端模块化-CommonJS,AMD,CMD,ES6
date: 2018-05-06 23:03:17
categories: JavaScript
tags:
- CommonJS
- AMD
- CMD
- ES6    
---

## 模块化解决什么问题

随着 JavaScript 工程越来越大，团队协作不可避免，为了更好地对代码进行管理和测试，模块化的概念逐渐引入前端。模块化可以降低协同开发的成本，减少代码量，同时也是“高内聚，低耦合”的基础。

模块化主要解决两个问题：

1. 命名冲突
2. 文件依赖：比如 bootstrap 需要引入 jquery，jquery 文件的位置必须要 bootstrap.js 之前引入。

<!--more-->

### 远古时代的人们是怎样解决模块化的

在各种模块化规范出来之前，人们使用匿名闭包函数解决模块化的问题。

```javascript
var num0 = 2; // 注意这里的分号
(function () {
  var num1 = 3
  var num2 = 5 
  var add = function () {
    return num0 + num1 + num2
  }
  console.log(add()) // 10
})()

// console.log(num1) // num1 is not defined
```

这样做的好处是，你可以在函数内部使用全局变量和局部变量，并且不用担心局部变量污染全局变量。这种用括号把匿名函数包起来的方式，也叫做立即执行函数（IIFE）。所有函数内部代码都在闭包(closure)内。它提供了整个应用生命周期的私有和状态。


### CommonJS 规范

CommonJS 将每个文件都视为一个模块，在每个模块中变量默认都是私有变量，通过 module.exports 定义当前模块对外输出的接口，通过 require 加载模块。

(1) 使用方法：

circle.js 

```javascript
const { PI } = Math

exports.area = (r) => PI * r ** 2

exports.circumference = (r) => 2 * PI * r
```

app.js 

```javascript
const circle = require('./circle.js')
console.log(circle.area(4))
```

(2) 原理：node 在编译 js 文件的过程中，会使用一个如下的函数包装器将其包装[模块包装器](http://nodejs.cn/api/modules.html#modules_the_module_wrapper)：

```javascript
(function (exports, require, module, __filename, __dirname) {
    const circle = require('./circle.js')
    console.log(circle.area(4))
})
```

这也是为什么在 node 环境中可以使用这几个没有显式定义的变量的原因。其中 `__filename` 和 `__dirname` 在查找文件路径的过程中分析得到后传入的。module 变量是这个模块对象自身，exports 是在 module 的构造函数中初始化的一个空对象。

更详细的内容可以参考 [node modules](http://nodejs.cn/api/modules.html)

关于什么时候使用 exports、什么时候使用 module.exports，可以参考 [exports shutcut](http://nodejs.cn/api/modules.html#modules_exports_shortcut)

(3) 优点 vs 缺点

CommonJS 能够避免全局命名空间污染，并且明确代码之间的依赖关系。但是 CommonJS 的模块加载是同步的，假如一个模块引用三个其它模块，那么这三个模块需要被完全加载后这个模块才能运行。这在服务端不是什么问题（node），但是在浏览器端就不是那么高效了，毕竟读取网络文件比本地文件要耗时的多。


### AMD

[AMD](https://github.com/amdjs/amdjs-api/wiki/AMD) 全称异步模块化定义规范（Asynchronous Module Definition），采用异步加载模块的方式，模块的加载不影响后面语句的执行，并且使用 callback 回调函数的方式来运行模块加载完成后的代码。

(1) 使用方式

定义一个 myModule 的模块，它依赖 jQuery 模块：

```javascript
define('myModule', ['jQuery'], function ($) {
  // $ 是 jQuery 的输出模块
  $('#app').text('Hello World')
})
```

第一个参数表示模块 id，为可选参数，第二个参数表示模块依赖，也是可选参数。

使用 myModule 模块：

```javascript
require(['myModule', function (myModule) {}])
```

[requirejs](http://requirejs.org/) 是 AMD 规范的一个实现，详细的使用方法可以查看官方文档。


### CMD

CMD 规范来源于 [seajs](https://seajs.github.io/seajs/docs/)，CMD 总体于 AMD 使用起来非常接近，AMD 与 CMD 的区别，可以查看 与 RequireJS 的异同](https://github.com/seajs/seajs/issues/277)

(1) 使用方式：

```javascript
// CMD
define(function(require, exports, module) {
  var a = require('./a')
  a.doSomething()
  // ...
  var b = require('./b')
  // 依赖可以就近书写
  b.doSomething()
  // ...
})
```

CMD 推崇依赖就近，可以把依赖写进你的代码中的任意一行，AMD 是依赖前置的，在解析和执行当前模块之前，模块必须指明当前模块所依赖的模块。

### UMD

UMD（Universal Module Definition）并不是一种规范，而是结合 AMD 和 CommonJS 的一种更为通用的 JS 模块解决方案。

在打包模块的时候经常会见到这样的写法：

```javascript
output: {
  path: path.resolve(__dirname, '../dist'),
  filename: 'vue.js',
  library: 'Vue',
  libraryTarget: 'umd'
},
```

表示打包出来的模块为 umd 模块，既能在服务端（node）运行，又能在浏览器端运行。我们来看 vue 打包后的源码 [vue.js](https://github.com/vuejs/vue/blob/master/dist/vue.js)

```javascript
(function (global, factory) {
	typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
	typeof define === 'function' && define.amd ? define(factory) :
	(global.Vue = factory());
}(this, (function () { 'use strict';
// ...
})))
```

代码翻译过来就是：

1. 首先判断是否为 node 环境：exports 为一个对象，并且 module 存在。
2. 如果是 node 环境就用 `module.exports = factory()` 把 vue 导出 （通过 require('vue') 进行引用）。
3. 如果不是 node 环境判断是否支持 AMD：define 为 function 并且 define.amd 存在。
4. 如果支持 AMD 就使用 define 定义模块，（通过 require(['vue']) 引用）。
5. 否则的话直接将 vue 绑定在全局变量上（通过 window.vue 引用）。


### ES6


终于到了 ES6 的时代，JS 开始从语言层面支持模块化，从 node8.5 版本开始支持原生 ES 模块。不过有两点限制：

1. 模块名（文件名）必须为 mjs
2. 启动参数要加上 `--experimental-modules`

假如有 a.mjs 如下：

```javascript
export default {
  name: 'Jack'	
}
```

在 b.mjs 中可以引用：

```javascript
import a from './a.mjs'
console.log(a) // { name: 'Jack' }
```

chrome61 开始也支持 JS module，只需要在 script 属性中添加 `type="module"` 即可。


```html
<script type="module" src="module.js"></script>
<script type="module">
  import { sayHello } from './main.js'
  sayHello()
</script>

// main.js

export function sayHello () {
  console.info('Hello World')	
}
```


### ES6 module 详解

ES6 module 主要由两个命令组成：export 和 import。


(1) export 命令

```javascript
// 输出变量
export let num = 123
export const name = 'Leo'

// 输出一组变量
let num = 123
let name = 'Leo'
export { num, name }

// 输出函数
export function foo (x, y) { return x ** y }

// 使用别名
function a () {}
function b () {}
export {
  a as name,
  b as value
}
// 引用的时候按照别名引用
import { name, value } from '..'
```


需要注意的是，export 命令只能对外输出接口，以下的输出方式均为错误的：

```javascript
// 报错
export 1
var m = 1
export m
function f () {}
export f

// 正确的写法
export var m = 1
var m = 1
export { m }
export { m as n}
export function f () {}
function f () {}
export { f }
```

export 输出的值是动态绑定的，这点与 CommonJS 不同，CommonJS 输出的是值的缓存，不存在动态更新。

export 命令必须处于模块顶层，如果处于块级作用域内，就会报错。

(2) import 命令


## 总结

## 参考资料