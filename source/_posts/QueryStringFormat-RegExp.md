---
title: 正则表达式格式化查询参数
date: 2018-03-26 23:05:05
categories: JavaScript
tags:
- RegExp
- JavaScript
---

记录一下，通过一行正则表达式和 replace 方法简单实现正则表达式格式化查询参数。

```
const url = 'https://lz5z.com/000/?a=123&b=456&c=%E4%B8%AD%E6%96%87'
/** 
 * 格式化查询字符串(正则实现) 
 * @param url url地址 
 * @return {Object} 格式化的json对象 
 */
function formatUrl(url) {
    const reg = /(?:[?&]+)([^&]+)=([^&]+)/g
    let data = {}

    function fn(str, key, value) {
        data[decodeURIComponent(key)] = decodeURIComponent(value)
    }
    url.replace(reg, fn)
    return data
}

console.log(formatUrl(url)) // { a: '123', b: '456', c: '中文' }
```

下次面试官问你的时候，你能答上来吗？😉😉😉

<!--more-->

下面是 《JavaScript高级程序设计》 中给出的方案:

```javascript
function getQueryStringArgs () {
    // 取得查询字符串并去掉开头的问号
    var qs = (location.search.length > 0 ? location.search.substring(1) : '')
    // 保存数据的对象
    var args = {}
    // 取得每一项
    var items = qs.length ? qs.split('&') : []

    for (var i = 0; i < items.length; i++) {
        var item = items[i].split('=')
        var name = decodeURIComponent(item[0])
        var value = decodeURIComponent(item[1])
        if (name.length) args[name] = value
    }
    return args
}
```
