---
title: Gulp快速学习
date: 2017-01-18 16:09:35
categories: JavaScript
tags:
- Gulp
- JavaScript
- Babel
- streaming
---

<img src="/assets/img/自动化.jpg" alt="自动化">
[图片摘自「程序员的那些事」]

## 什么是 gulp

简单的讲，gulp 是一个构建工具，一个基于流的构建工具，一个 nodejs 写的构建工具，使用 gulp 的目的就是为了自动化构建，提高程序员工作效率😂。

<!-- more -->
## 入门指南

1. 全局安装 gulp：

```shell
$ npm install --global gulp
```

2. 作为项目的开发依赖（devDependencies）安装：

```shell
$ npm install --save-dev gulp
```

3. 在项目根目录下创建一个名为 gulpfile.js 的文件：

```javascript
var gulp = require('gulp');
// 默认task
gulp.task('default', () => {
  console.log('Hello World')
});
```
4. 运行 gulp：

```shell
$ gulp
```

默认的名为 default 的任务（task）将会被运行。

想要单独执行特定的任务（task），请输入 

```shell
$ gulp <task> <othertask>。
```

## tasks 依赖

```javascript
var gulp = require('gulp');
// task1
gulp.task('task1', () => {
	console.log('task1');
});
// task2
gulp.task('task2', () => {
	setTimeout(() => {
		console.log('task2')
	}, 1000);
});
// 在执行 default 之前先执行 task1 和 task2
gulp.task('default', ['task1', 'task2'], () => {
	console.log('Hello World');
});
```
输出顺序为：
> task1 
> Hello World
> task2

## 流式处理

1. 在项目根目录下创建 src 文件目录，里面创建 index.js

2. 在项目根目录下创建 dist 文件目录

3. 安装 gulp-uglify
 
```shell
$ npm install gulp-uglify --save-dev
```
4. 使用 gulp 压缩 index.js 并将结果输出

```javascript
var gulp = require('gulp');
var uglify = require('gulp-uglify');
// 压缩js
gulp.task('default', () => {
	gulp.src('src/*.js')
		.pipe(uglify())
		.pipe(gulp.dest('dist'))
});
```
5. 运行 “gulp” 命令后发现在 dist 目录下生产了压缩后的 index.js

6. 解释

gulp.src 是输入； gulp.dest 是输出
pipe 是管道的意思，也是 stream 里核心概念，pipe 将上一个的输出作为下一个的输入。src 里所有 js，经过处理1，处理2，变成输出结果，中间的处理 pipe 可以1步，也可以是n步。第一步处理的结果是第二步的输入，以此类推，就像生产线一样，每一步都是一个 task 是不是很好理解呢？

每个独立操作单元都是一个 task，使用 pipe 来组装 tasks，于是 gulp 就变成了基于 task 的组装工具。


## babel 

babel 用于转化 JavaScript 代码，比如将 ES6 的语法转化成 ES5，或者将 JSX 语法转化为 JavaScript 语法。

假如上文中提到的 index.js 里面的内容如下：

```javascript
'use strict';
import express, { Router } from 'express';
import bodyParser from 'body-parser';
// 定义app和router
let app = express();
let router = Router();
//中间件
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
//路由
router.get('/', (req, res, next) => {
  res.end('Hello World!');
});
app.use('/', router);
//启动app
app.listen(3000, () => {
  console.log('server listening at port 3000...');
});
```
使用 babel 转化为 ES5 语法：

1. 安装 babel-core babel-preset-es2015

```shell
$ npm install --save-dev babel-core babel-preset-es2015
```

2. 创建 **.babelrc** 文件， 配置如下

> {
  "presets": ["es2015"]
}

3. 手动使用 babel 转译：

```shell
$ babel src -d lib
```
4. 安装 gulp-babel

```shell
$  npm install --save-dev gulp-babel
```
5. 编写 gulpfile

在根目录新建一个 gulpfile.babel.js 文件。
gulp 原生并不支持 ES6 语法，但是我们可以告诉 gulp 使用 babel 将 gulpfile 转换为 ES5，方法就是将 gulpfile 命名为 **gulpfile.babel.js**。
 
6. 使用 ES6 编写 **gulpfile.babel.js**

```javascript
import gulp from 'gulp';
import babel from 'gulp-babel';
// 语法转化+压缩
gulp.task('default', () => {
	gulp.src('src/*.js')
		.pipe(babel())
		.pipe(gulp.dest('lib'))
});
```

打开 lib 目录下的 index.js 文件，就可以查看 babel 编译后的 ES5 语法的文件了。

## gulp-watch

开始工作以后，每次改动 index.js 都要手动 gulp 一下实在太麻烦了，使用 gulp-watch 可以监听文件变化，当文件被修改之后，自动将文件转换。

1. 安装 gulp-watch

```shell
$ npm install gulp-watch --save-dev
```
2. 新增 task

```javascript
gulp.task('watch', () => {
	gulp.src('src/*.js')
		.pipe(watch('src/*.js'), {
			verbose: true
		})
		.pipe(babel())
		.pipe(gulp.dest('lib'))
});
```

3. 启动 watch task

```shell
$ gulp watch
```
修改 index.js 后 lib/index.js 也会随之改变。(≧∀≦)ゞ



## 查看全部 tasks

```shell
$ gulp -T
[16:06:54] Requiring external module babel-register
[16:06:54] ├── default
[16:06:54] └── watch
```

## gulp顺序执行

默认的，task 将以最大的并发数执行，也就是说，gulp 会一次性运行所有的 task 并且不做任何等待。如果你想要创建一个序列化的 task 队列，并以特定的顺序执行，需要做两件事：

1. 给出一个提示，来告知 task 什么时候执行完毕，
2. 并且再给出一个提示，来告知一个 task 依赖另一个 task 的完成。

假如我想要 task1 执行完成后再执行 task2， 可以用以下三种方式：

1. 直接返回一个流

```javascript
gulp.task('task1', function () {
    return gulp.watch('src/*.js');
});
//只要加一个return就好了
```

2. 返回一个promise

```javascript
gulp.task('task1', function () {
  var Q = require('q');
  var deferred = Q.defer();
  // do async stuff
  setTimeout(function () {
    deferred.resolve();
  }, 1);

  return deferred.promise;
});
```

3. 使用回调callback

task 的执行函数其实都有个回调，我们只需要在异步队列完成的时候调用它就好了。

```javascript
gulp.task('task1', function (cb) {
  // do async stuff
  setTimeout(function () {
    cb()
  }, 1);
});
```

所以只要依赖的任务是上面三种情况之一，就能保证当前任务在依赖任务执行完成后再执行。这边需要注意的是依赖的任务相互之间还是并行的。需要他们按顺序的话。记得给每个依赖的任务也配置好依赖关系。
