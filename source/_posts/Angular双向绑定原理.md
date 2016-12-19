---
title: Angular双向绑定实现原理
date: 2016-12-19 21:33:09
categories: JavaScript
tags:
- JavaScript
- Angular
- socket.io
- $digest
- $apply
- 双向数据绑定
---

# 从一个 demo 讲起

用 Angular + socket.io 做了一个聊天 demo，消息通信没有问题，在 Angular 数据绑定的地方却栽了跟头：明明 model 已经发生了改变，在视图上就是看不到更新。

后来仔细研究，通过使用 “$scope.$apply()” 解决了这个问题。

之前对 Angular 数据双向绑定只有一个大概的印象，并没有深入地了解，正好趁这个机会好好学习一下数据绑定的过程。
<!-- more -->

## 简化代码

服务端代码：

```javascript
'use strict';
let express = require('express');
let app = express();
let http = require('http').Server(app);
let io = require('socket.io')(http);
let path = require('path');

app.use(express.static(path.join(__dirname, 'public')));
app.get('/', function (req, res) {
    res.sendFile(__dirname + '/index.html');
});
io.on('connection', function(socket){
    // 接收事件
    socket.on('chat message', function(msg){
        console.log(msg);
        // 发送事件
        io.emit('chat message', msg);
    });
});
http.listen(3000, function () {
    console.log('listening on :3000');
});
```

客户端代码：

```html
<!doctype html>
<html ng-app="chatApp">
<head>
    <title>Socket.IO demo</title>
    <link rel="stylesheet" type="text/css" href="style.css">
    <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.6.0/angular.min.js"></script>
    <script src="/socket.io/socket.io.js"></script>
    <script src="main.js"></script>
</head>
<body ng-controller="ChatController">
<ul id="messages">
    <li ng-repeat="item in chatMessage">{{item}}</li>
</ul>
<form ng-submit="submit()">
    <input input id="m" ng-model="chatInput" autocomplete="off"/>
    <button>Send</button>
</form>
</body>
</html>
```

CSS 代码略。

JavaScript 代码:

```javascript
'use strict';
angular.module('chatApp', [])
    .controller('ChatController', ['$scope', function ($scope) {
        let socket = io();
        $scope.chatMessage = [];
        // 接收事件
        socket.on('chat message', function (msg) {
            $scope.chatMessage.push(msg);
        });

        $scope.submit = function () {
            //发送事件
            socket.emit('chat message', $scope.chatInput);
            $scope.chatInput = '';
        };
    }]);
```

[完整demo地址](https://github.com/Leo555/socket.io-demo)

socket.io 通过 socket.emit() 发送事件，通过 socket.on() 监听事件。

上面代码似乎没有什么问题，可是运行的时候总是发生视图不更新的情况。
debug 发现 $scope.chatMessage 的值已经发生改变了，按理说 Angular 的 model 与 view 是双向绑定的，model 改变 view 也应该随之更新才对啊，为什么会出现这种情况呢？

## 分析

$scope.chatMessage 发生变化后，没有强制 $digest 循环，监视 chatMessage 的 $watch 没有执行，而我们自己执行一次 $apply，那么这些 $watch 就会看见这些变化，然后根据需要更新 DOM。

要想搞懂上面这句话，还要从 $watch, $apply 和 $digest 讲起。

（1）$watch 队列（$watch list）

