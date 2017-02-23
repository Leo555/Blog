---
title: css 中的各种单位
date: 2017-02-23 14:15:49
categories: CSS
tags: css
---

之前遇到 css 中需要使用单位的情况，都草草用 px 或者百分比糊弄过去，导致当需要做一个响应式的页面的时候，要重新补一下 css 单位的技术债。

<!-- more -->

## px

px 是 css 中最常用的字体大小单位。
px 就是表示 pixel，像素，是屏幕上显示数据的最基本的点；还有一个看起来很像的单位 pt，pt 就是 point，是印刷行业常用单位，等于1/72英寸，一般在打印的时候使用。
像素 px 是相对于显示器屏幕分辨率而言的，所以一般把它看做一个基础单位，很多其它单位都是以 px 为参照的。

## em rem

em 指的是相对于当前对象内文本的字体大小，比如设置 body 的字体大小(font-size)为 14px，而对 body 内所有的 div 设置字体大小为 1.5em，那么 div 内字体大小就是 14px * 1.5 = 21px

通常写 html 的时候会发生很多嵌套，每个节点都从父阶段继承字体大小，这样很难控制每个层级的字体大小。rem (roo em) 应运而生，rem 是指相对于根节点字体大小，通常根节点是指 html 元素。

```css
html { font-size: 14px; } 
div { font-size: 1.5rem; }
```
这样所有 div 中字体的大小都是 21px 了。

## 百分比

css 中的百分比是一种相对值，使用百分比的关键是找到它的参照物。

| 属性 | 参照 |
| :-:| :------: |
| width & height |宽和高在使用百分比值时，其参照一般都是父元素的 content 的宽和高。|
| margin & padding| margin 和 padding，其任意方向的百分比值，参照都是包含块的宽度。|
| border-radius | 为一个元素的border-radius定义的百分比值，参照物是这个元素自身的尺寸。border-radius:50%;|
| font-size| 参照是直接父元素的 font-size。|
| line-height| 参照是元素自身的font-size|
| vertical-align| 参照是元素自身的line-height|
| bottom、left、right、top| 参照是元素的包含块。left和right是参照包含块的宽度，bottom和top是参照包含块的高度。|
| transform: translate | 参照是元素自己的边界框的尺寸|

## vh vm

移动互联网时代各种设备大小不一，响应式的布局变得更加流行，而响应式布局很大程度上依赖比例规则。

vh 和 vm 也是相对长度，不过其参照是显示窗口的宽度或高度，一般来说 100 vh = viewport 的高度，100vm = viewport 的宽度。

下面一段话是响应式的，你可以缩放浏览器大小来查看效果。

{% raw %}
<!DOCTYPE html>
<html>
<body>
	<div class="css-vm-test">缩放浏览器大小来查看效果</div>
</body>
<style>
	.css-vm-test { font-size: 3vw; color: red; }
</style>
</html>
{% endraw %}

## vmin 和 vmax

vmin 和 vmax 的出现主要是为了移动设备横竖屏切换。