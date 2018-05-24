---
title: 《深入浅出Node.js》-读书笔记
date: 2018-05-23 22:51:15
categories: Node
tags:
- JavaScript
- Node    
---

## 简介

不知不觉 Node 已经更新到第十个版本了，本人使用 Node 也有两年多时间，之前学习的东西一直零零散散，没有形成系统的知识体系，于是最近又抽时间回顾这本经典的 [《深入浅出Node.js》](https://book.douban.com/subject/25768396/)，阅读的过程中，难免有些东西不易理解或者容易忘记，因此选择博客的形式记录。

作者书写这本书的时候，Node 的稳定版本为 v0.10.13，当前最高版本为 v10.1.0，不过整个 Node 的核心体系在当时已经形成，因此对更高版本的理解问题不大。

## 第一章 Node 简介

Node 诞生于 2009 年 3 月，作者为 Ryan Dahl。作者选择 JavaScript 作为 Node 的实现语言主要因为：JavaScript 高性能（V8），符合事件驱动，没有后端历史包袱。

除了 HTML、WebKit 和显卡这些与 UI 相关技术没有支持外，整个 Node 的结构与 Chrome 非常相似，它们都是基于事件驱动的异步架构，浏览器通过事件驱动来服务界面上的交互，Node 通过事件驱动来服务 I/O。

<!--more-->

### Node 的特点

(1) 异步 I/O。在 Node 中，绝大多数的操作都是以异步的方式进行调用，从文件操作到网络请求都是如此。
(2) 事件与回调函数。Node 将前端浏览器中应用广泛的事件机制引入后端，配合异步 I/O。优点是事件编程轻量，低耦合，只用关注事务点等，缺点是多个事件之间的协作是一个问题。
(3) 单线程。Node 保持了 JS 单线程的特点，在 Node 中，JS 与其余线程无法共享状态。单线程好处了不用处理多线程之间的状态同步与通信，没有死锁的存在，也没有线程切换带来的性能开销。缺点是无法利用多核 CPU；错误会引起整个应用退出，应用健壮性值得考验；对大规模高 CPU 计算不友好。

在浏览器中，HTML5 制定了 Web Worker 标准来解决 JS 大规模计算导致的阻塞 UI 渲染的问题。而 Node 中，使用 child_process 创建子进程来应对单线程带来的问题。

(4) 跨平台。

### Node 应用场景

(1) I/O 密集型。I/O 密集的优势˞要在于 Node 利用事件循环的能力，而不是启动每一个线程为每一个请
求服务，资源占用极少。
(2) Node 是否适用于 CPU 密集型应用？首先 Node 的计算性能并不差，但是由于 JavaScript 单线程的原因，如果有长时间运算，将导致 CPU 不能释放，使后续 I/O 无法发起。
(3) 与遗留系统和平共处。比如和 Java 配合，Node 完成 Web 端的开发，Java 提供稳定的接口。
(4) 分布式应用。

## 第二章 模块机制

Node 的模块化采用 CommonJS 规范，关于 JavaScript 模块化的各种规范，可以参考 [前端模块化-CommonJS,AMD,CMD,ES6](https://lz5z.com/JavaScript%E6%A8%A1%E5%9D%97%E5%8C%96-CommonJS-AMD-CMD-ES6/)。

CommonJS 规范涵盖了模块，二进制，Buffer，字符集编码，I/O 流，进程环境，文件系统，socket，单元测试，Web服务器接口，包管理等。

### CommonJS 模块规范

(1) 模块引用

通过 require() 方法引入一个模块的 API 到当前上下文中。

```javascript
var math = require('math')
```
(2) 模块定义

在模块中，上下文提供 exports 对象用于导出当前模块的变量或者方法，并且它是唯一导出的出口。在模块中，还存在一个 module 对象，代表模块自身，而 exports 是 module 的属性。

```javascript
exports.add = function () {
  return eval(Array.prototype.join.call(arguments, '+'))  
}
```

(3) 模块标识

模块标识就是传递给 require() 的参数，它必须是符合小驼峰命名的字符串，或者以 `.` 和 `..` 开头的相对路径，或者绝对路径。

CommonJS 构建的这套模块导出和引入机制使得用户完全不必考虑变量污染，命名空间等方案相形见绌。

### Node 模块实现

Node 引入模块，需要经历三个步骤：路径分析，文件定位，编译执行。

Node 中的模块分为核心模块和文件模块。

(1) 核心模块在 Node 源码编译过程中，编译成为二进制文件，在 Node 启动阶段部分核心模块就被加载进内存，所以省去了文件定位和编译的时间，加载速度最快。

(2) 文件模块则是在运行时动态加载。

(3) 自定义模块是指非核心模块，也不是路径形式的文件模块。以文件或者包的形式存在，这类模块的查找是最费时的。

模块路径：Node 在定位文件模块的时候采用的一种查找策略。具体表现为一个路径组成的数组。比如我在自己的电脑 `/Users/lizhen/WorkSpaces/test` 目录下面创建文件 index.js：

内容如下：

```javascript
console.log(module.paths)
```

运行脚本输出结果如下：

```shell
[ '/Users/lizhen/WorkSpaces/test/node_modules',
  '/Users/lizhen/WorkSpaces/node_modules',
  '/Users/lizhen/node_modules',
  '/Users/node_modules',
  '/node_modules' ]
```

其路径寻址规则如下：从当前目录的 node_modules 中寻找 -> 父目录的 node_modules 中寻找 -> 递归一直到根目录的 node_modules。

它的生成方式与 JavaScript 原型链或者作用域链的查找方式十分类似。Node 会逐个尝试模块路径，直到找到模块或者查找到根目录位置。可以看出，当文件路径比较深的时候，模块查找会比较耗时。

Node 对引入过的模块都会进行缓存，无论是核心模块还是文件模块，require() 方法都采用缓存优先的方式进行加载，并且核心模块的优先级高于文件模块。

#### 文件定位

require() 在分析标识符的过程中，如果标识符不包括扩展名，Node 会按照 `.js`, `.json`, `.node` 的次序补足扩展名，依次尝试。

在尝试的过程中，需要调用 fs 模块同步阻塞式地判断文件是否存在，所以会引起性能问题。解决的办法是：1. `.node` 和 `.json` 文件标识符中带上扩展名。2. 同步配合缓存，可以大幅缓解 Node 单线程中阻塞调用的缺陷。

### 模块编译

在 Node 中，每个文件都是一个对象，它的定义如下：

```javascript
function Module (id, parent) {
  this.id = id
  this.exports = {}
  this.parent = parent
  if (parent && parent.children) {
    parent.children.push(this)
  }
  this.filename = null
  this.loaded = false
  this.children = []
}
```
编译和执行是引入文件模块的最后一个阶段。定位到文件后，Node 会新建一个模块对象，然后根据路径载人并编译。不同文件载入方式不同：

1. `.js` 文件，通过 fs 模块同步读取文件后编译执行。
2. `.node` 文件，由 C/C++ 编写，通过 dlopen() 加载最后编译生成的文件。
3. `.json` 文件，通过 fs 模块同步读取后，用 JSON.parse() 解析。
4. 其余文件都被当做 `.js` 文件载入。

每个编译成功的模块都会将其文件路径作为索引缓存在 `Module._cache` 对象上，以提高二次引入的性能。 

根据不同的文件扩展名，Node 会调用不同的读取方式，如 `.json` 文件：

```javascript
Module._extensions['.json'] = function (module, filename) {
  var content = NativeModule.require('fs').readFileSync(filename, 'utf8')
  try {
    module.exports = JSON.parse(stripBOM(content))
    } catch (e) {
      e.message = filename + ':' e.message
      throw e
    } 
}
```

其中，`Module._extensions` 会赋值给 require 的 extensions 属性。

```javascript
console.log(require.extensions) // { '.js': [Function], '.json': [Function], '.node': [Function] }
```

也可以通过扩展 `require.extensions['.ext']` 的方式对自定义扩展名进行特殊的加载，但是 Node 官方并不鼓励这种行为。

### JavaScript 模块编译

在编译 JavaScript 的过程中，Node 对获取的 JavaScript 文件进行包装：[模块包装器](http://nodejs.cn/api/modules.html#modules_the_module_wrapper)

```javascript
(function(exports, require, module, __filename, __dirname) {
// 模块的代码实际上在这里
});
```
这样每个模块文件之间都进行了作用域隔离，包装之后的代码会通过 vm 原生模块的 runInThisContext() 方法执行（类似 eval，只是有明确的上下文，不污染全局）。

**exports vs module.exports**

exports 对象本质上来说只是 Node 模块包装器的一个形参，直接对其进行赋值，只会改变形参的引用，但并不能改变作用域外的值。

```javascript
var change = function (a) {
  a = 100
  console.log(a) // 100  
}
var a = 10
change(a)
console.log(a) // 10
```
所以如果要实现 require 引入一个类的效果，请赋值给 module.exports 对象。

更详细的解释，可以查看 [exports 快捷方式](http://nodejs.cn/api/modules.html#modules_exports_shortcut)。

我个人的理解是：module 对象在 Node 执行时创建，并且自带 exports 属性，而 exports 对象是对 module.exports 的值引用，当 module.exports 改变的时候， exports 不会被改变，而模块导出的时候，真正导出的是 module.exports，而不是 exports。

看这个例子：

math.js

```javascript
exports.add = function () {
  return eval(Array.prototype.join.call(arguments, '+'))
}
module.exports = {
  add: function () {
    return Array.prototype.join.call(arguments, '+')
  }
}
```

test.js

```javascript
var math = require('./math')
console.log(math.add(2, 34)) //  2+34
```

可以看出，exports 上赋的值，在 module.exports 被重写后无效。

### 核心模块

Node 的核心模块分为 C/C++ 编写和 JavaScript 编写的两部分。其中 C/C++ 文件在 [src](https://github.com/nodejs/node/tree/master/src) 目录下，JavaScript 文件在 [lib](https://github.com/nodejs/node/tree/master/lib) 目录下。

(1) JavaScript 核心模块编译过程

在编译所有的 C/C++ 文件之前，编译程序需要将所有的 JavaScript 模块文件编译为 C/C++ 代码。
- 转为 C/C++ 代码。Node 使用 V8 附带的 js2c.py 工具，将所有内置的 JS 代码（`src/node.js` 和 `lib/*.js`）转换为 C++ 里面的数组，生成 `node_natives.h` 头文件。
- 编译 JS 核心模块。首先在引入 JS 的核心模块的过程中，经历了模块包装器的过程，然后导出 exports 对象。JS 核心模块源文件通过 `process.binding('natives')` 取出，编译成功后模块缓存在 `NativeModule._cache`，文件模块则缓存在 `Module._cache`。

```javascript
function NativeModule (id) {
  this.filename = id + '.js'
  this.id = is
  this.exports = {}
  this.loaded = false  
}
NativeModule._source = process.binding('natives')
NativeModule._cache = {}
```

(2) C/C++ 核心模块的编译过程

Node 的高性能，很大程度是因为核心模型，多数有 C/C++ 编写，C++ 模块主内完成核心，JS 模块主外实现封装模块，充分利用了脚本语言易编写，C/C++ 高效执行的优点。Node 中常见的 buffer、crypto、evals、fs、os 等模块都是 C/C++ 编写的。

(3) 核心模块引入流程

<img src="/assets/img/node_core_module_import.png" alt="node_core_module_import">

(4) 模块调用栈

<img src="/assets/img/node_module_imports.png" alt="node_module_imports">

(5) 包与 NPM

在 Node 中，包和 NPM 是将模块联系起来的一种机制。CommonJS 规范中包目录应该包含如下这些文件。

1. package.json：包描述文件
2. bin： 可执行二进制文件
3. lib：存放 JavaScript 文件
4. doc：存放文档目录
5. test：单元测试代码

NPM 全局安装：

通过执行命令 `npm install express -g` 将 express 安装为全局可用的可执行命令，但并不意味着可以从任何地方通过 require() 都可以引入它。

实际上，全局安装的包都被安装在一个统一的目录下，这个目录为：

`path.resolve(process.execPath, '..', '..', 'lib', 'node_modules')`

这个路径是 Node 可执行文件的路径，比如，Node 可执行文件的路径为 `/usr/local/bin/node`，那么模块目录就是 `/usr/local/lib/node_modules`。

关于更多 JavaScript 模块的规范可以参考 [前端模块化-CommonJS,AMD,CMD,ES6](https://lz5z.com/JavaScript%E6%A8%A1%E5%9D%97%E5%8C%96-CommonJS-AMD-CMD-ES6/)。