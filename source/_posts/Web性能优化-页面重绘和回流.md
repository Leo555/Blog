---
title: Web 性能优化-页面重绘和回流（重排）
date: 2018-05-02 21:46:24
categories: 性能
tags:
- CSS
- 重绘
- 回流    
---

## 前言

早在五年前，Google 就提出了 1s 完成终端页面的首屏渲染的标准。

<img src="/assets/img/google_atf.png" alt="google_atf">

常见的优化网络请求的方法有：DNS Lookup，减少重定向，避免 JS、CSS 阻塞，并行请求，代码压缩，缓存，按需加载，前端模块化...

<!--more-->

虽然相较于网络方面的优化，前端渲染的优化显得杯水车薪，而且随着浏览器和硬件性能的增长，再加上主流前端框架（react、vue、angular）的已经帮我们解决了大多数的性能问题，但是前端渲染性能优化依然值得学习，除去网络方面的消耗，留给前端渲染的时间已经不多了。本文主要学习前端渲染相关的问题。

## 浏览器是如何渲染一个页面的

>1.  浏览器把获取到的 HTML 代码解析成1个 DOM 树，HTML 中的每个 tag 都是 DOM 树中的1个节点，根节点是 document 对象。DOM 树里包含了所有 HTML 标签，包括 `display:none` 隐藏的标签，还有用 JS 动态添加的元素等。
>2. 浏览器把所有样式解析成样式结构体，在解析的过程中会去掉浏览器不能识别的样式，比如 IE 会去掉 -moz 开头的样式。
>3. DOM Tree 和样式结构体组合后构建 render tree, render tree 类似于 DOM tree，但区别很大，render tree 能识别样式，render tree 中每个 NODE 都有自己的 style，而且 render tree 不包含隐藏的节点 (比如 `display:none` 的节点，还有 head 节点)，因为这些节点不会用于呈现，而且不会影响呈现的节点，所以就不会包含到 render tree 中。注意 `visibility:hidden` 隐藏的元素还是会包含到 render tree 中的，因为 `visibility:hidden` 会影响布局(layout)，会占有空间。根据 CSS2 的标准，render tree 中的每个节点都称为 Box (Box dimensions)，理解页面元素为一个具有填充、边距、边框和位置的盒子。
>4. 一旦 render tree 构建完毕后，浏览器就可以根据 render tree 来绘制页面了。

总结为下图：

<img src="/assets/img/web_repaint_reflow.png" alt="web_repaint_reflow">

