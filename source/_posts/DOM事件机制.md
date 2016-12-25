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

事件捕获：当事件发生时（onclick,onmouseover……），浏览器会从根节点开始由外到内进行事件传播，即点击了子元素，如果父元素通过事件捕获方式注册了对应的事件的话，会先触发父元素绑定的事件。（IE10 及以下浏览器不支持捕获型事件）

事件冒泡：与事件捕获恰恰相反，事件冒泡顺序是由内到外进行事件传播，直到根节点。
<!-- more -->
# 事件

(1)onlick -->事件冒泡，重写onlick会覆盖之前属性，没有兼容性问题

```javascript
el.onclik = null; //解绑单击事件，将onlick属性设为null即可
```

(2)addEventListener(event, listener, useCapture)　　
参数定义：event---（事件名称，如click，不带on），listener---事件监听函数，useCapture---是否采用事件捕获进行事件捕捉，默认为false，即采用事件冒泡方式。 IE8 及以下不支持，属于DOM级的方法，可添加多个方法不被覆盖

```javascript
//事件类型没有on，false 表示在事件第三阶段（冒泡）触发，true表示在事件第一阶段（捕获）触发。 如果handle是同一个方法，只执行一次。
ele.addEventListener('click', function(){ }, false);  
//解绑事件，参数和绑定一样
ele.removeEventListener(event.type, handle, boolean);
```


(3)attachEvent(event.type, handle ); IE特有，兼容IE8及以下，可添加多个事件处理程序，只支持冒泡阶段

```javascript
//如果handle是同一个方法，绑定几次执行几次，这点和addEventListener不同,事件类型要加on,例如onclick而不是click
ele.attachEvent('onclick', function(){ }); 
//解绑事件，参数和绑定一样
ele.detachEvent("onclick", function(){ });
```

(4)默认事件行为：href=""，submit表单提交等

* return false; 阻止独享属性（通过on这种方式）绑定的事件的默认事件

```javascript
ele.onclick = function() {
 ……                         //你的代码
 return false;              //通过返回false值阻止默认事件行为
};
```

* event.preventDefault( ); 阻止通过 addEventListener( ) 添加的事件的默认事件

```javascript
element.addEventListener("click", function(e){
 var event = e || window.event;
 ……
 event.preventDefault( );      //阻止默认事件
},false);
```

* event.returnValue = false; 阻止通过 attachEvent( ) 添加的事件的默认事件

```javascript
element.attachEvent("onclick", function(e){
   var event = e || window.event;
   ……
   event.returnValue = false;       //阻止默认事件
});
```

## 事件封装

JavaScript 中实现事件绑定主要使用两个方法： [addEventListener](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener)、[attachEvent](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/attachEvent)。

为了兼容浏览器，按照网上通用的方案对事件进行封装

```javascript
// 事件绑定
function addEvent(element, eType, handle, bol) {
 if(element.addEventListener){           //如果支持addEventListener
     element.addEventListener(eType, handle, bol);
 }else if(element.attachEvent){          //如果支持attachEvent
     element.attachEvent("on"+eType, handle);
 }else{                                  //否则使用兼容的onclick绑定
     element["on"+eType] = handle;
 }
}
```

```javascript
// 事件解绑
function removeEvent(element, eType, handle, bol) {
 if(element.addEventListener){
     element.removeEventListener(eType, handle, bol);
 }else if(element.attachEvent){
     element.detachEvent("on"+eType, handle);
 }else{
     element["on"+eType] = null;
 }
}
```


HTML

```html
<table id="outside">
	<tr><td class='t' id="t1">one</td></tr>
	<tr><td class='t' id="t2">two</td></tr>
</table>
```

css

```css
.t{
    width: 100px;
    height: 50px;
    margin: 0 auto;
    background: orange;
}
```

JavaScript

```javascript
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
```



