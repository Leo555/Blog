---
title: 再不学 flex 就不会写布局了
date: 2017-04-19 20:35:52
categories: css
tags: 
- flex
- css
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

1. 绝对布局，使用 margin

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

2. 相对布局，计算 left 和 top

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

3. 父容器宽高不确定或者不容易确定，综合相对布局 + 绝对布局

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

4. 使用 flex

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

5. flex + margin

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

（一） 免去了很多计算。最后两个使用 flex 布局的例子中，无论父元素还是子元素的宽度和高度发生改变，都能依然能保持居中；而前面三种方法中，则需要都要改变其他值，才能保持居中。

（二） 使用 flex 布局的语义化要比前面几种都好，前面三种方法给了一大堆数字，不去认真看一看、算一算，很难确定是否是居中，这对代码阅读者也是非常不友好。

（三） flex 对响应式布局的支持更好。虽然前面几种方法也能实现响应式布局，但是实现起来比较麻烦，不如 flex 来得实在。

（四） flex 支持行内元素。

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
项目默认沿主轴排列。单个项目占据的主轴空间叫做 main size，占据的交叉轴空间叫做 cross size。

容器具有这样的特点：父容器可以统一设置子容器的排列方式，子容器也可以单独设置自身的排列方式，如果两者同时设置，以子容器的设置为准。

## 父容器

### justify-content 设置子容器沿主轴排列

| 属性 | 描述 | 效果|
| :-| :- | :- |
|justify-content: flex-start|起始端对齐|<img src="/assets/img/flex-start.png" alt="flex-start">|
|justify-content: flex-end|末尾段对齐|<img src="/assets/img/flex-end.png" alt="flex-end">|
|justify-content: center|居中对齐|<img src="/assets/img/flex-center.png" alt="flex-center">|
|justify-content: space-around|子容器沿主轴均匀分布，位于首尾两端的子容器到父容器的距离是子容器间距的一半。|<img src="/assets/img/space-around.png" alt="space-around">|
|justify-content: space-between|子容器沿主轴均匀分布，位于首尾两端的子容器与父容器相切。|<img src="/assets/img/space-between.png" alt="space-between">|

### align-items 设置自容器沿交叉轴排列

| 属性 | 描述 |效果|
| :-| :- | :- |
|align-items: flex-start|起始端对齐|<img src="/assets/img/align-flex-start.png" alt="flex-start">|
|align-items: flex-end|末尾段对齐|<img src="/assets/img/align-flex-end.png" alt="flex-start">|
|align-items: center|居中对齐|<img src="/assets/img/align-center.png" alt="align-center">|
|align-items: baseline|基线对齐（首行文字对齐）所有子容器向基线对齐，交叉轴起点到元素基线距离最大的子容器将会与交叉轴起始端相切以确定基线。|<img src="/assets/img/align-baseline.png" alt="align-baseline">|
|align-items: stretch|子容器沿交叉轴方向的尺寸拉伸至与父容器一致|<img src="/assets/img/align-stretch.png" alt="align-stretch">|
