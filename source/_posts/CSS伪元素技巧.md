---
title: CSS 伪元素技巧
date: 2017-12-08 20:08:00
categories: CSS
tags:
- CSS
- 伪元素
- 清除浮动
---

## 伪元素技巧

在 [CSS 伪元素基本用法](https://lz5z.com/CSS%E4%BC%AA%E5%85%83%E7%B4%A0%E5%9F%BA%E6%9C%AC%E7%94%A8%E6%B3%95/)一文中讲述了伪元素的基础功能，本章学习一些进阶功能，看看伪元素能实现哪些方便好用的功能。


### 清除浮动

如果一个元素内部的子元素全部都是浮动的话，那么这个元素会出现高度塌陷，这个时候就需要清除浮动。高度塌陷的负面作用主要有：不能正确显示背景，边框不能撑开，margin 和 padding 不能正确显示。

假设有代码如下：

<!--more-->

html:

```html
<div class="outer">
  <div class="inner">1</div>
  <div class="inner">2</div>
  <div class="inner">3</div>
</div>
```

css:

```css
.outer {
  border: 1px solid;
  background: #ccc;
  margin: 10px;
  padding: 5px;
}
.inner {
  float: left;
  width: 80px;
  height: 80px;
  border: 1px solid;
}
```

使用伪元素清除浮动的办法：

```css
.outer {
  zoom: 1; // IE6/7 兼容性
}
.outer:after {
  content: "";
  display: block;
  clear: both;  
}
```

其它清除浮动的办法：

（1）给父元素设置高度。
（2）`clear: both` 清除浮动。

常见的用法是在父元素结束之前，统一引入一个元素 `clear: both` 用来清除浮动。

html:

```html
<div class="outer">
  <div class="inner">1</div>
  <div class="inner">2</div>
  <div class="inner">3</div>
  <div class="clear"></div>
</div>
```

css:

```css
.clear {
  clear: both;
}
```

这种方法实现起来很简单，不过缺点也很明显，引入了额外的 DOM 元素。

clear 属性可以对应的属性值有：
- left  在左侧不允许浮动元素。
- right  在右侧不允许浮动元素。
- both  在左右两侧均不允许浮动元素。
- none  默认值。允许浮动元素出现在两侧。
- inherit  规定应该从父元素继承 clear 属性的值。

（3）给父级元素定义 `overflow: auto` 或者 `overflow: hidden`

```css
.outer {
  overflow: auto;
  zoom: 1; // IE6/7 兼容性
}
```

使用 overflow 属性来清除浮动只可以使用 hiddent 和 auto 不能使用 visible。 为了兼容 IE 最好用 `overflow:hidden`，缺点是元素会被截断。

总结清除浮动最佳方案

```css
// 全浏览器通用的 clearfix 方案
// 引入了 zoom 以支持 IE6/7
// 同时加入 :before 以解决现代浏览器上边距折叠的问题
.clearfix:before,
.clearfix:after {
  display: table;
  content: " ";
}
.clearfix:after {
  clear: both;
}
.clearfix {
  zoom: 1;
}
```

### 扩大可点击范围

这点在移动端开发显得尤为重要，可以增强用户体验。

html:

```html
<button class="btn">click</button>
```

css:

```css
.btn {
  position: relative;
}
.btn:before {
  content: '';
  position: absolute;
  top: -20px;
  right: -20px;
  bottom: -20px;
  left: -20px;
}
```

还有一种不使用伪元素扩大可点击范围的方式是使用 border + background-clip
 
```css
.btn {
  border: 20px solid transparent;
  background-clip: padding-box;
}
```


### 实现分割线效果

{% raw %}
<!DOCTYPE html>
<html lang="en">
<head>
  <style>
  .divide {
    width: 100%;
    text-align: center;
  }
  .divide:before, .divide:after {
    content: "";
    position: absolute;
    margin: 14px 14px 10px 10px;
    height: 1px;
    width: calc(50% - 75px);
    background-color: red;
    padding: 0 10px;
  }
  .divide:before {
    left: 0;
  }
  .divide:after {
    right: 0;
  }
  </style>
</head>
<body>
  <p class="divide">我是分割线</p>
</body>
</html>
{% endraw %}

实现方式

html:

```html
<p class="divide">我是分割线</p>
```

css:

```css
.divide {
  width: 100%;
  text-align: center;
}
.divide:before, .divide:after {
  content: "";
  position: absolute;
  margin: 14px 14px 10px 10px;
  height: 1px;
  width: calc(50% - 75px);
  background-color: red;
  padding: 0 10px;
}
.divide:before {
  left: 0;
}
.divide:after {
  right: 0;
}
```

### 调用元素属性

通过在 content 中使用 attr 函数可以调用元素的属性。

```css
a:after {
  content: attr(href);
}
```

### 引用媒体资源

```css
a:before {
  content: url(https://lz5z.com/assets/img/avatar.svg);
}
```

### 计数器 counter

1. counter-reset：创建或者重置一个计数器
2. counter-increment：计数器递增
3. content：配合伪元素插入内容

html:

```html
<ol class="sites">
  <li><input type="checkbox">Apple</li>
  <li><input type="checkbox">Google</li>
  <li><input type="checkbox">Amazon</li>
  <li><input type="checkbox">Facebook</li>
</ul>
<p>一共选择了<span class="count"></span>个网站</p>
```

css:

```css
.sites {
  counter-reset: site;
}
.sites input:checked {
  counter-increment: site;
}
.count:before {
  content: counter(site);
}
```



### 自制 checked 样式

{% raw %}
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <title>Document</title>
  <style>
  #sites li {
    margin: 0 auto;
    width: 30px;
    font-size: 14px;
    line-height: 1.5;
    cursor: pointer;
  }
  
  #sites li:before {
    color: #7cfc00;
    background: #fff;
    border: 2px solid #d3d3d3;
    content: " ";
    width: 16px;
    height: 16px;
    line-height: 1;
    margin-left: -38px;
    position: absolute;
    text-align: center;
    vertical-align: middle;
    cursor: pointer;
    pointer-events: all;
  }
  
  #sites li.checked:before {
    background: green;
    border: 2px solid green;
    color: #fff;
    content: "\2714";
  }
  </style>
