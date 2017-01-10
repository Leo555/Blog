---
title: Node.js中child_procss模块
date: 2016-11-16 20:53:46
tags: 
- Node
- 进程
categories: JavaScript
---

# 简介

Node.js 的单线程模型给了它无数的赞美，也带给它无数的诟病。单线程模型，让开发者远离了线程调度的复杂性，使用事件驱动也能开发出一个高并发的服务器；同样也是因为单线程，让CPU密集型计算应用完全不适用。

Node.js 中内建了一个 [child_process](https://nodejs.org/api/child_process.html)模块，可以在程序中创建子进程，从而实现多核并行计算。
<!-- more -->

# [child_process](https://nodejs.org/api/child_process.html)

child_process 是 Node.js 中一个非常重要的模块，主要功能有：
1. 创建子进程
2. 主进程与子进程通信
3. 主进程读取子进程返回结果

使用 child_process 模块创建进程一共有六种方法（Node.js v7.1.0）

### 异步创建进程
1. child_process.**exec**(command[, options][, callback])
2. child_process.**execFile**(file[, args][, options][, callback])
3. child_process.**fork**(modulePath[, args][, options])
4. child_process.**spawn**(command[, args][, options])

### 同步创建进程
1. child_process.**execFileSync**(file[, args][, options])
2. child_process.**execSync**(command[, options])
3. child_process.**spawnSync**(command[, args][, options])

以异步函数中 spawn 是最基本的创建子进程的函数，其他三个异步函数都是对 spawn 不同程度的封装。spawn 只能运行指定的程序，参数需要在列表中给出，而 exec 可以直接运行复杂的命令。
    
## spawn()
spawn从定义来看，有3个参数。
```javascript
child_process.spawn(command[, args][, options])
```
1. command: 执行的命令
2. args: 参数列表，可输入多的参数
3. options: 环境变量对象
4. return: 返回一个ChildProcess 类的实例

### options
> 
1. cwd [String] Current working directory of the child process
2. env [Object] Environment key-value pairs
3. argv0 [String] Explicitly set the value of argv[0] sent to the child process. This will be set to command if not specified.
4. stdio [Array] | [String] Child's stdio configuration. (See options.stdio)
5. detached [Boolean] Prepare child to run independently of its parent process. Specific behavior depends on the platform, see options.detached)
6. uid [Number] Sets the user identity of the process. (See setuid(2).)
7. gid [Number] Sets the group identity of the process. (See setgid(2).)
8. shell [Boolean] | [String] If true, runs command inside of a shell. Uses '/bin/sh' on UNIX, and 'cmd.exe' on Windows. A different shell can be specified as a string. The shell should understand the -c switch on UNIX, or /d /s /c on Windows. Defaults to false (no shell).


spawn 方法创建一个子进程来执行特定命令，它没有回调函数，只能通过监听事件，来获取运行结果。属于异步执行，适用于子进程长时间运行的情况。

```javascript
let child_process = require('child_process');

let path = '.';
let child = child_process.spawn('ls', ['-l', path]);
child.stdout.on('data', (data) => {
    console.log('stdout: ' + data);
});

child.stderr.on('data', (data) => {
    console.log('stderr: ' + data);
});

child.on('close', (code) => {
    console.log('child process exited with code ' + code);
});
```

spawn 方法通过 stream 的方式发数据传给主进程，从而实现了多进程之间的数据交换。

## exec()

exec 方法的定义如下：

```javascript
child_process.exec(command[, options][, callback])
```

exec 方法是对 spawn 方法的封装，增加了 shell/bash 命令解析和回调函数，更加符合 JavaScript 的函数调用习惯。

command参数是一个命令字符串

```javascript
let exec = require('child_process').exec;

let ls = exec('ls -l', function (error, stdout, stderr) {
  if (error) {
    console.error(error.stack);
    console.log('Error code: ' + error.code);
  }
  console.log('Child Process STDOUT: ' + stdout);
});
```

exec 方法第二个参数是回调函数，该函数接受三个参数，分别是发生的错误、标准输出的显示结果、标准错误的显示结果。

