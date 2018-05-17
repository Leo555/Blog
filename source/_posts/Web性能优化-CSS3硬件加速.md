---
title: Web 性能优化-CSS3 硬件加速(GPU 加速)
date: 2018-05-03 20:10:40
categories: 性能
tags:
- CSS
- 动画
- GPU
---

## CSS3 硬件加速简介

上一篇文章学习了重绘和回流对页面性能的影响，是从比较宏观的角度去优化 Web 性能，本篇文章从每一帧的微观角度进行分析，来学习 CSS3 硬件加速的知识。

CSS3 硬件加速又叫做 GPU 加速，是利用 GPU 进行渲染，减少 CPU 操作的一种优化方案。由于 GPU 中的 transform 等 CSS 属性不会触发 repaint，所以能大大提高网页的性能。

我做了一个页面，左边元素的动画通过 left/top 操作位置实现，右边元素的动画通过 `transform: translate` 实现，你可以打开 chrome 的 “Paint flashing” 查看，绿色部分是正在 repaint 的内容。
    
[查看地址](https://lz5z.com/css3_hardware_speedup/)

从 demo 中可以看到左边的图形在运动时外层有一圈绿色的边框，表示元素不停地 repaint，并且可以看到其运动过程中有丢帧现象，具体表现为运动不连贯，有轻微闪动。
<!--more-->

### 动画与帧

之前学习 flash 的时候，就知道动画是由一帧一帧的图片组成，在浏览器中也是如此。我们首先看一下，浏览器每一帧都做了什么。

<img src="/assets/img/css3_gpu_speedup.png" alt="css3_gpu_speedup" style="max-height: : 66px">

>1. JavaScript：JavaScript 实现动画效果，DOM 元素操作等。
>2. Style（计算样式）：确定每个 DOM 元素应该应用什么 CSS 规则。
>3. Layout（布局）：计算每个 DOM 元素在最终屏幕上显示的大小和位置。由于 web 页面的元素布局是相对的，所以其中任意一个元素的位置发生变化，都会联动的引起其他元素发生变化，这个过程叫 reflow。
>4. Paint（绘制）：在多个层上绘制 DOM 元素的的文字、颜色、图像、边框和阴影等。
>5. Composite（渲染层合并）：按照合理的顺序合并图层然后显示到屏幕上。

### 动画与图层

浏览器在获取 render tree（详细知识可以查看[Web性能优化-页面重绘和回流（重排）](https://lz5z.com/Web%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96-%E9%A1%B5%E9%9D%A2%E9%87%8D%E7%BB%98%E5%92%8C%E5%9B%9E%E6%B5%81/)）后，渲染树中包含了大量的渲染元素，每一个渲染元素会被分到一个图层中，每个图层又会被加载到 GPU 形成渲染纹理。GPU 中 transform 是不会触发 repaint 的，这一点非常类似 3D 绘图功能，最终这些使用 transform 的图层都会由独立的合成器进程进行处理。

过程如下：

render tree -> 渲染元素 -> 图层 -> GPU 渲染 -> 浏览器复合图层 -> 生成最终的屏幕图像。

> TIPS: chrome devtools 中可以开启 Rendering 中的 Layer borders 查看图层纹理。
> 其中黄色边框表示该元素有 3d 变换，表示放到一个新的复合层（composited layer）中渲染，蓝色栅格表示正常的 render layer。

在文章开始给出的[例子](https://lz5z.com/css3_hardware_speedup/)中，我们也可以开启 Layer borders，可以观察到，使用 `transform: translate` 动画的元素，外围有一个黄色的边框，可知其为复合层。

<img src="/assets/img/css3_gpu_lauer_borders.png" alt="css3_gpu_lauer_borders">

在 GPU 渲染的过程中，一些元素会因为符合了某些规则，而被提升为独立的层（黄色边框部分），一旦独立出来，就不会影响其它 DOM 的布局，所以我们可以利用这些规则，将经常变换的 DOM 主动提升到独立的层，那么在浏览器的一帧运行中，就可以减少 Layout 和 Paint 的时间了。

### 创建独立图层

哪些规则能让浏览器主动帮我们创建独立的层呢？

1. 3D 或者透视变换（perspective，transform） 的 CSS 属性。
2. 使用加速视频解码的 video 元素。
3. 拥有 3D（WebGL） 上下文或者加速 2D 上下文的 canvas 元素。
4. 混合插件（Flash)。
5. 对自己的 opacity 做 CSS 动画或使用一个动画 webkit 变换的元素。
6. 拥有加速 CSS 过滤器的元素。
7. 元素有一个包含复合层的后代节点(换句话说，就是一个元素拥有一个子元素，该子元素在自己的层里)。
8. 元素有一个兄弟元素在复合图层渲染，并且该兄弟元素的 z-index 较小，那这个元素也会被应用到复合图层。

关于 z-index 导致的硬件加速的问题，可以查看这篇文章 [CSS3硬件加速也有坑！！](http://div.io/topic/1348)

### 开启 GPU 加速

CSS 中的以下几个属性能触发硬件加速：

1. transform
2. opacity
3. filter
4. will-change

如果有一些元素不需要用到上述属性，但是需要触发硬件加速效果，可以使用一些小技巧来诱导浏览器开启硬件加速。

```css
.element {
    -webkit-transform: translateZ(0);
    -moz-transform: translateZ(0);
    -ms-transform: translateZ(0);
    -o-transform: translateZ(0);
    transform: translateZ(0); 
    /**或者**/
    transform: rotateZ(360deg);
    transform: translate3d(0, 0, 0);
}
```

注意：我在不同的资料中查到的 transform 是否能触发硬件加速的结果不同，自己测试后，发现结果是可以。

### 要注意的问题

（1）过多地开启硬件加速可能会耗费较多的内存，因此什么时候开启硬件加速，给多少元素开启硬件加速，需要用测试结果说话。
（2）GPU 渲染会影响字体的抗锯齿效果。这是因为 GPU 和 CPU 具有不同的渲染机制，即使最终硬件加速停止了，文本还是会在动画期间显示得很模糊。


## 参考文章

- [Increase Your Site’s Performance with Hardware-Accelerated CSS](http://blog.teamtreehouse.com/increase-your-sites-performance-with-hardware-accelerated-css)
- [用CSS开启硬件加速来提高网站性能](http://www.cnblogs.com/rubylouvre/p/3471490.html)
- [css3硬件加速](https://www.jianshu.com/p/f8b1d6e598db)
- [CSS3硬件加速也有坑！！](http://div.io/topic/1348)
- [GPU加速是什么](https://aotu.io/notes/2017/04/11/GPU/index.html)
- [使用CSS3 will-change提高页面滚动、动画等渲染性能](http://www.zhangxinxu.com/wordpress/2015/11/css3-will-change-improve-paint/)