</head>

<body>
  <ol id="sites">
    <li class="checked">Apple</li>
    <li>Google</li>
    <li class="checked">Amazon</li>
    <li>Facebook</li>
  </ol>
</body>
<script>
function hasClass(el, className) {
  if (el.classList) {
    return el.classList.contains(className)
  } else {
    return !!el.className.match(new RegExp('(\\s|^)' + className + '(\\s|$)'))
  }
}

function addClass(el, className) {
  if (el.classList) {
    el.classList.add(className)
  } else if (!hasClass(el, className)) {
    el.className += ` ${className}`
  }
}

function removeClass(el, className) {
  if (el.classList) {
    el.classList.remove(className)
  } else if (hasClass(el, className)) {
    let reg = new RegExp('(\\s|^)' + className + '(\\s|$)')
    el.className = el.className.replace(reg, ' ')
  }
}

function changeStyle(ele) {
  if (hasClass(ele, 'checked')) {
    removeClass(ele, 'checked')
  } else {
    addClass(ele, 'checked')
  }
}

let sites = document.querySelector('ol#sites')
// 事件委托
sites.addEventListener('click', function(e) {
  e = e || window.event
  let target = e.target || e.srcElement
  if (target.tagName.toLowerCase() === 'li') {
    changeStyle(target)
  }
}, false)

</script>
</html>
{% endraw %}


html:

```html
<ol id="sites">
  <li class="checked">Apple</li>
  <li>Google</li>
  <li class="checked">Amazon</li>
  <li>Facebook</li>
</ol>
```

css

```css
li {
  font-size: 14px;
  line-height: 1.5;
  cursor: pointer;
}

li:before {
  color: #7cfc00;
  background: #fff;
  border: 2px solid #d3d3d3;
  content: " ";
  width: 16px;
  height: 16px;
  line-height: 1;
  margin-left: -38px;
  position: absolute;
  text-align: center;
  vertical-align: middle;
  cursor: pointer;
  pointer-events: all;
}

li.checked:before {
  background: green;
  border: 2px solid green;
  color: #fff;
  content: "\2714";
}
```

## 最后

在网上还有很多关于伪元素的用法，非常有趣，既能减少 DOM 元素数量，还能用 CSS 实现一部分 JS 的功能，非常酷炫，后面见到有趣的用法会不断记录。