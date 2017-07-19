---
title: CSS3动画—transition
date: 2017-06-12 10:21:22
categories: CSS
tags:
- transition
- 动画
- 过渡
---

CSS3 过渡属性被封装在 transition 规范中，过渡的意义在于，给了 CSS 时间轴的概念，在此之前所有的 CSS 状态变化都是瞬间完成的。过渡可以视为简单版的动画，通过定义开始状态和结束状态，达到样式转变的功能。

目前各大浏览器都支持 transition，所以不加浏览器前缀即可使用。

CSS3 transition 规范定义了以下四个 CSS 属性：

transition-delay(过渡延迟时间)
transition-duration(过渡持续时间)
transition-property(过渡属性) 
transition-timing-function(过渡效果的时间曲线)
<!--more-->

```css
/* transition: 1s 1s width ease; */
transition-property: width;
transition-duration: 1s;
transition-delay: 1s;
transition-timing-function: ease;
```

<script async src="//jsfiddle.net/Leo555/kd7f9khw/embed/result,html,css/"></script>


### 过渡属性 transition-property

默认值为 all，表示浏览器所有能接受的可过渡属性，可以使用单个值或以逗号隔开的多个值。

```css
transition-property: width,height;
transition-duration: 1s,2s;
/* transition: 1s width, 2s height; */
/* transition: width 1s, height 2s; */
```

<script async src="//jsfiddle.net/Leo555/whanfhLk/2/embed/result,html,css/"></script>

可以在 [这里](http://oli.jp/2010/css-animatable-properties/) 和 [这里](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_animated_properties) 查看哪些 CSS 属性支持 transition。

### 延迟时间 transition-delay

transition-delay 属性规定了在执行一个过渡之前的等待时间。IE 和 Opera 不接受 transition-duration 在-10ms和10ms之间的值。默认值0表示不过渡直接看到执行后的结果。单位是秒s，也可以是毫秒ms。

```css
transition-delay: 1s;
transition-delay: 1000ms;
```

### 过渡时间 transition-duration 

动画的执行时间，默认值0表示不过渡。单位是秒s，也可以是毫秒ms。

```css
transition-duration: 1s;
transition-duration: 1000ms;
```

### 过渡效果 transition-timing-function

ease：默认值，缓解效果，变化速度逐渐放慢
linear：线性效果，匀速变化
ease-in：渐显效果，加速变化
ease-out：渐隐效果，减速变化
ease-in-out：渐显渐隐效果
cubic-bezier： 自定义变化速度，可以使用 [cubic-bezier](http://cubic-bezier.com/#.17,.67,.83,.67) 定制想要的效果。

```css
transition: width cubic-bezier(.14,.78,.92,.36) 1s;
```

<script async src="//jsfiddle.net/Leo555/37m1tc5a/1/embed/result,html,css/"></script>

### transition

transition 是一个复合属性，可以同时定义 
transition-property、transition-duration、transition-timing-function、transition-delay 子属性值。

```css
/* property name | duration | timing function | delay */
transition: margin-left 4s ease-in-out 1s;

/* property name | duration | delay */
transition: margin-left 4s 1s;

/* property name | duration */
transition: margin-left 4s;

/* Apply to all changed properties */
transition: all 0.5s ease-out;

/* Apply to multiple properties */
transition: width 2s, height 2s, background-color 2s, transform 2s;
```

写复合属性的时候，四个属性是可以改变顺序的，不过两个时间属性若同时出现，第一个代表 duration，第二个代表 delay，如果只出现一个时间属性，则表示 duration。

### transition 结合 transform

使用 transition 结合 transform 能够完成一些简单的动画效果

<script async src="//jsfiddle.net/Leo555/e7j3p7ru/2/embed/result,html,css/"></script>

使用 transition 做动画简单易用，不过也存在一些缺点：

（1）动画需要事件触发
（2）动画只能执行一次
（3）transition 只能定义开始状态和结束状态，不能定义中间状态

因此如果想要完成比较复杂的动画，还是要用 css3 中的 animation 属性。

## 参考资料
- [CSS动画简介](http://www.ruanyifeng.com/blog/2014/02/css_transition_and_animation.html)
- [MDN-Using CSS transitions](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Transitions/Using_CSS_transitions)