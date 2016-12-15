---
title: JavaScript跨域实践
date: 2016-12-16 01:04:17
categories: JavaScript
tags:
- JavaScript
- HTML
- 跨域
---

# 背景

最近写了一个 Flask 服务，然后用本地的 angular 页面去 call 这个服务的时候，一直报错，错误信息如下
> XMLHttpRequest cannot load http://XXX:8085/predict. Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource. Origin 'null' is therefore not allowed access.



