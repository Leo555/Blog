---
title: 使用 requestAnimationFrame 解决滚动点停误触和 scroll 事件延迟
date: 2018-10-09 13:07:37
categories: JavaScript
tags:
- requestAnimationFrame
- touch event
---

## 背景

在手机端网页开发过程中，我们经常会遇到滚动点停误触的问题，最开始想到的解决办法就是判断当前页面（DOM）是否在滚动，如果在滚动，就取消点击或者其他事件。但是在判断页面是否在滚动的时候出现了一些问题，最常见的就 uiwebview scroll 事件延迟，导致我们无法准确判断当前页面（DOM）是否还在滚动。于是想到了使用 requestAnimationFrame 判断某个元素的位置是否发生变化来标识当前页面（DOM）是否在滚动。

<!--more-->

## 常见的滚动点停误触

这是移动端的前端开发中实际遇到的一个问题，当我们的页面出现滚动条的时候，用手滑动屏幕，屏幕上页面内容会快速滚动，不会因为手已经离开了屏幕而滚动停止。当我们想要停止滚动的时候，轻轻点击屏幕，让屏幕停止。但是这个时候有个问题，如果屏幕上点击的位置恰好可以点击，这个时候就会误触。还有一种常见的情况是，滚动已经停止了，点击屏幕发生在其之后，但是感觉像是发生了误触。

### 常用的解决办法

最先想到的解决办法当然是加锁，当页面在滚动的时候，就禁止元素的点击或者 touch 事件。但是这里存在一个问题，有些情况下，我们并不能正确的获得当前页面是否正在发生滚动。比如在 iOS UIWebViews 中, 在视图的滚动过程中，scroll 事件不会被触发；在滚动结束后，scroll 才会触发，参见 Bootstrap issue #16202 。不能正确获取 scroll 事件就无法正确判断当前页面是否正在滚动。看起来我们陷入了僵局。

## 新的解决方案

我们放弃 scroll 事件，使用别的方式判断页面是否滚动。最先想到的就是通过获取某个元素的相对位置，如果在两帧之内位置没有发生变化，那不就证明了当前页面已经不滚动了吗。


### 如何判断元素位置没有发生改变

我们首先给 window 上绑定 touch 事件：

```javascript
window.addEventListener('touchmove', this.onWindowTouchMove.bind(this))
window.addEventListener('touchend', this.onWindowTouchEnd.bind(this))
```

如果发生 touchmove，就认为用户滑动了，在 touchend 的时候通过 getBoundingClientRect() 获取元素位置，再使用 requestAnimationFrame() 判断在两帧之间元素的位置是否发生变化，以此来标识页面滚动是否停止。

```javascript
let element = e.target
let rectObject0 = element.getBoundingClientRect()
let _this = this
window.cancelAnimationFrame(raf)

function step (timestamp) {
    _this.scrollTime = Date.now()
    let rectObject1 = element.getBoundingClientRect()
    if (rectObject0.top !== rectObject1.top) {
        rectObject0 = rectObject1
        raf = window.requestAnimationFrame(step)
    } else {
        _this.isScrolling = false
        window.cancelAnimationFrame(raf)
        return
    }
}

raf = window.requestAnimationFrame(step)
```

下面贴一下完整代码：

ScrollingObserver.js 

```javascript
let scrollTimer
let raf

export default class ScrollingObserver {

    /**
     * 构造函数
     * @param isScrolling 初始值是否为滚动
     * @param scrollTime 设置初始滚动时间
     * @param useRaf 是否使用 requestAnimationFrame
     */
    constructor (isScrolling = false, scrollTime = Date.now(), useRaf = false) {
        this.isScrolling = isScrolling
        this.scrollTime = scrollTime
        this.useRaf = useRaf
        this.initEvents()
    }

    /**
     * 初始化 touch 事件
     */
    initEvents () {
        window.addEventListener('touchmove', this.onWindowTouchMove.bind(this))
        window.addEventListener('touchend', this.onWindowTouchEnd.bind(this))
    }

    /**
     * 移除 touch 事件
     */
    destroy () {
        window.removeEventListener('touchmove', this.onWindowTouchMove.bind(this))
        window.removeEventListener('touchend', this.onWindowTouchEnd.bind(this))
    }

    onWindowTouchMove () {
        this.isScrolling = true
    }

    onWindowTouchEnd (e) {
        if (!this.isScrolling) return
        if (this.useRaf) {
            this.rafHandler(e)
        } else {
            this.setIntervalHandler(e)
        }
    }

    /**
     * 使用 requestAnimationFrame 判断元素位置是否发生变化
     * @param e
     */
    rafHandler (e) {
        let element = e.target
        let rectObject0 = element.getBoundingClientRect()
        let _this = this
        window.cancelAnimationFrame(raf)

        function step (timestamp) {
            _this.scrollTime = Date.now()
            let rectObject1 = element.getBoundingClientRect()
            if (rectObject0.top !== rectObject1.top) {
                rectObject0 = rectObject1
                raf = window.requestAnimationFrame(step)
            } else {
                _this.isScrolling = false
                window.cancelAnimationFrame(raf)
                return
            }
        }

        raf = window.requestAnimationFrame(step)
    }

    /**
     * 使用 setInterval 判断元素位置是否发生变化
     * @param e
     */
    setIntervalHandler (e) {
        let element = e.target
        clearInterval(scrollTimer)
        let rectObject0 = element.getBoundingClientRect()
        scrollTimer = setInterval(() => {
            let rectObject1 = element.getBoundingClientRect()
            this.scrollTime = Date.now()
            if (rectObject0.top === rectObject1.top) {
                this.isScrolling = false
                clearInterval(scrollTimer)
            }
            rectObject0 = rectObject1
        }, 16.7 * 5)
    }
}
```
注意要将实例写成单例模式：

```javascript
import ScrollingObserver from './ScrollingObserver'

let instance;

export default function Scroll () {
    if (!instance) {
        instance = new ScrollingObserver();
    }
    return instance
}
```

使用方式：

```javascript
import Scroll from './scroll'

let isScrolling = Scroll().isScrolling // 页面是否在滚动
let scrollTime = Scroll().scrollTime // 最后滚动时间
```

需要使用 ssr 的同学请注意不要在 node 端初始化，因为构造函数中使用了 window 对象。


## 总结

简单通过判断两帧之间元素的相对位置是否发生变化来判断页面是否正在滚动。使用 requestAnimationFrame 并且只在 touchend 后触发检查机制，对页面性能也不会造成太大的影响。目前来看是不错的解决方案。
















