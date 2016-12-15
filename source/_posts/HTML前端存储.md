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

| 特性 | Chrome | Firefox (Gecko) | Internet Explorer | Opera | Safari (WebKit)|
| :-| :------: | :------: |:------:| :------: | :------: |
| localStorage  | 4  | 3.5 | 8 |  10.50 | 4 |
| sessionStorage | 5  | 2 |  8  | 10.50 | 4 |

## 差别

Cookie 一般由服务器生成，可设置失效时间。如果在浏览器端生成 Cookie，默认是关闭浏览器后失效。Http 通信的时候 Cookie 的信息会保存的 Http 头中。
localStorage 和 sessionStorage 仅在客户端（即浏览器）中保存，不参与和服务器的通信。

## 应用场景

因为每个 HTTP 请求都会带着 Cookie 的信息，所以 Cookie 应当尽可能精简，比较常用的一个应用场景就是判断用户是否登录。针对登录过的用户，服务器端会在他登录时往 Cookie 中插入一段加密过的唯一辨识单一用户的辨识码，下次只要读取这个值就可以判断当前用户是否登录啦。

localStorage 主要存储一些比较多的本地数据，如 HTML5 小游戏里面生成的数据。

如果遇到一些内容特别多的表单，为了优化用户体验，我们可能要把表单页面拆分成多个子页面，然后按步骤引导用户填写。这时候 sessionStorage 的作用就发挥出来了。

## 安全性的考虑

需要注意的是，不是什么数据都适合放在 Cookie、localStorage 和 sessionStorage 中的。使用它们的时候，需要时刻注意是否有代码存在 XSS 注入的风险。因为只要打开控制台，你就随意修改它们的值，所以千万不要用它们存储你系统中的敏感数据。