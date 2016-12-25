---
title: DOM 事件机制
date: 2016-12-25 17:44:44
categories: JavaScript
tags:
- 事件流
- JavaScript
- HTML
---

DOM 事件流（event  flow）存在三个阶段：事件捕获 --> 事件目标 --> 事件冒泡。

事件捕获：当事件发生时（onclick,onmouseover……），浏览器会从根节点开始由外到内进行事件传播，即点击了子元素，如果父元素通过事件捕获方式注册了对应的事件的话，会先触发父元素绑定的事件。（IE10 及以下浏览器不支持捕获型事件，所以就少了一个事件捕获阶段）

事件冒泡：与事件捕获恰恰相反，事件冒泡顺序是由内到外进行事件传播，直到根节点。
<!-- more -->
# 事件绑定

JavaScript 中实现事件绑定主要使用两个方法： [addEventListener](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener)、[attachEvent](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/attachEvent)。

## 例子

```html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Event test</title>
	<style>
	    .t{
	        width: 100px;
	        height: 50px;
	        margin: 0 auto;
	        background: orange;
	    }
	</style>
</head>
<body>
	<table id="outside">
    	<tr><td class='t' id="t1">one</td></tr>
    	<tr><td class='t' id="t2">two</td></tr>
	</table>
<script type="text/javascript">
	function modify() {
	  let t2 = document.getElementById("t2");
	  if (t2.firstChild.nodeValue === "three") {
	    t2.firstChild.nodeValue = "two";
	  } else {
	    t2.firstChild.nodeValue = "three";
	  }
	}

	let el = document.getElementById("outside");
	el.addEventListener("click", modify, false);
</script>
</body>
</html>
```
addEventListener(event, listener, useCapture)　　

·参数定义：event---（事件名称，如click，不带on），listener---事件监听函数，useCapture---是否采用事件捕获进行事件捕捉，默认为false，即采用事件冒泡方式。

addEventListener在 IE11、Chrome 、Firefox、Safari等浏览器都得到支持。

