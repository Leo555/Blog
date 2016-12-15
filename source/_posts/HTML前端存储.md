---
title: HTML前端存储
date: 2016-11-16 00:33:38
categories: HTML
tags:
- HTML
- JavaScript
---
# Cookie, LocalStorage 与 SessionStorage

## 基本概念

Cookie，指某些网站为了辨别用户身份而储存在用户本地终端（Client Side）上的数据（通常经过加密）。

html5 中的 Web Storage 包括了两种存储方式：sessionStorage和localStorage。

sessionStorage 用于本地存储一个会话（session）中的数据，这些数据只有在同一个会话中的页面才能访问并且当会话结束后数据也随之销毁。因此 sessionStorage 不是一种持久化的本地存储，仅仅是会话级别的存储。

而 localStorage 用于持久化的本地存储，除非主动删除数据，否则数据是永远不会过期的。浏览器中同一个域下的窗口可以共享 localStorage 数据。

## 兼容性

| 属性 | 描述 | 类型 | 默认值|
| 特性 | Chrome | Firefox (Gecko) | Internet Explorer | Opera | Safari (WebKit)|
| :-| :------: | :------: |:------:| :------: | :------: |
| localStorage  | 4  | 3.5 | 8 |  10.50 | 4 |
| sessionStorage | 5  | 2 |  8  | 10.50 | 4 |