图片来自 [浏览器渲染页面过程与页面优化](https://segmentfault.com/a/1190000010298038)

在此过程中，前端工程师主要的敌人为：
1. 重新计算样式（Recalculate Style）、计算布局（Layout）=> Rendering/Reflow。
2. 绘制 => Painting/Repaint。

### 重绘与回流

1. 当 render tree 中的一部分（或全部）因为元素的规模尺寸、布局、显示/隐藏等改变而需要重新构建，这个过程称作回流（reflow）。页面第一次加载的时候，至少发生一次回流。
2. 当 render tree 中的一些元素需要更新属性，而这些属性只是影响元素的外观，风格，而不会影响布局的，比如 background-color，这个过程叫做重绘（repaint）

在回流的时候，浏览器会使 render tree 中受到影响的部分失效，并重新构造这部分渲染树，完成回流后，浏览器会重新绘制受影响的部分到屏幕中，该过程成为重绘。因此**回流必将引起重绘，而重绘不一定会引起回流。**

Reflow 的成本比 Repaint 高得多的多。DOM Tree 里的每个结点都会有 reflow 方法，一个结点的 reflow 很有可能导致子结点，甚至父点以及同级结点的 reflow。

### 在 chrome 中查看 repaint

F12 打开控制台 -> DevTools -> Show console drawer -> Rendering -> 勾选 Paint flashing。

### 重绘何时发生

当一个元素的外观的可见性 visibility 发生改变的时候，但是不影响布局。类似的例子包括：outline, visibility, background color。

### 回流何时发生

0. 页面渲染初始化。
1. 调整窗口大小。
2. 改变字体，比如修改网页默认字体。
3. 增加或者移除样式表。
4. 内容变化，比如文本改变或者图片大小改变而引起的计算值宽度和高度改变。
5. 激活 CSS 伪类，比如 :hover
6. 操作 class 属性。
7. 脚本操作 DOM，增加删除或者修改 DOM 节点，元素尺寸改变——边距、填充、边框、宽度和高度。
8. 计算 offsetWidth 和 offsetHeight 属性。
9. 设置 style 属性的值。


```javascript
var s = document.body.style
s.padding = "2px" // 回流+重绘
s.border = "1px solid red" // 回流+重绘
s.color = "blue" // 重绘
s.backgroundColor = "#ccc" // 重绘
s.fontSize = "14px" // 再一次 回流+重绘
document.body.appendChild(document.createTextNode('abc!')) // 回流+重绘
```

### 浏览器

如果向上述代码中那样，浏览器不停地回流+重绘，很可能性能开销非常大，实际上浏览器会优化这些操作，将所有引起回流和重绘的操作放入一个队列中，等待队列达到一定的数量或者时间间隔，就 flush 这个队列，一次性处理所有的回流和重绘。

虽然有浏览器优化，但是当我们向浏览器请求一些 style 信息的时候，浏览器为了确保我们能拿到精确的值，就会提前 flush 队列。

1. offsetTop/Left/Width/Height
2. scrollTop/Left/Width/Height
3. clientTop/Left/Width/Height
4. width,height
5. getComputedStyle(), 或者 IE的 currentStyle

### 减少回流重绘

- requestAnimationFrame：能保证浏览器在正确的时间进行渲染。

- 保持 DOM 操作“原子性”：

```javascript
// bad
var newWidth = ele.offsetWidth + 10
ele.style.width = newWidth + 'px'

var newHeight = ele.offsetHeight + 10
ele.style.height = newHeight + 'px'

// good 读写分离，批量操作
var newWidth = ele.offsetWidth + 10 // read
var newHeight = ele.offsetHeight + 10 // read
ele.style.width = newWidth + 'px' // write
ele.style.height = newHeight + 'px' // write
```

- 使用 classList 代替 className：

className 只要赋值，就一定出现一次 rendering 计算；classList 的 add 和 remove，浏览器会进行样式名是否存在的判断，以减少重复的 rendering。

```javascript
ele.className += 'something'
ele.classList.add('something')
ele.classList.remove('something')
```

- 批量操作借助临时变量

```javascript
// bad
for (let i = 0; i < 10; i++) {
  el.style.left = el.offsetLeft + 5 + 'px'
  el.style.top = el.offsetTop + 5 + 'px' 
}
// good
let left = el.offsetLeft
let top = el.offsetTop
for (let i = 0; i < 10; i++) {
  left += 5
  top += 5 
}
el.style.left = left + 'px'
el.style.top = left + 'px' 
```

- 对元素进行“离线操作”，完成后再一起更新：

1. 使用 DocumentFragment 进行缓存操作,引发一次回流和重绘 [了解DocumentFragment 给我们带来的性能优化](http://www.cnblogs.com/blueSkys/p/3685740.html)
2. 元素操作前使用 `display: none`，完成后再将其显示出来，这样只会触发一次回流和重绘。
3. 使用 cloneNode + replaceChild 技术，引发一次回流和重绘。

假如需要在下面的 html 中添加两个 li 节点：

```html
<ul id="">
</ul>
```

使用 JavaScript：

```javascript
let ul = document.getElementByTagName('ul')
let man = document.createElement('li')
man.innerHTML = 'man'
ul.appendChild(li)
 
let woman = document.createElement('li')
woman.innerHTML = 'woman'
ul.appendChild(woman)
```

上述代码会发生两次回流，假如使用 `display: none` 的方案，虽然能够减少回流次数，但是会发生一次闪烁，这时候使用 DocumentFragment  的优势就体现出来了。

DocumentFragment 有两大特点：

1. DocumentFragment 节点不属于文档树，继承的 parentNode 属性总是 null。
2. 当请求把一个 DocumentFragment 节点插入文档树时，插入的不是 DocumentFragment 自身，而是它的所有子孙节点。这使得 DocumentFragment 成了有用的占位符，暂时存放那些一次插入文档的节点。它还有利于实现文档的剪切、复制和粘贴操作。、

```javascript
let fragment = document.createDocumentFragment()

let man = document.createElement('li')
let woman = document.createElement('li')
man.innerHTML = 'man'
woman.innerHTML = 'woman'
fragment.appendChild(man)
fragment.appendChild(woman)

document.body.appendChild(spanNode)
```

可见 DocumentFragment 是一个孤儿节点，没爹就能出生，但是在需要它的时候，它又无私地把孩子奉献给文档树，然后自己默默离开。是不是有点像《银翼杀手2049》？

## 参考资料

- [16毫秒的优化
](http://velocity.oreilly.com.cn/2013/ppts/16_ms_optimization--web_front-end_performance_optimization.pdf)
- [浏览器渲染页面过程与页面优化](https://segmentfault.com/a/1190000010298038)
- [页面重绘和回流以及优化](http://www.css88.com/archives/4996)
