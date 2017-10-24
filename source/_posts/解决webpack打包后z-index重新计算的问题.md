---
title: 解决webpack打包后z-index重新计算的问题
date: 2017-10-24 13:18:37
categories: JavaScript
tags:
- webpack
- css
---

## 背景

与 PC 端共同开发一个页面，页面由 PC 端提供内部 iframe 则由我们前端提供。开发时候遇到了一个问题，webpack 将 css 的 z-index 重新计算，导致 iframe 里面 z-index 比较大的 toast 被 iframe 外面 z-index 较小的 dialog 覆盖。

给 z-index 加上 !important 后依然无效，查资料发现是 OptimizeCssAssetsPlugin 调用 cssProcessor cssnano 对 z-index 进行了重新计算导致的。

这本来是 webpack 插件的一个善举（让 z-index 数值更加合理），但是具体情况来看，这里显然不需要这个 “善举”。

<!--more-->

## 解决方案

解决方案按照网上的资料，可以在 OptimizeCssAssetsPlugin 插件中关掉 [cssnano](http://cssnano.co/) 对 z-index 的重新计算（cssnano 称为 rebase）。

```javascript
new OptimizeCSSPlugin({
    cssProcessor: require('cssnano'),
    cssProcessorOptions: {
        discardComments: {removeAll: true},
        // 避免 cssnano 重新计算 z-index
        safe: true
    },
    canPrint: false
})
```

cssnano 将 z-index rebase 归类为 unsafe，而不是 bug，只有在单个网页的 css 全部写入一个 css 文件，并且不通过 JavaScript 进行改动时是 safe。

参考： http://cssnano.co/optimisations/zindex/

cssnano 默认进行 z-index rebase。

unsafe (potential bug) 优化项默认不开启应该比较友好。

## 另外一个方案

以上是网上提供的方案，而且亲测有效，但是由于项目太大，因为其中一个小功能改了整个项目的 css 处理策略，难免有些担心会影响到其它页面。思考再三，决定不改 webpack 配置。

观察之前项目中使用的框架，在生成 dialog 或者 toast 的时候，即使在 webpack 插件对 css 进行处理之后，其 z-index 依然是很大的。

比如 element-ui 下 的 popup-manager.js 中首先设置 zIndex 为 2000，然后在 openModal 的时候动态添加 css 到 DOM 中，并且改变 zIndex 的值，而在浏览器中观察弹框的 z-index，果然是没有经过 cssnano rebase 的。

于是仿照 element-ui 的做法，把 z-index 相关的 css 用 js 动态插入到 DOM 中，就完美地解决了这个问题，并且没有对其它项目产生影响。

```javascript
// 改变 toast 的 z-index
(function addToastStyle () {
    let nod = document.createElement('style')
    let str = `.mint-toast{z-index:2009;}`
    nod.type = 'text/css'
    nod.appendChild(document.createTextNode(str))
    document.getElementsByTagName('head')[0].appendChild(nod)
})()
```

