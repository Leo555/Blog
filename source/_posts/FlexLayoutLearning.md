---
title: 再不学 flex 就不会写布局了
date: 2017-04-19 20:35:52
categories: css
tags: 
- flex
- css
- 居中
---

## 如何居中的问题

块状元素居中是一个老生常谈的话题，之前面试的时候考官也曾问到过这个。下面写几种常见的块状元素居中的方式。

<!-- more -->
假如想要 con 在 box 中居中

```html
<div class="box">
  <div class="con"></div>
</div> 
```

### 绝对布局，使用 margin

```css
.box {
  width: 500px;
  height: 500px;
  background: #ebebeb;
}
.con {
  width: 100px;
  height: 100px;
  background: #000;
  position: absolute;
  margin: 200px;
}
```

### 相对布局，计算 left 和 top

```css
.box {
  width: 500px;
  height: 500px;
  background: #ebebeb;
}
.con {
  width: 100px;
  height: 100px;
  background: #000;
  position: relative;
  left: 200px;
  top: 200px;
}
```

### 父容器宽高不确定或者不容易确定，综合相对布局 + 绝对布局

```css
.box {
    width: 500px;
    height: 500px;
    background: #ebebeb;
    position: relative;
}

.con {
    width: 100px;
    height: 100px;
    background: #000;
    position: absolute;
    top: 50%;
    left: 50%;
    margin-top: -50px;
    margin-left: -50px;
}
```

### 使用 flex

``` css
.box {
    width: 500px;
    height: 500px;
    background: #ebebeb;
    display: flex;
    justify-content: center;
    align-items: center;
}

.con {
    width: 100px;
    height: 100px;
    background: #000;
}
```

### flex + margin

```css
.box {
    display: flex;
    width: 500px;
    height: 500px;
    background: #ebebeb;
}

.con {
    width: 100px;
    height: 100px;
    background: #000;
    margin: auto;
}
```

使用 flex 布局的优势不可谓不明显：

- 免去了很多计算。最后两个使用 flex 布局的例子中，无论父元素还是子元素的宽度和高度发生改变，都能依然能保持居中；而前面三种方法中，则需要都要改变其他值，才能保持居中。
- 使用 flex 布局的语义化要比前面几种都好，前面三种方法给了一大堆数字，不去认真看一看、算一算，很难确定是否是居中，这对代码阅读者也是非常不友好。
- flex 对响应式布局的支持更好。虽然前面几种方法也能实现响应式布局，但是实现起来比较麻烦，不如 flex 来得实在。
- flex 支持行内元素。

## 什么是 flex 布局

传统布局的核心是盒子模型，依赖 display 属性 + position 属性 + float 属性。可以看出来传统布局非常容易实现像 word 左对齐，右对齐这样的功能，可以说，传统布局更适合于文字排版。

flex 是 flexible Box 的缩写，可以看做弹性的盒子模型。

### flex 用法

使用 flex 首先要设置父元素 `display: flex`。任何元素都可以指定为 flex 布局：

块状元素：

```css
.box {
    display: flex;
}
```

行内元素

```css
.box {
    display: inline-box;
}
```

设为 flex 布局以后，子元素的 float、clear 和 vertical-align 属性将失效。

## flex 两个基本概念

flex 的核心的概念就是 **容器** 和 **轴**。容器包括外层的 **父容器** 和内层的 **子容器**，轴包括 **主轴** 和 **交叉轴**，如下图所示：

<img src="/assets/img/flex-layout.png" alt="我是一只的图片">

容器默认存在两根轴：水平的主轴（main axis）和垂直的交叉轴（cross axis）。主轴的开始位置叫做 main start，结束位置叫做 main end；交叉轴同理，
子容器默认沿主轴排列。单个子容器占据的主轴空间叫做 main size，占据的交叉轴空间叫做 cross size。

容器具有这样的特点：父容器可以统一设置子容器的排列方式，子容器也可以单独设置自身的排列方式，如果两者同时设置，以子容器的设置为准。

## 父容器

父容器一共有6个属性: **flex-direction, flex-wrap, flex-flow, justify-content, align-items, align-content**

### flex-direction 属性决定主轴的方向

| 属性 | 描述 | 效果|
| :-| :- | :- |
|flex-direction: row|（默认值）主轴为水平方向，起点在左端|<img src="/assets/img/flex-direction-row.png" alt="flex-direction-row">|
|flex-direction: row-reverse|主轴为水平方向，起点在右端|<img src="/assets/img/flex-direction-row-reverse.png" alt="flex-direction-row-reverse">|
|flex-direction: column|主轴为垂直方向，起点在上沿|<img src="/assets/img/flex-direction-column.png" alt="flex-direction-column">|
|flex-direction: column-reverse|主轴为垂直方向，起点在下沿|<img src="/assets/img/flex-direction-column-reverse.png" alt="flex-direction-column-reverse">|


