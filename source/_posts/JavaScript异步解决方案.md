---
title: JavaScript异步解决方案async/await
date: 2016-11-01 22:54:01
tags: 
- Node
- ES7
- async
categories: JavaScript

---

# 简介

异步操作一直都是 JavaScript 中一个比较麻烦的事情，从最早的 callback hell，到TJ大神的 co，再到 Promise 对象，然后ES6中的 Generator 函数，每次都有所改进，但都不是那么彻底，而且理解起来总是很复杂。 

直到 async/await 出现，让写异步的人根本不用关心它是不是异步，可以说是目前最好的 JavaScript 异步解决方案。

ECMAScript 2016(ES7) 中已经确定支持 async/await，那我们怎么能够落后呢？

本文是 async/await 的学习笔记，涵盖基本用法以及一些小demo。

<!-- more -->

## async 函数是什么

阮一峰的 Blog [async 函数的含义和用法](http://www.ruanyifeng.com/blog/2015/05/async.html), 对async的定义一语中的：**async 函数就是 Generator 函数的语法糖。**

假如有一个Generator函数：

```JavaScript
/**
 * Created by leo on 2016/11/1.
 */
'use strict';
const f = (time) => {
    return new Promise(function (resolve) {
        setTimeout(() => {
            resolve(time);
        }, time);
    });
};

const gen = function* () {
    const f1 = yield f(1000);
    const f2 = yield f(2000);
};

```

调用方法:

```JavaScript
let generator = gen();

let ret = generator.next();
ret.value.then((data)=> {
    console.log(data);
    let ret1 = generator.next(data);
    ret1.value.then(function (data) {
        generator.next(data);
    })
});
```

将 gen 函数写成 async 函数，就是下面这样:

```JavaScript
const asyncF = async(()=> {
    let f1 = await(f(1000));
    let f2 = await(f(2000));
});
```

一比较就会发现，async 函数就是将 Generator 函数的星号（*）替换成 async，将 yield 替换成 await，仅此而已。

### 说明

由于目前的大部分浏览器和NodeJS环境还不支持async/await，所以本文程序借助 “asyncawait” 实现，需要额外安装

```shell
$ npm install asyncawait
```

当然如果你对babel比较熟悉的话，也可以通过babel将async/await编译为ES5，就可直接运行了。

##  async/await 使用规则

- async 表示这是一个async函数，await只能用在这个函数里面。
- await 如果后面是异步函数，跟在后面的应该是一个Promise对象。
- await 表示在这里等待Promise返回结果了，再继续执行。

## 获得返回值

可以看到使用 Generator 的时候获取返回值必须使用 .then() 方法，而使用 async/await 就简单很多：

```JavaScript
'use strict';
let async = require('asyncawait/async');
let await = require('asyncawait/await');

const f = (time) => {
    return new Promise(function (resolve) {
        setTimeout(() => {
            resolve(time);
        }, time);
    });
};

(async(()=> {
    let f1 = await(f(1000));
    console.log(f1);
    let f2 = await(f(2000));
    console.log(f2);
}))();

```

await等待的虽然是promise对象，但不必写使用 .then()，也可以得到返回值。

## 捕捉异常

既然 .then() 不用写了，那 .catch()也不用写，可以直接用标准的try 
catch语法捕捉错误

```JavaScript
const f = (time) => {
    return new Promise(function (resolve, reject) {
        setTimeout(() => {
            reject(new Error('error'));
        }, time);
    });
};

(async(()=> {
    try {
        await(f(3000));
    } catch (err) {
        console.log(err.message); // 这里捕捉到错误 `error`
    }
}))();
```

await 命令后面的 Promise 对象，运行结果可能是 rejected，所以最好把 await 命令放在 try...catch 代码块中

## 循环使用 await

await 最好用的地方是可以写在 for 循环里面，这是Promise无法做到的，使得 async/await 看起来更像是同步代码

```JavaScript
const f = (time) => {
    return new Promise(function (resolve) {
        setTimeout(() => {
            resolve(time);
        }, time);
    });
};
(async(()=> {
    for (var i = 1; i <= 10; i++) {
        console.log(`当前是第${i}次等待..`);
        await(f(1000));
    }
}))();
```

