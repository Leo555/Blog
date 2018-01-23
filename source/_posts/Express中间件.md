---
title: Expree中间件
date: 2016-9-12 13:39:18
tags: 
- Node
- Express
categories: JavaScript
---

# 背景
---

去年刚入职不久参与公司Mean技术栈的培训，其中有share过Express的东西，由于当时没有参与过实际项目，对Express理解并不深刻。后来有幸参与ShuttleBus项目，在实际使用中对Express有了些许了解，这里就把自己的想法写出来。

Express是一个非常轻量的Web开发框架，它有两个核心概念：Middleware和Routing，也是Express模块化、组织清晰的关键。

本篇先来讲讲Middleware。
<!-- more -->
# Middleware中间件

Express是什么意思呢，特快列车，或者快递服务，在生活中通常会指快递。想象一下一个快递从生产到消费者手中会经过怎么样的流程？这个快递在工厂加工，然后发货，中途可能经过公路运输，海路运输，航空运输，最后到达收件人手中。如果把Http中的请求（request）比作货物，那层层加工和运输就是 **中间件**，每个流程都是先获取货物，然后处理或者传递，到达终点的时候结束整个流程。不同的是中间件在处理request的过程中，可能会对其进行修改，但是如果你的快递发货后被掉包，你肯定怒不可遏了。

