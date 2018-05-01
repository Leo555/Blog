---
title: JavaScript 中 的 DOM 和 BOM
date: 2016-12-24 13:23:25
categories: JavaScript
tags:
- DOM
- BOM
---

## JavaScript 与 ECMAScript 关系

JavaScript = ECMAScript + DOM + BOM

1.ECMAScript 为 JavaScript 提供核心语言功能，是由欧洲计算机制造商协会（ECMA）39号技术委员会（TC39）制定的一种通用、跨平台、供应商中立的脚本语言和语义。ECMAScript 是一种由 ECMA 组织通过 ECMA-262 标准化的脚本程序设计语言。ECMA-262 标准没有参考 Web 浏览器，它规定了语言的语法、类型、语句、关键字、保留字、操作符、对象。

2.DOM (文档对象模型) 是针对 XML 但是经过扩展用于 HTML 的应用程序编程接口（API）。DOM 把 HTML 页面映射为一个多层节点结构，开发人员借助 DOM 提供的 API，可以轻松地删除，添加，替换或者修改节点。

3.BOM（浏览器对象模型）指的是由 Web 浏览器暴露的所有对象组成的表示模型。从根本上将 BOM 只处理浏览器窗口和框架，但是人们习惯把针对浏览器的 JavaScript 扩展也算作 BOM 的一部分，例如：浏览器弹出新窗口的功能；移动、缩放和关闭浏览器窗口的功能；navigator 对象；location 对象； screen 对象；cookies 支持；XMLHttpRequest 和 IE 的 ActiveXObject 对象。BOM 直到 HTML5 才有了规范可以遵守，在此之前每个浏览器都有自己不同的实现。

<!--more-->

### DOM 级别

DOM1 级由两个模块组成，DOM 核心（DOM Core）和 DOM HTML。其中，DOM Core 规定如何映射基于 XML 的文档结构，DOM HTML 模块则在 DOM Core 基础上加以扩展，添加了针对 HTML 的对象和方法。

DOM2 在原有的 DOM 基础上又扩充了鼠标和用户界面事件、范围、遍历（迭代 DOM 文档的方法）等细分模块，并且通过对象接口增加了对 CSS 的支持。DOM2 级引入的模块有：
    - DOM 视图（DOM Views）：定义了追踪不同文档的视图接口。
    - DOM 事件（DOM Events）：定义了事件和事件处理的接口。
    - DOM 样式（DOM Style）：定义了基于 CSS 为元素样式的接口。
    - DOM 遍历和范围（DOM Traversal and Range）：定义了遍历和操作文档树的接口。

DOM3 级进一步扩展 DOM，引入了以统一方式加载和保存文档的方法——在 DOM 加载和保存（DOM Load and Save）模块中定义，新增了 DOM 验证（DOM Validation）。DOM3 级也对 DOM Core 进行了扩展，开始支持 XML 1.0 规范。

> DOM0 级，DOM0 级标准本质上不存在，所谓 DOM0 只是 DOM 历史坐标中的一个参照点，具体来说，DOM0 级是指 Internet Explorer 4.0 和 Netscape Navigator 4.0 最初支持的 DHTML。



