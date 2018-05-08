---
title: CSS3 动画—transform
date: 2017-06-09 16:23:31
categories: CSS
tags:
- transform
- 动画
- 变形
---

在 CSS3 中，跟动画相关的属性有：变形 transform、过渡 transition、动画 animation。先放一个 Lea Verou 大神的链接 [animatable](http://leaverou.github.io/animatable/)。

本章学习 CSS3 中的 transform 属性。
<!--more-->

## 变形 transform

transform 属性目前还存在浏览器兼容性问题，建议使用 PostCSS 或手动添加浏览器前缀。
使用 transform，元素可以被转换（translate）、旋转（rotate）、缩放（scale）、倾斜（skew）。 
transform 属性只对 block 元素生效。
<script async src="//jsfiddle.net/Leo555/jeejj6yL/13/embed/result,html,css/"></script>

### 移动 translate

 transform: translate(x, y); 表示使元素在 X 轴和 Y 轴移动，y 可以省略，表示不移动。如果参数为负，则表示往相反的方向移动。同时还可以使用 translateX、translateY 和 translateZ 表示在某一个方向移动。Z 轴移动的前提是元素本身或者元素的父元素设定了透视值。

```css
transform: translate(12px, 50%);
transform: translateX(2em);
transform: translateY(0.3in);
transform: translateZ(20px);
```

<script async src="//jsfiddle.net/Leo555/bhotf9bb/embed/result,html,css/"></script>

### 旋转 rotate

旋转 transform: rotate(angle) angle 取值有：角度值deg，弧度值rad，梯度gard，转/圈turn，正数值代表顺时针旋转，反之逆时针。

rotateX、rotateY、rotateZ 表示分别在 X、Y、Z 轴上旋转。rotate3d(x, y, z, angle) 表示在3维空间旋转。

```css
transform: rotate(-30deg);
transform: rotate(0.5turn);
transform: rotate3d(1, 2.0, 3.0, 10deg);
transform: rotateX(0.5deg);
transform: rotateY(0.5deg);
transform: rotateZ(0.5deg);
```
<script async src="//jsfiddle.net/Leo555/L5xfztsb/2/embed/result,html,css/"></script>

### 缩放 scale

缩放 transform: scale(x, y) 表示使元素在 X 轴和 Y 轴缩放。

```css
transform: scale(2, 0.5);
transform: scaleX(2);
transform: scaleY(0.5);
transform: scale3d(2.5, 1.2, 0.3);
transform: scaleZ(0.3);
```
<script async src="//jsfiddle.net/Leo555/bo2zu0fv/embed/result,html,css/"></script>

### 倾斜 skew

倾斜 transform: skew(x, y) 表示 X 轴和 Y 轴倾斜的角度，取值类型为角度值deg。

```css
transform: skew(30deg, 20deg);
transform: skewX(30deg);
transform: skewY(1.07rad);
```

<script async src="//jsfiddle.net/Leo555/h7pox5r3/4/embed/result,html,css/"></script>

### 矩阵变形 matrix 

矩阵变形transform: matrix(a,c,e,b,d,f) 相当于直接应用一个[a c e b d f]变换矩阵。

```css
transform:  matrix(a, c, b, d, tx, ty)
```
<script async src="//jsfiddle.net/Leo555/nn7q512z/embed/result,html,css/"></script>

### 变形原点 transform-origin 
transform-origin 用来定义转换元素的位置，在没有重置 transform-origin 改变元素原点位置的情况下，CSS 的变形操作都是以元素自己中心位置进行。

```css
transform-origin: left;
transform-origin: left top;
transform-origin: 50% 100%;
transform-origin: 50% bottom;
transform: rotate(30deg);
```

<script async src="//jsfiddle.net/Leo555/o992vtgg/embed/result,html,css/"></script>


## 参考资料

- [MDN](https://developer.mozilla.org/zh-CN/docs/Web/CSS/transform)
- [CSS3的变形transform、过渡transition、动画animation学习](http://www.cnblogs.com/imwtr/p/5885885.html)