> [中间件（Middleware）](http://www.expressjs.com.cn/guide/using-middleware.html)
是一个函数，它可以访问请求对象（request object (req)）, 响应对象（response object (res)）, 和 web 应用中处于请求-响应循环流程中的中间件，一般被命名为 next 的变量。

# Sample
假如我们有这样一个需求，前端向server发送一个请求，server收到请求后返回给前端一句欢迎语，并且打印一段log。

提取一下发现有server两个功能点：
1. server返回前端欢迎语
2. server打印log

下面我们将这两个功能点抽象为两个Middleware

```javascript
var http = require('http');
var express = require('express');

// 打印log的Middleware
function logMid(request, response, next) {
    console.log(request.method + ': ' + request.url);
    next(); // 调用下一个middleware
}

// 返回欢迎语的middleware
function welcomeMid(request, response) {
    if (request.url === '/') {
        return response.end('Welcome to Home Page!');
    }
    if (request.url === '/about') {
        return response.end('Welcome to About Page!');
    }
    response.end('404, Page Not Found!');
}

var app = express();

// 一次调用Middleware
app.use(logger);
app.use(responser);

var server = http.createServer(app);
server.listen(3000);

```

logMid中间件由于后面要执行下一个中间件，因此手动调用了next()方法，表示将控制权向下传递；而welcomeMid却没有调用，因为它是最后一个中间件，所以可以省略next的调用。

如果当前中间件没有终结请求-响应循环，则必须调用 next() 方法将控制权交给下一个中间件，否则请求就会挂起，直到请求超时。

# Middleware 功能

从上面的Sample可以看出，中间件可以有以下功能：
1. 执行任何代码。可能与请求有关也可能无关（如上的logMid）
2. 修改request和response对象
3. 终结请求-响应循环，比如调用response.end()
4. 调用下一个Middleware

# Express 中间件分类

## 应用级中间件
应用级中间件绑定到 app 对象（express实例）使用 app.use() 和 app.METHOD()， 其中， METHOD 是需要处理的 HTTP 请求的方法，例如 GET, PUT, POST 等等，全部小写。例如：

```javascript
var app = express();

// 没有挂载路径的中间件，应用的每个请求都会执行该中间件
app.use((req, res, next) => {
  console.log('Time:', Date.now());
  next();
});

// 挂载至 /user/:id 的中间件，任何指向 /user/:id 的请求都会执行它
app.use('/user/:id', (req, res, next) => {
  console.log('Request Type:', req.method);
  next();
});

// 路由和句柄函数(中间件系统)，处理指向 /user/:id 的 GET 请求
app.get('/user/:id', (req, res, next) => {
  res.send('USER');
});

```

一个请求装载一组中间件栈。

```javascript
// 一个中间件栈，对任何指向 /user/:id 的 HTTP 请求打印出相关信息
app.use('/user/:id', (req, res, next) => {
  console.log('Request URL:', req.originalUrl);
  next();
}, (req, res, next) => {
  console.log('Request Type:', req.method);
  next();
});
```

作为中间件系统的路由句柄，使得为路径定义多个路由成为可能。在下面的例子中，为指向 /user/:id 的 GET 请求定义了两个路由。第二个路由永远不会被调用，因为第一个路由已经终止了请求-响应循环。

```javascript
// 一个中间件栈，处理指向 /user/:id 的 GET 请求
app.get('/user/:id', (req, res, next) => {
  console.log('ID:', req.params.id);
  next();
}, (req, res, next) => {
  res.send('User Info');
});

// 处理 /user/:id， 打印出用户 id
app.get('/user/:id', (req, res, next) => {
  res.end(req.params.id);
});
```

这两个路由均对应指向 /user/:id的get请求，但是第二个路由永远不会执行，因为第一个路由已经终止了请求-响应循环。
如果在中间栈中跳过剩余的中间件，可以手动调用next('route')将控制权交给下一个中间件。<!--**注意：** next('route') 只对使用 app.VERB() 或 router.VERB() 加载的中间件有效。--> 如下：

```javascript
// 一个中间件栈，处理指向 /user/:id 的 GET 请求
app.get('/user/:id', (req, res, next) => {
  // 如果 user id 为 0, 跳到下一个路由
  if (req.params.id == 0) next('route');
  // 否则将控制权交给栈中下一个中间件
  else next(); //
}, (req, res, next) => {
  // 渲染常规页面
  res.render('regular');
});

// 处理 /user/:id， 渲染一个特殊页面
app.get('/user/:id', function (req, res, next) {
  res.render('special');
});
```


## 路由级中间件

路由级中间件和应用级中间件一样，只是它绑定的对象为 express.Router()。

```
var router = express.Router();
```

路由级使用 router.use() 或 router.VERB() 加载。
上述在应用级创建的中间件系统，可通过如下代码改写为路由级：

```javascript
var app = express();
var router = express.Router();

// 没有挂载路径的中间件，通过该路由的每个请求都会执行该中间件
router.use((req, res, next) => {
  console.log('Time:', Date.now());
  next();
});

// 一个中间件栈，显示任何指向 /user/:id 的 HTTP 请求的信息
router.use('/user/:id', (req, res, next) => {
  console.log('Request URL:', req.originalUrl);
  next();
}, (req, res, next) => {
  console.log('Request Type:', req.method);
  next();
});

// 一个中间件栈，处理指向 /user/:id 的 GET 请求
router.get('/user/:id', (req, res, next) => {
  // 如果 user id 为 0, 跳到下一个路由
  if (req.params.id == 0) next('route');
  // 负责将控制权交给栈中下一个中间件
  else next(); //
}, (req, res, next) => {
  // 渲染常规页面
  res.render('regular');
});

// 处理 /user/:id， 渲染一个特殊页面
router.get('/user/:id', (req, res, next) => {
  console.log(req.params.id);
  res.render('special');
});

// 将路由挂载至应用
app.use('/', router);
```


## 错误处理中间件

错误处理中间件有4个参数，定义错误处理中间件时必须使用这4个参数。即使不需要next对象，也必须在签名中声明它，否则中间件会被识别为一个常规中间件，不能处理错误。

```javascript
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});
```

错误处理中间件一般定义在其他 app.use() 和路由调用后，例如：

```javascript
var bodyParser = require('body-parser');
var methodOverride = require('method-override');

app.use(bodyParser());
app.use(methodOverride());
app.use((err, req, res, next) => {
  // 业务逻辑
});
```

为不同的错误定义不同的中间件

```javascript
var bodyParser = require('body-parser');
var methodOverride = require('method-override');

//logErrors 将请求和错误信息写入标准错误输出、日志或类似服务
function logErrors(err, req, res, next) {
  console.error(err.stack);
  next(err);
}

//
function clientErrorHandler(err, req, res, next) {
  if (req.xhr) {
    res.status(500).send({ error: 'Something blew up!' });
  } else {
    next(err);
  }
}

//errorHandler 能捕获所有错误
function errorHandler(err, req, res, next) {
  res.status(500);
  res.render('error', { error: err });
}

app.use(bodyParser());
app.use(methodOverride());
app.use(logErrors);
app.use(clientErrorHandler);
app.use(errorHandler);
```

如果向 next() 传入参数（除了 ‘route’ 字符串，传入route参数则直接跳入下一个中间件），Express 会认为当前请求有错误的输出，因此会直接进入错误处理中间件，跳过后续其他非错误处理和路由/中间件函数。这点也Promise的catch十分相似，只有Promise链中有一个函数reject了，就跳过所有reject后的函数，直奔catch函数。


1. next(err) 会跳过后续句柄，除了那些用来处理错误的句柄。
2. next('route')会跳过当前中间件栈中剩余的中间件，直接进入下一个中间件。
3. Express中处理错误的middleware只会处理通过next(err)方式报出的错误，而不会处理throw出的错误
4. 即使某个处理错误的middleware是整个栈的最后一个，在定义时也必须写四个参数(err, req, res, next)，以免混淆

Express 内置了一个错误处理句柄，它可以捕获应用中可能出现的任意错误。这个缺省的错误处理中间件将被添加到中间件堆栈的底部。

如果你向 next() 传递了一个 error ，而你并没有在错误处理句柄中处理这个 error，Express 内置的缺省错误处理句柄就是最后兜底的。最后错误将被连同堆栈追踪信息一同反馈到客户端。堆栈追踪信息并不会在 **生产环境**中反馈到客户端。


## 内置中间件

从 4.x 版本开始，除了 express.static, Express 以前内置的中间件现在已经全部单独作为模块安装使用了。

### express.static(root, [options])
express.static是处理静态文件的中间件，参数 root 指提供静态资源的根目录，
可选的 options 参数拥有如下属性。

| 属性 | 描述 | 类型 | 默认值|
| :-| :------: | :------: | :-|
|dotfiles   | 是否对外输出文件名以点（.）开头的文件。|可选值为 “allow”、“deny” 和 “ignore”  |String  “ignore”|
|etag    |是否启用 etag 生成  |  Boolean |true|
|extensions | 设置文件扩展名备份选项 |Array   |[]|
|index   |发送目录索引文件，设置为 false 禁用目录索引。|  Mixed  | “index.html”|
|lastModified   | 设置 Last-Modified 头为文件在操作系统上的最后修改日期。可能值为 true 或 false。|   Boolean| true|
|maxAge  |以毫秒或者其字符串格式设置 Cache-Control 头的 max-age 属性。 |Number  |0|
|redirect  |  当路径为目录时，重定向至 “/”。  | Boolean| true|
|setHeaders  |设置 HTTP 头以提供文件的函数。|  Function     | 无 |

下面来实践一个这个中间件的用法，假如有一张图片 avatar.png放在public文件夹下面：

```javascript
var http = require('http');
var express = require('express');

var app = express();

var options = {
  dotfiles: 'ignore',
  etag: false,
  extensions: ['htm', 'html'],
  index: false,
  maxAge: '1d',
  redirect: false,
  setHeaders: function (res, path, stat) {
    res.set('x-timestamp', Date.now());
  }
}

app.use(express.static('public', options));
var server = http.createServer(app);

server.listen(3000);
```

启动服务后就可以通过 http://localhost:3000/avatar.png 访问图片了。


## 第三方中间件

通过使用第三方中间件从而为 Express 应用增加更多功能。

安装所需功能的 node 模块，并在应用中加载，可以在应用级加载，也可以在路由级加载。

下面的例子安装并加载了一个解析 cookie 的中间件： cookie-parser

> $ npm install cookie-parser
 
```javascript
var express = require('express');
var app = express();
var cookieParser = require('cookie-parser');

// 加载用于解析 cookie 的中间件
app.use(cookieParser());
```

请参考 [**第三方中间件**](http://www.expressjs.com.cn/resources/middleware.html) 获取 Express 中经常用到的第三方中间件列表

