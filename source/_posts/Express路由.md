---
title: Express路由
date: 2016-9-14 00:00:00
tags: 
- Node
- Express
categories: JavaScript
---
# Routing
---

前面说到Express有两个核心概念：Middleware和Routing。什么是Routing呢，简单来说就是http请求与服务端应答逻辑之间的映射关系。

<!-- more -->
路由是由一个 URI、HTTP 请求（GET、POST等）和若干个句柄组成，它的结构如下： app.METHOD(path, [callback...], callback)， app 是 express 对象的一个实例， METHOD 是一个 HTTP 请求方法， path 是服务器上的路径， callback 是当路由匹配时要执行的函数。

上篇由if else处理不同的get请求就是最原始的路由，但是如果项目稍微大一点，维护无数else将是开发者的噩梦。幸好Express有强大的路由机制，比如解析url，正则表达式匹配等等，给开发者带来小小便利。

# 路由方法

路由方法是http请求时Express对应的方法，主要有app.get()、app.put()、app.post()、app.delete()等。
比如，匹配起GET /和负责回应主页的方法homepageHandler，可以这么写：

```javascript
app.get('/', function homepageHandler(request, response) { ... });
```

而要匹配POST /reivew/new和负责添加新评论的方法addNewReview（假设它已经在别处定义好了）则可以是：

```javascript
app.post('/review/new', addNewReview);
```

app.all()是一个特殊的方法，它的作用是对于一个路径上的所有请求加载中间件，在下面的例子中，来自 “/secret” 的请求，不管使用 GET、POST、PUT、DELETE 或其他任何 http 模块支持的 HTTP 请求，句柄都会得到执行。

```javascript
app.all('/secret', function (req, res, next) {
  console.log('Accessing the secret section ...');
  next(); // pass control to the next handler
});
```

如果处理某个HTTP方法+path对的逻辑很复杂的话，我们也可以把它拆分成middleware栈的形式，依次传给app.METHOD()方法，也就是app.METHOD(path, [middleware...], last_middleware)。

```javascript
var http = require('http');
var express = require('express');
var logger = require('morgan');

var app = express();

app.use(logger('short'));
app.get('/', function (req, res) {
    res.end('Welcome to Homepage');
});

app.get('/about', function (req, res) {
    res.end('Welcome to About page');
});

app.use(function (req, res, next) {
    var err = new Error('404: Page Not Found');
    err.status = 404;
    next(err);
});

app.use(function errorHandler(err, req, res, next) {
    res.status(err.status || 500);
    res.end(err.message);
});

var server = http.createServer(app);

server.listen(3000);
```

以上就是定义routing的第一种方式。

# Router对象

Express的Router对象，也就是之前提到的router-level middleware，可以从两个方面来理解：

可以等同于整个应用中的一个子应用，比如一个RESTful API；它有自己的middleware栈
抽象地来看，可以简单视为整个应用middleware栈中的一片

在开发Express应用的时候，我们可以想想，整个应用是不是可以分拆为许多子应用，例如像上面所提到的，可以有个子应用专门来负责和数据库沟通并返回JSON格式的信息，即一个RESTful API。那么，在代码里，我们就可以新建一个子应用如下：

```javascript
var apiRouter = express.Router();
```

然后，像主应用一样，我们可以为这个子应用添加middleware和routing：

```javascript
apiRouter.get('/id', ...);
apiRouter.post('/review/new', ...);
apiRouter.put(...);
apiRouter.delete(...);
```

最后，把所有path以/api开头的HTTP请求都导入到这个子应用去：

```javascript
app.use('/api', apiRouter);
```

上面的用法跟middleware的设定是一模一样的，只不过这里添加的不是一个方法，而是一个Router对象。这也是Router对象称为router-level middleware的原因。

# 响应方法
下表中响应对象（res）的方法向客户端返回响应，终结请求响应的循环。如果在路由句柄中一个方法也不调用，来自客户端的请求会一直挂起。

| 方法 | 描述 |
| :-| :-|
|[res.download()](http://www.expressjs.com.cn/4x/api.html#res.download)  | 提示下载文件。|
|[res.end()](http://www.expressjs.com.cn/4x/api.html#res.end) |终结响应处理流程。|
|[res.json()](http://www.expressjs.com.cn/4x/api.html#res.json) | 发送一个 JSON 格式的响应。|
|[res.jsonp()](http://www.expressjs.com.cn/4x/api.html#res.jsonp) |发送一个支持 JSONP 的 JSON 格式的响应。|
|[res.redirect()](http://www.expressjs.com.cn/4x/api.html#res.redirect) |  重定向请求。|
|[res.render()](http://www.expressjs.com.cn/4x/api.html#res.render)  |  渲染视图模板。|
|[res.send()](http://www.expressjs.com.cn/4x/api.html#res.send) | 发送各种类型的响应。|
|[res.sendFile](http://www.expressjs.com.cn/4x/api.html#res.sendFile) |   以八位字节流的形式发送文件。|
|[res.sendStatus()](http://www.expressjs.com.cn/4x/api.html#res.sendStatus) |    设置响应状态代码，并将其以字符串形式作为响应体的一部分发送。|

# 参数化的path

假如有两篇文章的请求地址分别为 a/article 和 b/article, 服务器对这两篇文章的Get请求处理逻辑是相同的，Express如何做routing呢？换言之，Express如何把HTTP方法+一类path和相关的逻辑对应起来呢？

最简单的方法就是将这一类path中不同的那一部分看作一个参数，给它取个名字，并在其前加上一个引号。

```javascript
app.get('/:name/article', handleArticleRequest);
```

这样就把所有的形如GET+/xxxxxxx/article的请求和这段负责回复博客的逻辑handleArticleRequest对应了起来。其中:name表示path的这一部分是一个参数，Express会自动把这部分的值存在对应的req.params.name这个对象里，以便这段逻辑使用。假如handleArticleRequest是一个方法，那么它大概会是这么个结构：

```javascript
function handleArticleRequest(req, res) {
    var name = req.params.name;
    // ...
}
```

类似的，当path含有query部分的时候，Express也会自动把query的部分存到req.query这个对象里面。假如说一个path含有query为?p1=v1&p2=v2，那么在处理它的逻辑里，我们可以通过req.query.p1和req.query.p2来访问相应的值（都会是string对象）。

# 结语
以上就是对Express的routing机制的一点简单的介绍。更详细的内容参见 [官网](http://www.expressjs.com.cn/guide/routing.html)。
