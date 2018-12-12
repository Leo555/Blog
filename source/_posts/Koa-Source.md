---
title: Koa 源码研读
date: 2018-12-05 23:06:57
categories: 
- JavaScript
tags:
- Koa
- node
---

## 简介

[Koa](https://koajs.com/) 是一个非常轻量的 web 开发框架，由 Express 团队打造。相较于 Express，Koa 使用 async 函数解决异步的问题，并且完全脱离中间件，非常优雅，而且 Koa 代码简洁友好，很适合初学者阅读。


### Koa 代码结构

<img src="/assets/img/koa-source.png" alt="koa-source" style="max-width: 300px;display: block;">

<!--more-->

可以看到 Koa 的结构非常简单，lib 文件夹下面放着 koa 的核心文件：


### application.js

application 是 koa 的入口文件，export 出一个 Application 的类（继承自 events.Emitter）。application 有以下几个主要（public）的 api：

- listen: 实现对 http.createServer() 的封装，传入的参数 callback 中完成中间件合并，错误监听以及上下文的创建和 request 的处理。

- use: 我们通常使用 app.use(function) 将中间件添加到应用程序。use 方法中，koa 将中间件（函数）添加到 this.middleware 数组中。

- callback: koa-compose 将中间件组合在一起, 然后返回一个 request 回调函数，同时给 listen 作为回调。

- toJSON: 返回一个去除私有属性（`_`开头）的对象。


```javascript
module.exports = class Application extends Emitter {
  listen(...args) {
    debug('listen');
    const server = http.createServer(this.callback());
    return server.listen(...args);
  }
  
  use(fn) {
    if (typeof fn !== 'function') throw new TypeError('middleware must be a function!');
    this.middleware.push(fn);
    return this;
  }
  
  callback() {
    const fn = compose(this.middleware);
    
    if (!this.listenerCount('error')) this.on('error', this.onerror);
    
    const handleRequest = (req, res) => {
      const ctx = this.createContext(req, res);
      return this.handleRequest(ctx, fn);
    };
  
    return handleRequest;
  }
}
```

### context.js

context 是我们在使用 koa 中最常接触到的 ctx，就是一个暴露出来的对象。context 中实现了对 cookie 的 get set 操作，这也是我们可以直接使用 ctx 对 cookie 操作的原理。除此之外，ctx 中最重要的是 delegate，也就是委托。我们简单看一下代码：

```javascript
delegate(proto, 'response')
  .method('attachment')
  .method('redirect')
  .method('remove')
  .method('vary')
  .method('set')
  .method('append')
  .method('flushHeaders')
  .access('status')
  .access('message')
  .access('body')
  .access('length')
  .access('type')
  .access('lastModified')
  .access('etag')
  .getter('headerSent')
  .getter('writable');
```

以上的 proto 就是 ctx，实现了对 response 对象的代理，比如我们可以通过使用 ctx.status 来访问 ctx.response.status。

同样的，request 上面的属性和方法也被代理到了 ctx 中：

```javascript

delegate(proto, 'request')
  .method('acceptsLanguages')
  .method('acceptsEncodings')
  .method('acceptsCharsets')
  .method('accepts')
  .method('get')
  .method('is')
  .access('querystring')
  .access('idempotent')
  .access('socket')
  .access('search')
  .access('method')
  .access('query')
  .access('path')
  .access('url')
  .access('accept')
  .getter('origin')
  .getter('href')
  .getter('subdomains')
  .getter('protocol')
  .getter('host')
  .getter('hostname')
  .getter('URL')
  .getter('header')
  .getter('headers')
  .getter('secure')
  .getter('stale')
  .getter('fresh')
  .getter('ips')
  .getter('ip');
```

ctx.hostname 即是 ctx.request.hostname。


### request.js && response.js

request.js 和 response.js 中完成对 Koa Request/Response 对象的封装，可以通过 request.xxx/response.xxx 对其进行操作。其中使用了很多 get 和 set 方法。



## 实现一个简单的 moa

- 首先需要完成对 http 模块的封装，可以使用创建服务器。
- 然后完成 request 和 response 对象的封装，以及将其代理到 context 对象上。
- 然后需要处理中间件以及实现洋葱模型。
- 最后需要完成对错误的处理和异常捕获。
































