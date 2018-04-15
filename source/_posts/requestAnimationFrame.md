---
title: 使用 requestAnimationFrame 实现动画
date: 2018-04-14 18:24:28
categories: JavaScript
tags:
- requestAnimationFrame
---

## 如何实现一个动画

我们来实现一个最简单的需求，将一个元素从屏幕左边均匀地移动到屏幕右边。

下面是效果:

{% raw %}
<!DOCTYPE html>
<html lang="en">
<head>
  <style>
    .animate-warpper {
      width: 100%;
      height: 70px;
    }
    @keyframes move_animation {
      0% { left: 0px; }
      100% { left: calc(100% - 60px); }
    }
    .animate-div {
      width: 60px;
      height: 40px;
      position: absolute;
      left: 0;
      border-radius: 5px;
      background: #92B901;
      transform: translateZ(0);
      -webkit-transform: translateZ(0);
      animation: move_animation 5s linear 2s infinite alternate;
    }
  </style>
</head>
<body>
  <section class="animate-warpper"> 
    <div class="animate-div"></div>
  </section>
</body>
</html>
{% endraw %}

<!--more-->

（1）css animation

用 css 实现是最合理也是最高效的。

```css
@keyframes move_animation1 {
  0% { left: 0px; }
  100% { left: calc(100% - 60px); }
}
@keyframes move_animation {
  0% { transform: translateX(0); }
  50% { transform: translateX(250px); }
  100% { transform: translateX(500px)); }    
}
.animate-div {
  width: 60px;
  height: 40px;
  border-radius: 5px;
  background: #92B901;
  left: 0;
  position: absolute;
  transform: translateZ(0);
  -webkit-transform: translateZ(0);
  animation: move_animation 5s linear 2s infinite alternate;
}
```

> 注：`transform:translateZ(0);` 用来开启 chrome GPU 加速，解决动画”卡顿”。
> 在动画中使用 transform 比 left/top 性能更好，能减少浏览器 repaint。

（2）假如用 JS 实现呢

首先想到的是 setInterval/setTimeout，原理就是利用人眼的视觉残留和电脑屏幕的刷新，让元素以连贯平滑的方式逐步改变位置，最终实现动画的效果。

常用的屏幕刷新频率为 60Hz，一些电竞屏幕则为 144Hz。我们以常用的刷新频率为例，60Hz 意味着屏幕每 1000 / 60 ≈ 16.7ms 刷新一次，所以我们设置 setInterval 的间隔为 16.7ms：

```javascript
const animateDiv = document.querySelector('.animate-div')
let i = 0
let inter = setInterval(() => {
  animateDiv.style.left = 1/3 * (++i) + '%'
  if (i === 300) clearInterval(inter)
}, 16.7)
```

setInterval/setTimeout 存在两个问题：
    
> - setTimeout 的执行时间并不是确定的。在 Javascript 中， setTimeout 任务被放进了异步队列中，只有当主线程上的任务执行完以后，才会去检查该队列里的任务是否需要开始执行，因此 setTimeout 的实际执行时间一般要比其设定的时间晚一些。
> - 刷新频率受屏幕分辨率和屏幕尺寸的影响，因此不同设备的屏幕刷新频率可能会不同，而 setTimeout 只能设置一个固定的时间间隔，这个时间不一定和屏幕的刷新时间相同。

以上两种情况都会导致 setTimeout 的执行步调和屏幕的刷新步调不一致，从而引起丢帧现象。 虽然在上述代码中我们将时间间隔设置为 16.7ms，但是还是不能完全避免丢帧的现象。

（3）requestAnimationFrame 

requestAnimationFrame 与 setTimeout/setInterval 最大的区别是由系统自己的刷新机制来决定什么时候调用动画函数，开发者只需要定义好动画函数，这个函数会在浏览器重绘之前调用。

## requestAnimationFrame 简介

requestAnimationFrame 接收一个回调函数作为参数，[DOMHighResTimeStamp](https://developer.mozilla.org/zh-CN/docs/Web/API/DOMHighResTimeStamp)，指示当前被 requestAnimationFrame() 排序的回调函数被触发的时间。回调函数中传入时间戳作为参数，该时间戳是一个十进制数，单位毫秒，最小精度为 1ms。

```javascript
const animateDiv = document.querySelector('.animate-div')
let start = null

// 回调函数
function step(timestamp) {
    if (!start) start = timestamp
    let progress = timestamp - start
    animateDiv.style.left = progress + 'px'
    if (progress < 350) {
        // 在动画没有结束前，递归渲染
        window.requestAnimationFrame(step)
    }
}

// 第一帧渲染
window.requestAnimationFrame(step)
```

### requestAnimationFrame 优势

除了精准控制调用时机以外，requestAnimationFrame 还有两大优点：

- 运行在后台标签页或者隐藏的 iframe 里时，requestAnimationFrame() 暂停调用以提升性能和电池寿命。
- 函数节流：在高频率事件(resize,scroll等)中，为了防止在一个刷新间隔内发生多次函数执行，使用 requestAnimationFrame 可保证每个刷新间隔内，函数只被执行一次。

### cancelAnimationFrame

取消一个先前通过调用 window.requestAnimationFrame()方法返回的动画帧请求。

```javascript
const animateDiv = document.querySelector('.animate-div')
const requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame ||
  window.webkitRequestAnimationFrame || window.msRequestAnimationFrame

const cancelAnimationFrame = window.cancelAnimationFrame || window.mozCancelAnimationFrame

let start = null
let myReq = null

function step(timestamp) {
  let progress = timestamp - start
  animateDiv.style.left = progress + 'px'
  if (progress < 2000) {
    myReq = requestAnimationFrame(step)
  }
}
myReq = requestAnimationFrame(step)

setTimeout(() => {
  window.cancelAnimationFrame(myReq)
}, 200)
```

### 优雅降级

requestAnimationFrame 目前还存在兼容性问题，使用 [requestAnimationFrame polyfill](https://github.com/darius/requestAnimationFrame) 来进行优雅降级。

```javascript
if (!Date.now)
    Date.now = function() { return new Date().getTime(); };

(function() {
    'use strict';
    
    let vendors = ['webkit', 'moz'];
    for (let i = 0; i < vendors.length && !window.requestAnimationFrame; ++i) {
        let vp = vendors[i];
        window.requestAnimationFrame = window[vp+'RequestAnimationFrame'];
        window.cancelAnimationFrame = (window[vp+'CancelAnimationFrame']
                                   || window[vp+'CancelRequestAnimationFrame']);
    }
    if (/iP(ad|hone|od).*OS 6/.test(window.navigator.userAgent) // iOS6 is buggy
        || !window.requestAnimationFrame || !window.cancelAnimationFrame) {
        let lastTime = 0;
        window.requestAnimationFrame = function(callback) {
            let now = Date.now();
            let nextTime = Math.max(lastTime + 16, now);
            return setTimeout(function() { callback(lastTime = nextTime); },
                              nextTime - now);
        };
        window.cancelAnimationFrame = clearTimeout;
    }
}());
```


## 参考资料

- [MDN-CSS requestAnimationFrame](https://developer.mozilla.org/zh-CN/docs/Web/API/Window/requestAnimationFrame)
- [深入理解 requestAnimationFrame](http://mp.weixin.qq.com/s/_m1flYySn6sgAROYbXqltg)
- [CSS动画之硬件加速](https://www.w3cplus.com/css3/introduction-to-hardware-acceleration-css-animations.html)