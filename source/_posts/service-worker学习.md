---
title: service worker 使用
date: 2017-07-09 20:05:46
categories: HTML
tags:
- service worker
- HTML5
- 离线缓存
- postMessage
---

## service worker 简介

service worker 的功能和特性可以总结为以下几点：

1. service worker 是一个独立 worker 线程，独立于当前网页进程，有自己独立的 worker context
2. service worker 的线程能力基于 webworker 而生，通过 postMessage 和 onMessage 进行线程之间的通信；缓存机制是依赖 [cache API](https://developer.mozilla.org/zh-CN/docs/Web/API/Cache) 实现的。service worker = webworker + cache API
3. 一旦被 install 之后，就永远存在，除非被 uninstall；需要的时候可以直接唤醒，不需要的时候自动睡眠
4. 可以可编程拦截代理请求( https 请求)和缓存文件，缓存的文件直接可以被网页进程取到（包括网络离线状态）
5. 离线内容开发者可控；能向客户端推送消息；不能直接操作 dom
6. 必须在 https 环境下才能工作，当然 localhost 或者 127.0.0.1 也是 ok 的
7. service worker 是异步的，内部通过 Promise 实现， localStorage 是同步的，因此 service worker 内不许用使用 loaclStorage
8. 依赖 HTML5 fetch API 和 Promise

<!--more-->

# service worker 使用

## 注册

```javascript
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
        navigator.serviceWorker.register('/sw.js', {scope: '/'})
            .then(function (registration) {
                // 注册成功
                console.log('ServiceWorker registration successful with scope: ', 
                    registration.scope);
            })
            .catch(function (err) {
                // 注册失败:(
                console.log('ServiceWorker registration failed: ', err);
            });
    });
}
```

每次页面加载成功后，就会调用 register() 方法，浏览器将会判断 service worker 线程是否已注册并做出相应的处理。

scope 参数是可选的，默认值为 `sw.js` 所在的文件目录。

打开 chrome 浏览器, 输入 chrome://inspect/#service-workers 可以可以用 DevTools 查看 Service workers 的工作情况。


## 安装

service worker 注册后，浏览器就会尝试安装并激活它，并且在这里完成静态资源的缓存。

所以我们在 `sw.js` 中添加 install 事件

```javascript
this.addEventListener('install', function (event) {
    event.waitUntil(
        caches.open('my-test-cache-v1').then(function (cache) {
            return cache.addAll([
                '/',
                '/index.html',
                '/main.css',
                '/index.js',
                '/sw-lifecycle.jpg'
            ]);
        })
    );
});
```
install 事件一般是被用来完成浏览器的离线缓存功能，service worker 的缓存机制是依赖 [cache API](https://developer.mozilla.org/zh-CN/docs/Web/API/Cache) 实现的。cache API 为绑定在 service worker 上的全局对象，可以用来存储网络响应发来的资源，这些资源只在站点域名内有效，并且一直存在，直到你告诉它不再存储。

### 缓存和返回请求

每次任何被 service worker 控制的资源被请求到时，都会触发 fetch 事件，因此我们可以利用 fetch 事件对资源响应做一些拦截操作

```javascript
this.addEventListener('fetch', function (event) {
    event.respondWith(
        caches.match(event.request).then(function (response) {
            // 如果 service worker 有自己的返回，就直接返回，减少一次 http 请求
            if (response) {
                return response;
            }
            // 如果 service worker 没有返回，从服务器请求资源
            var request = event.request.clone(); // 把原始请求拷过来
            return fetch(request).then(function (httpRes) {
                // 请求失败了，直接返回失败的结果就好了。。
                if (!httpRes && httpRes.status !== 200) {
                    return response;
                }
                // 请求成功的话，再一次缓存起来。
                var responseClone = httpRes.clone();
                caches.open('my-test-cache-v1').then(function (cache) {
                    cache.put(event.request, responseClone);
                });
                return httpRes;
            });
        })
    );
});
```

这样看来，其实可以把 service worker 理解为一个浏览器端的代理服务器，这个代理服务器通过 scope 和 fetch 事件来 hook 站点的请求，来达到资源缓存的功能。

注意：request 和 response 不能直接使用而是通过 clone 的方式使用是因为他们是 stream，因此只能使用一次。

### install vs fetch

- install 的优点是第二次访问即可离线，缺点是需要将需要缓存的资源 URL 在编译时插入到脚本中，增加代码量和降低可维护性；
- fetch 的优点是无需更改编译过程，也不会产生额外的流量，缺点是需要多一次访问才能离线可用。


## service worker 更新

`/sw.js` 控制着页面资源和请求的缓存，如果 `/sw.js` 需要更新应该怎么办呢？

- service worker 控制着整个 App 的离线缓存。 为了避免 service worker 缓存自己导致死锁无法升级，通常将 sw.js 本身的缓存直接交给 HTTP 服务器缓存。
- 更新 `sw.js` 文件，当浏览器获取到了新的文件，发现 `sw.js` 文件发生更新，就会安装新的文件并触发 install 事件。
- 但是此时已经处于激活状态的旧的 service worker 还在运行，新的 service worker 完成安装后会进入 waiting 状态，直到所有已打开的页面都关闭。
- 新服务工作线程取得控制权后，将会触发其 activate 事件。

```javascript
// 安装阶段跳过等待，直接进入 activate
self.addEventListener('install', function (event) {
    event.waitUntil(self.skipWaiting());
});

self.addEventListener('activate', function (evnet) {
    event.waitUntil(
        Promise.all([
            // 更新客户端
            self.clients.claim(),
            // 清理旧版本
            caches.keys().then(function (cacheList) {
                return Promise.all(
                    cacheList.map(function (cacheName) {
                        if (cacheName !== 'my-test-cache-v1') {
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
        ])
    );
});
```

注意：如果 `sw.js` 文件被浏览器缓存，则可能导致更新得不到响应。如遇到该问题，可尝试这么做：在 webserver 上添加对该文件的过滤规则，不缓存或设置较短的有效期。

### 手动更新 /sw.js

也可以借助 `Registration.update()` 手动更新

```javascript
var version = '1.0.1';

navigator.serviceWorker.register('/sw.js').then(function (reg) {
    if (localStorage.getItem('sw_version') !== version) {
        reg.update().then(function () {
            localStorage.setItem('sw_version', version)
        });
    }
});
```
### 自动更新

除了浏览器触发更新之外，service worker 还有一个特殊的缓存策略： 如果该文件已 24 小时没有更新，当 Update 触发时会强制更新。这意味着最坏情况下 service worker 会每天更新一次。

### 调试时更新

可以单独设置调试时 service worker 安装后立即激活：

```javascript
self.addEventListener('install', function() {
    self.skipWaiting();
});
```

## service worker 生命周期

<img src="/assets/img/sw-lifecycle.png" alt="sw-lifecycle">

### service worker 工作流程

service worker 基于注册、安装、激活等步骤在浏览器 js 主线程中独立分担缓存任务。

- 首先在页面的 javaScript 主线程中使用 navigator.serviceWorker.register() 来注册 servcie worker。
- 如果注册成功，service worker 在 ServiceWorkerGlobalScope 环境中运行； 这是一个特殊的 worker context，与主脚本的运行线程相独立，同时也没有访问 DOM 的能力。
- 后台开始安装步骤，通常在安装的过程中需要缓存一些静态资源。install 事件回调中有两个方法：
    - event.waitUntil()：传入一个 Promise 为参数，等到该 Promise 为 resolve 状态为止。
    - self.skipWaiting()：self 是当前 context 的 global 变量，执行该方法表示强制当前处在 waiting 状态的 Service Worker 进入 activate 状态。
- 当 service worker 安装完成后，会接收到一个激活事件（activate event）。激活事件的处理函数中，主要操作是清理旧版本的 service worker 脚本中使用资源。activate 回调中有两个方法：
    - event.waitUntil()：传入一个 Promise 为参数，等到该 Promise 为 resolve 状态为止。
    - self.clients.claim()：在 activate 事件回调中执行该方法表示取得页面的控制权, 这样之后打开页面都会使用版本更新的缓存。旧的 Service Worker 脚本不再控制着页面，之后会被停止。
- 激活成功后 service worker 可以控制页面了，刷新页面可以查看 service worker 的工作成果。

### service worker 事件

- install: service worker 安装成功后被触发的事件，在事件处理函数中可以添加需要缓存的文件。
- activate：当 service worker 安装完成后并进入激活状态，会触发 activate 事件。通过监听 activate 事件你可以做一些预处理，如对于旧版本的更新、对于无用缓存的清理等。
- message：service worker 通过 postMessage API，可以实现与主线程之间的通信。

下面是一个使用 service worker 的 postMessage API 做的一个简单计算器，其中计算部分在 service worker 线程中完成。假如有一些比较耗时的工作，比如大量计算，或者 fetch 数据，可以将其放入 service worker 线程中，以达到提高页面响应的目的。

<iframe defer src="https://lz5z.com/service_worker_postMessage/" frameBorder=0 marginwidth=0 marginheight=0 scrolling=no style="width:500px;height:50px;" width=500  height=50 scrolling=no ALLOWTRANSPARENCY="true"></iframe>

[在线演示](https://lz5z.com/service_worker_postMessage/)
[源码](https://github.com/Leo555/service_worker_postMessage)

- fetch (请求)：当浏览器在当前指定的 scope 下发起请求时，会触发 fetch 事件，并得到传有 response 参数的回调函数，回调中就可以做各种代理缓存的事情了。
- push (推送)：push 事件是为推送准备的。不过首先需要了解一下 [Notification API](https://developer.mozilla.org/zh-CN/docs/Web/API/notification) 和 [PUSH API](https://developer.mozilla.org/zh-CN/docs/Web/API/Push_API)。通过 PUSH API，当订阅了推送服务后，可以使用推送方式唤醒 Service Worker 以响应来自系统消息传递服务的消息，即使用户已经关闭了页面。


## 示例

这个[网站](http://service-worker.org/)记录了很多 service worker demo。

## 参考文档

- [lavas](https://lavas.baidu.com/doc/offline-and-cache-loading/service-worker/service-worker-introduction)
- [Service Worker API-MDN](https://developer.mozilla.org/zh-CN/docs/Web/API/Service_Worker_API)
- [服务工作线程](https://developers.google.com/web/fundamentals/getting-started/primers/service-workers?hl=zh-cn)
- [Service Worker 更新机制](http://harttle.com/2017/04/10/service-worker-update.html)