### flex-wrap 决定子容器是否换行排列

| 属性 | 描述 | 效果|
| :-| :- | :- |
|flex-wrap: nowrap|（默认）不换行|<img src="/assets/img/flex-wrap-nowrap.png" alt="flex-wrap-nowrap">|
|flex-wrap: wrap|换行，第一行在上方|<img src="/assets/img/flex-wrap-wrap.png" alt="flex-wrap-wrap">|
|flex-wrap: wrap-reverse|换行，第一行在下方|<img src="/assets/img/flex-wrap-wrap-reverse.png" alt="flex-wrap-wrap-reverse">|

## flex-flow

flex-direction 属性和 flex-wrap 属性的简写形式，默认值为 row nowrap

### justify-content 设置子容器在主轴上的对齐方式

| 属性 | 描述 | 效果|
| :-| :- | :- |
|justify-content: flex-start|（默认）起始端对齐|<img src="/assets/img/flex-start.png" alt="flex-start">|
|justify-content: flex-end|末尾段对齐|<img src="/assets/img/flex-end.png" alt="flex-end">|
|justify-content: center|居中对齐|<img src="/assets/img/flex-center.png" alt="flex-center">|
|justify-content: space-around|子容器沿主轴均匀分布，位于首尾两端的子容器到父容器的距离是子容器间距的一半。|<img src="/assets/img/flex-space-around.png" alt="space-around">|
|justify-content: space-between|子容器沿主轴均匀分布，位于首尾两端的子容器与父容器相切。|<img src="/assets/img/flex-space-between.png" alt="space-between">|

### align-items 设置子容器沿交叉轴的对齐方式

| 属性 | 描述 |效果|
| :-| :- | :- |
|align-items: flex-start|交叉轴的起点对齐|<img src="/assets/img/align-flex-start.png" alt="flex-start">|
|align-items: flex-end|交叉轴的终点对齐|<img src="/assets/img/align-flex-end.png" alt="flex-start">|
|align-items: center|交叉轴的中点对齐|<img src="/assets/img/align-center.png" alt="align-center">|
|align-items: baseline|基线对齐（首行文字对齐）所有子容器向基线对齐，交叉轴起点到元素基线距离最大的子容器将会与交叉轴起始端相切以确定基线。|<img src="/assets/img/align-baseline.png" alt="align-baseline">|
|align-items: stretch|（默认）如果子容器未设置高度或设为auto，子容器沿交叉轴方向的尺寸拉伸至与父容器一致|<img src="/assets/img/align-stretch.png" alt="align-stretch">|


## 子容器

子容器一共有6个属性： **order, flex-grow, flex-shrink, flex-basis, flex, align-self**

### order 改变子容器的排列顺序

默认值为 0，可以为负值，数值越小排列越靠前。order 只能为整数。

| 属性 |效果|
| :-| :- |
|order: -1|<img src="/assets/img/flex-order.png" alt="flex-order">|

### flex-grow 定义子容器如何瓜分剩余空间

默认值为 0，就是即使存在剩余空间，也不瓜分。如果定义了非 0 值，则按照比例瓜分。flex-grow 只能为整数。

| 属性 |效果|
| :-| :- |
|flex-grow: 1|<img src="/assets/img/flex-grow.png" alt="flex-grow">|

### flex-shrink 定义了子容器的缩小比例。

默认为1，即如果空间不足，则子容器将缩小。如果所有子容器的 flex-shrink 都为1，当空间不足时，都将等比例缩小。如果某个子容器的 flex-shrink 为0，其他子容器都为1，则空间不足时，前者不缩小。

| 属性 |效果|
| :-| :- |
|flex-shrink: 0|<img src="/assets/img/flex-shrink.png" alt="flex-shrink">|

### flex-basis 用来改变子容器占据主轴空间的大小

表示在不伸缩的情况下子容器占据主轴空间的大小，默认为 auto，表示子容器本来的大小。


### flex

flex-grow, flex-shrink 和 flex-basis 的简写，默认值为 0 1 auto


### align-self 用来覆盖父容器的 align-items 属性

align-self 属性允许单个子容器有与其他子容器不一样的对齐方式，默认值为auto，表示继承父元素的 align-items 属性，如果没有父元素，则等同于 stretch。改属性的取值与 align-items 相同。

| 属性 |效果|
| :-| :- |
|align-self: flex-end|<img src="/assets/img/flex-align-self.png" alt="flex-align-self">|


## 参考资料
1. [MDN CSS Flexible Box Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout)
2. [Flex 布局教程：语法篇](http://www.ruanyifeng.com/blog/2015/07/flex-grammar.html?utm_source=tuicool)