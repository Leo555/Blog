---
title: nssm将应用写入Windows服务
date: 2016-10-13 9:42:52
tags: 
- Python
- Node
categories: Windows
---

# 安装 
---

[nssm](http://nssm.cc/)是一个Windows服务管理器，可以把应用写入服务，以达到自动重启的功能。

目前最新的版本是2.24，[下载地址](http://nssm.cc/download)。 下载完成以后解压到某个路径下，然后将win64/win32文件路径（D:\nssm-2.24\win64）添加的环境变量Path。
<!-- more -->
# 使用

## Node

假设有一个最简单的node服务器程序
```javascript
var express = require('express');
var app = express();

app.get('/', function(req, res) {
	res.send('Hello World');
});

app.listen(3000, function() {
	console.log('app is listening at port 3000');
});
```
需要将其写入Windows服务。


打开控制台工具。输入:
```
$ nssm install node_test
```
之后会显示出GUI界面：

![GUI](http://i1.piimg.com/567571/bae4d79ec7252de9.png)

输入**Path**为node.exe安装路径，**Startup directory**为应用文件路径，**Arguments**为启动文件

![参数](http://i1.piimg.com/567571/f75d03875221178c.png)

点击Install service

![success](http://p1.bqimg.com/567571/92475175737060e3.png)

然后打开Windows的Services

![Windows Service](http://p1.bqimg.com/567571/b47f06fe33d04914.png)

看到刚才安装的应用已经在Services里面了，并且为“Automatic”，说明它会随着Windows启动而自动启动。

右击-“start”启动该服务，或者在命令行中输入

```
$ nssm start node_test
```

在浏览器中输入**http://localhost:3000/**查看效果
![3000](http://i1.piimg.com/567571/527e0e7fe0357a2e.png)

在控制台输入nssm查看所有命令，可以看出nssm使用极其简单，参考[官方文档](http://nssm.cc/usage)
```
$ nssm install [<servicename>]
$ nssm remove [<servicename>]
$ nssm start <servicename>
$ nssm stop <servicename>
$ nssm restart <servicename>
$ nssm edit <servicename>
```

## bat

Windows中可以使用批处理文件做一些自动化和重复性的工作，bat文件单击即可运行。

假如还是在刚才index.js文件夹下面有一个bat文件,文件内容：
```
node index.js 1> app.log 2>&1
```

我们将bat文件写入Windows Services（记得提前移除刚才写入的node_test服务）
```
$ nssm install node_test_bat
```
这次路径直接选择bat文件即可，因为它是可执行文件。

![bat](http://p1.bpimg.com/567571/13de8c2c5d5396a2.png)

启动bat文件

```
$ nssm start node_test_bat
```
在浏览器中输入**http://localhost:3000/**查看效果,发现服务已经成功开启，而且这个时候在index.js文件夹里面发现了一个
**app.log**文件，里面记录着node服务器的输入日志：
```
app is listening at port 3000
```
于是就在nssm监控管理node服务的同时，还拥有了一个简单的日志系统，是不是很方便。

## Python

将Python应用写入Windows服务也可以使用上述两种方法。

### nssm启动bat服务报错

遇到bat文件双击可以运行，但是写入服务却不能运行的情况。

![](http://p1.bqimg.com/567571/311affdfb01653db.png)

通过Google发现是可能是因为同时安装Python2和Python3导致的，因此改变bat文件为：


```
py -3 main.py
```

写入服务即可。


# 注意

注意非常不推荐把一个运行一次就结束的程序写入Windows Services的，比如Node或者Python脚本里面只有一句输出
```javascript
console.log('Hello');
```

```python
print('Hello')
```
使用Windows自带的Services手动启动：

![](http://p1.bpimg.com/567571/15d4d4abfb4ebb47.png)

使用nssm启动：
```
$ node_test: Unexpected status SERVICE_PAUSED in response to START control.
```
![](http://p1.bpimg.com/567571/b2fb46ada936946f.png)

因为应用启动后立即结束，所以应用进入**Paused**的状态。

但是可以把定时任务写入Services。

如果对Python定时任务感兴趣，可以移步[Python定时任务的实现方式](http://www.lz5z.com/Python%E5%AE%9A%E6%97%B6%E4%BB%BB%E5%8A%A1%E7%9A%84%E5%AE%9E%E7%8E%B0%E6%96%B9%E5%BC%8F/)

---

