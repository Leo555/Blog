---
title: CSS3 动画—animation
date: 2017-06-12 17:23:48
categories: CSS
tags:
- animation
- 动画
---
animation 属性目前还存在浏览器兼容性问题，建议使用 PostCSS 或手动添加浏览器前缀。本文学习使用 animation 属性创建简单动画。
{% raw %}
<!DOCTYPE html>
<html lang="en">
<head>
  <style>
  .anima_div {
    width: 60px;
    height: 40px;
    background: #92B901;
    position: relative;
    padding: 20px 10px 0px 10px;
    animation: animated_div 5s infinite;
    border-radius: 5px;
  }

  @keyframes animated_div {
    0%  {transform: rotate(0deg);left:0px;}
    25%  {transform: rotate(20deg);left:0px;}
    50%  {transform: rotate(0deg);left:300px;}
    55%  {transform: rotate(0deg);left:300px;}
    70%  {transform: rotate(0deg);left:300px;background:#1ec7e6;}
    100%  {transform: rotate(-360deg);left:0px;}
  }
  </style>
</head>
<body>
  <div class="anima_div"></div>
</body>
</html>
{% endraw %}

<!--more-->

## animation

animation 是复合属性，其子属性有：

(1) animation-delay 动画延时
(2) animation-direction 动画在每次运行完后是反向运行还是重新回到开始位置重复运行
(3) animation-duration 动画一个周期的时长
(4) animation-iteration-count 动画重复次数，infinite无限次重复动画
(5) animation-name 指定由 @keyframes
(6) animation-timing-function 设置动画速度曲线，默认是 "ease"
(7) animation-fill-mode 指定动画执行后跳回到初始状态还是保留在结束状态
此外，还有 animation-play-state 属性，但是不能简写到 animation 属性中，该属性允许暂停和恢复动画。

基本语法

```css
animation-name: first_animation;
animation-duration: 5s;
animation-timing-function: linear;
animation-delay: 2s;
animation-iteration-count: infinite;
animation-direction: alternate;
animation-play-state: running;

/* 简写 */
animation: first_animation 5s linear 2s infinite alternate;
```
> animation: name duration timing-function delay iteration-count direction;

### @keyframes

@keyframes 用于规定动画如何从一种样式逐渐变化为另一种样式，其基本用法如下：

```css
@keyframes first_animation {
  0%   {background: red; left:0px; top:0px;}
  25%  {background: yellow; left:200px; top:0px;}
  50%  {background: blue; left:200px; top:200px;}
  75%  {background: green; left:0px; top:200px;}
  100% {background: red; left:0px; top:0px;}
}

@keyframes first_animation {
  from {background: red;}
  50% { background: orange }
  to {background: yellow;}
}
```
关键词 "from" 和 "to"，等同于 0% 和 100%，表示动画开始状态和结束状态。中间状态由浏览器自动推算。

### animation-iteration-count

animation-iteration-count 指定动画播放的次数，默认值为 1。可以指定具体的次数，也可以使用关键字 infinite 让动画无限次播放。

```css
animation-name: first_animation;
animation-duration: 5s;
animation-iteration-count: 1;
/* 等同于 */
animation: first_animation 5s infinite;
```

### animation-fill-mode

animation-fill-mode 指定动画执行后跳回到初始状态还是保留在结束状态。

> animation-fill-mode : none | forwards | backwards | both;

none: 不改变默认行为
forwards：当动画完成后，保持最后一个属性值(在最后一个关键帧中定义) 
backwards：让动画回到第一帧的状态(在第一个关键帧中定义) 
both：根据 animation-direction 轮流应用 forwards 和 backwards 规则

<script async src="//jsfiddle.net/Leo555/3nrjmak2/1/embed/result,html,css/"></script>


### animation-direction

animation-direction 指定对象动画运动的方向，有以下四种取值：

normal：正常方向，默认
reverse：动画反向运行,方向始终与normal相反
alternate：动画会循环正反方向交替运动
alternate-reverse：动画从反向开始，再正反方向交替运动

### animation-play-state

animation-play-state 用于手动控制动画的状态，有 paused 和 running 两种取值：

running：默认值，表示动画正常运动
paused：表示暂停动画

<script async src="//jsfiddle.net/Leo555/0yzvd9nL/2/embed/result,css/"></script>

## 参考资料

- [MDN-CSS Animations](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_Animations)
- [CSS3的变形transform、过渡transition、动画animation学习](http://www.cnblogs.com/imwtr/p/5885885.html)
- [CSS动画简介](http://www.ruanyifeng.com/blog/2014/02/css_transition_and_animation.html)