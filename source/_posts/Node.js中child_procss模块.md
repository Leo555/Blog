---
title: Node.js中child_procss模块
date: 2016-11-16 20:53:46
tags: 
- Node
- 进程
categories: Node
---

# 简介

Node.js 的单线程模型给了它无数的赞美，也带给它无数的诟病。使用事件驱动，使得开发者不使用多线程也能开发出一个高并发的服务器。单线程模型，让程序员远离了线程调度的复杂性；同样也是因为单线程，让CPU密集型计算应用完全不适用。

Node.js 中内建了一个 child_process 模块，可以在程序中创建子进程，从而实现多核并行计算。
<!-- more -->

# child_process

child_process是 Node.js 中一个非常重要的模块，主要功能有：
1. 创建子进程
2. 子进程与子进程通信
3. 主进程读取子进程返回结果

[官方API](https://nodejs.org/api/child_process.html)

使用 child_process 模块创建进程一共有六种方法（Node.js v7.1.0）
异步创建进程：
1. child_process.exec()
2. child_process.execFile()
3. child_process.fork()
4. child_process.spawn()

同步创建进程：
1. child_process.execFileSync()
2. child_process.execSync()
3. child_process.spawnSync()

以异步函数中spawn是最基本的创建子进程的函数，其他三个异步函数都是对spawn不同程度的封装。spawn只能运行指定的程序，参数需要在列表中给出，而exec可以直接运行复杂的命令。
    
## spawn()
spawn从定义来看，有3个参数。
```JavaScript
child_process.spawn(command[, args][, options])
```
1. command: 执行的命令
2. args: 参数列表，可输入多的参数
3. options: 环境变量对象
4. return: 返回一个ChildProcess 类的实例

spawn方法创建一个子进程来执行特定命令，它没有回调函数，只能通过监听事件，来获取运行结果。属于异步执行，适用于子进程长时间运行的情况。
```JavaScript
let child_process = require('child_process');

let path = '.';
let ls = child_process.spawn('ls', ['-l', path]);
ls.stdout.on('data', (data) => {
    console.log('stdout: ' + data);
});

ls.stderr.on('data', (data) => {
    console.log('stderr: ' + data);
});

ls.on('close', (code) => {
    console.log('child process exited with code ' + code);
});
```

spawn 方法通过stream的方式发数据传给主进程，从而实现了多进程之间的数据交换。

### exec()

exec 方法的定义如下：
```JavaScript
child_process.exec(command[, options][, callback])
```

exec方法是对spawn方法的封装，增加了shell/bash命令解析和回调函数，更加符合JavaScript的函数调用习惯。

command参数是一个命令字符串
```JavaScript

```