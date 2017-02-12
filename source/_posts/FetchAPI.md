---
title: Fetch API使用
date: 2017-02-12 16:25:06
categories: JavaScript
tags:
- JavaScript
- W3C
- Fetch API
---

# 背景

在上一章学习 [React 组件](https://lz5z.com/ReactJS%E2%80%94%E7%BB%84%E4%BB%B6/)的时候，想增加 React 对 Ajax 支持的内容，却发现网上的教程竟然用 jQuery 完成 Ajax 请求，个人觉得为了发送一个简单的请求引入 jQuery 库杀鸡焉用宰牛刀啊。其实 W3C 已经有了更好的替代品，那就是： [Fetch API](https://fetch.spec.whatwg.org/)。

## [Fetch API](https://developer.mozilla.org/zh-CN/docs/Web/API/Fetch_API)

Fetch API 的出现与 JavaScript 异步编程模型 Promise 息息相关，在 Fetch API 出现之前，JavaScript 通过 XMLHttpRequest(XHR) 来执行异步请求，XHR 将输入、输出和用事件模型混杂在一个对象里，这种设计并不符合职责分离的原则。而且，基于事件的模型与 Promise 以及基于 Generator 的异步编程模型不太搭。

Fetch API 提供了对 [Headers](https://developer.mozilla.org/zh-CN/docs/Web/API/Headers)，[Request](https://developer.mozilla.org/zh-CN/docs/Web/API/Request)，[Response](https://developer.mozilla.org/zh-CN/docs/Web/API/Response) 三个对象的封装，以及一个 [fetch()](https://developer.mozilla.org/zh-CN/docs/Web/API/GlobalFetch) 函数用来获取网络资源，并且在离线用户体验方面，由于 ServiceWorkers 的介入，Fetch API 也能提供强大的支持。


### fetch() 兼容性

fetch() 方法被定义在 window 对象中，你可以直接在控制台中输入 fetch() 查看浏览器是否支持，gitHub 上有基于低版本浏览器的[兼容实现](https://github.com/github/fetch)。

### 简单示例

fetch() 方法接受一个参数——资源的路径。无论请求成功与否，它都返回一个 promise 对象，resolve 对应请求的 Response 对象。

```javascript
let myImage = document.querySelector('.my-image');
fetch('https://lz5z.com/assets/img/avatar.png')
  .then((response) => {
    if (!response.ok) return new Error(response);
    return response.blob();
  })
  .then((myBlob) => {
    let objectURL = URL.createObjectURL(myBlob);
    myImage.src = objectURL;
  })
  .catch((err) => {
    console.log(err);
  }); 
```
点击查看[效果](/assets/demo/fetch-demo/index.html)

在获取请求的 Response 对象后，通过该对象的 json() 方法可以将结果作为 JSON 对象返回，response.json() 同样会返回一个 Promise 对象，因此可以继续链接一个 then() 方法。相比传统的 XHR 的基于事件类型的编程方式，四不四简单很多哈。

### Request 对象

Fetch API 引入了3个接口，它们分别是 Headers，Request 以及 Response 。他们直接对应了相应的 HTTP 概念，但是基于安全考虑，有些区别，例如支持CORS规则以及保证 cookies 不能被第三方获取。

通过 Request 构造器函数创建一个新的请求对象，这也是建议标准的一部分。 第一个参数是请求的 url，第二个参数是一个选项对象，用于配置请求。然后将 Request 对象传递给 fetch() 方法，用于替代默认的URL字符串。

```javascript
//不缓存响应结果， 方法为 GET
let req = new Request(url, {method: 'GET', cache: 'reload'});
fetch(req).then((response) => {
  //
}).catch((err) => {
  console.log(err);
});
```
除此之外，还可以基于 Request 对象创建新对象，比如将一个 GET 请求创建成为一个 POST 请求

```javascript
let postReq = new Request(req, {method: 'POST'});
console.log(postReq.method); //"POST"
```
### Headers 对象

每个 Request 对象都有一个 header 属性，在 Fetch API 中它对应了一个 Headers 对象。 我们可以使用 Headers 对象构建 Request 对象。而在 Response 对象中也有一个 header 属性，但是响应头是只读的。

Headers 接口是一个简单的多映射的名-值表

```javascript
let headers = new Headers();
headers.append('Accept', 'application/json');
let request = new Request(url, {headers: headers});
fetch(request).then((response) => {
  console.log(response.headers);
});
```
也可以传一个多维数组或者 json：

```javascript
reqHeaders = new Headers({
  "Content-Type": "text/plain",
  "Content-Length": content.length.toString(),
  "X-Custom-Header": "ProcessThisImmediately",
});
//操作 Headers 中的内容
reqHeaders.has("Content-Type") //true
reqHeaders.get("Content-Type") //"text/plain"
reqHeaders.set("Content-Type", "text/html")
reqHeaders.delete("X-Custom-Header");
```

### Response 对象

构建 Respondse 对象有什么用呢？通常 Response 的内容在服务端生成，但是 Fetch API 是浏览器里面的内容啊。

对了，就是为了离线应用，通过 Service Worker 浏览器能够获取请求头的内容，然后通过在浏览器中构建响应头来替换来自服务器的响应头以达到构建离线应用的目的（这方面内容以后再说）。

构建方法

```javascript
let response = new Response(
  JSON.stringify({photos: {photo: []}}),
    {status: 200, headers: headers}
);
```

### steam 支持

Request 和 Response 对象中的 body 只能被读取一次，它们有一个属性叫bodyUsed，读取一次之后设置为true，就不能再读取了。

```javascript
let res = new Response("one time use");
console.log(res.bodyUsed); //false
res.text().then((v) {
  console.log(v); //"one time use"
  console.log(res.bodyUsed); // true
});
```
这样设计的目的是为了之后兼容基于流的 API，让应用只能消费一次 data，这样就允许了 JavaScript 处理大文件例如视频，并且可以支持实时压缩和编辑。

### clone 支持

如何让 body 能经得起多次读取呢？Fetch API 提供了一个 clone() 方法。调用这个方法可以得到一个克隆对象。不过要记得，clone() 必须要在读取之前调用，也就是先 clone() 再读取。

```javascript
let res = new Response("many times use");
console.log(res.bodyUsed); //false
let clone = sheep.clone();
console.log(res.bodyUsed); //false
```

## 总结

值得一提的是，