title: 使用Electron构建跨平台桌面应用
tags:
  - Node
  - ES7
  - async
categories: JavaScript
date: 2016-11-11 11:44:11
---
# 简介

Electron提供了丰富的本地（操作系统）的API，使你能够使用纯JavaScript来创建桌面应用程序。与其它各种的Node.js运行时不同的是Electron专注于桌面应用程序而不是Web服务器。

这并不意味着Electron是一个绑定图形用户界面（GUI）的JavaScript库。取而代之的是，Electron使用Web页面作为它的图形界面，所以你也可以将它看作是一个由JavaScript控制的迷你的Chrominum浏览器。