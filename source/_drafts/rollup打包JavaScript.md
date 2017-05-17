---
title: 使用 rollup 打包 JavaScript
date: 2017-04-30 13:45:51
categories: JavaScript
tags:
- rollup
- JavaScript
---

[rollup](https://rollupjs.org/) 的第一个 master 分支创建于 2015年5月，相较于 webpack 年轻了大约 3 岁。3 岁对于一个热门开源项目来说差不多就是从青年到壮年的发展，项目维护基本上是由固定的几个人来负责，但是项目周边生态却是由整个开源社区贡献，而这需要时间的积累。

我是从掘金的一篇文章才开始了解 rollup 的——[《Webpack、Rollup 相爱相杀的那些事》](https://juejin.im/entry/58f428078d6d810064887400)。从文章中看到 Vue、React、Ember、Preact、D3、Three.js、Moment 以及其它许多知名的库都在使用 Rollup 进代码进行打包，这让我非常好奇，究竟 Rollup 有哪些特殊之处呢？

<!-- more -->

## 简介

rollup 目前最新版本为 0.5.6，还没有发布它第一个正式版本，但是在 github 已经有 9k+ 的 Star 了，可见其受欢迎程度。

rollup 自己的定位是

> Rollup is a module bundler for JavaScript which compiles small pieces of code into something larger and more complex, such as a library or application. It uses the new standardized format for code modules included in the ES6 revision of JavaScript, instead of previous idiosyncratic solutions such as CommonJS and AMD. ES6 modules let you freely and seamlessly combine the most useful individual functions from your favorite libraries. This will eventually be possible natively, but Rollup lets you do it today.

翻译过来就是：

> Rollup 是一个 JavaScript 模块打包工具，可以把小段的代码编译成更大更强的代码，比如库和app。它使用更新的标准来处理代码模块化，包括 ES6 修订版，而不是像之前的解决方案那样使用 CommonJS 和 AMD 作为解决方案。ES6 模块化方案让你能够更加自由和无缝地使用库的功能。

我的理解就是：

Rollup 是基于 ES2015 模块化对代码进行打包，相较于 webpack 使用 CommonJS 更加高效，是未来 JavaScript 发展的趋势。

### Rollup 优势