由于标准输出和标准错误都是流对象（stream），可以监听 data 事件，因此上面的代码也可以写成下面这样。

```javascript
let exec = require('child_process').exec;
let child = exec('ls -l');

child.stdout.on('data', (data) => {
    console.log('stdout: ' + data);
});
child.stderr.on('data', (data) => {
    console.log('stdout: ' + data);
});
child.on('close', (code) => {
    console.log('closing code: ' + code);
});
```

exec 方法会直接调用 bash（/bin/sh程序） 来解释命令，如果用户输入恶意代码，将会带来安全风险。因此，在有用户输入的情况下，最好不使用 exec 方法，而是使用 execFile 方法。

## execFile()

execFile的定义如下：

```javascript
child_process.execFile(file[, args][, options][, callback])
```
execFile 命令有四个参数，file 和callbakc 为必传参数，options、args 为可选参数：

* file 要执行程序的文件或命令名。字符串类型
* args 要执行程序或命令的参数列表。数组类型
* options 可选参数对象，与exec的options对象相同
* callback 子进程执行完毕的回调函数。与exec的callback函数相同
* 返回值: ChildProcess 对象

execFile 从可执行程序启动子进程。与 exec 相比，execFile 不启动独立的 bash/shell，因此更加轻量级，也更加安全。 execFile 也可以用于执行命令。

```javascript
let childProcess = require('child_process');
let path = ".";
childProcess.execFile('ls', ['-l', path], (err, result) => {
    if (err) {
        console.error(err);
    }
    console.log(result)
});
```

那么，什么时候使用 exec，什么时候使用 execFile 呢？

如果命令参数是由用户来输入的，对于 exec 函数来说是有安全性风险的，因为 Shell 会运行多行命令，比如 ’ls -l .;pwd，如逗号分隔，之后的命令也会被系统运行。但使用 exeFile 命令时，命令和参数分来，防止了参数注入的安全风险。

## fork()

fork 函数，用于在子进程中运行的模块，如 fork('./son.js') 相当于 spawn('node', ['./son.js']) 。与 spawn 方法不同的是，fork 会在父进程与子进程之间，建立一个通信管道，用于进程之间的通信。

假设有一个主进程文件 mian.js:

```javascript
let childProcess = require('child_process');
let son = childProcess.fork('./son.js');

son.on('message', (m) => {
    console.log('Main Listen: ', m);
});
son.send({
    hello: 'son'
});
```
有一个子进程文件 son.js:

```javascript
process.on('message', (m) => {
    console.log('Son Listen:', m);
});
process.send({
    Hello: 'main'
});
```
运行程序：

```
$ node test.js
Son Listen: { hello: 'son' }
Main Listen:  { Hello: 'main' }
```

通过 main.js 启动子进程 son.js，通过 process 在两个进程之间传递数据。

使用 child_process.fork() 生成新进程之后，就可以用 son.send(message, [sendHandle]) 向新进程发送消息，新进程中通过监听message事件，来获取消息，这就是主线程与子线程之间的通信方式。

## Windows

在Windows上执行一个 **.bat** 或者 **.cmd** 文件的方式略有不同。 

假如有一个bat文件 my.bat

### spawn

```javascript
const spawn = require('child_process').spawn;
const bat = spawn('cmd.exe', ['/c', 'my.bat']);

bat.stdout.on('data', (data) => {
  console.log(data);
});

bat.stderr.on('data', (data) => {
  console.log(data);
});

bat.on('exit', (code) => {
  console.log(`Child exited with code ${code}`);
});
```

### exec

```javascript
const exec = require('child_process').exec;
exec('my.bat', (err, stdout, stderr) => {
  if (err) {
    console.error(err);
    return;
  }
  console.log(stdout);
});
```

如果文件名中有空格：

```javascript
const bat = spawn('"my script.cmd"', ['a', 'b'], { shell:true });
// or:
exec('"my script.cmd" a b', (err, stdout, stderr) => {
  // ...
});
```