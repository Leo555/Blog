---
title: 使用 IndexedDB 打造前端离线日志系统
date: 2019-03-10 15:13:56
categories: JavaScript
tags:
- IndexedDB
---

## 前言

本文从理论和实战的两个方面讲述前端离线日志系统是如何构建的，其中包括 IndexedDB 基本用法，api 设计，兼容性设计，内容压缩等等。因为内容比较多，我将文章分为 4 部分来讲述整个日志系统的设计。

- 前端数据存储： IndexedDB
- 数据存储压缩： deflate/gzip
- 服务端设计：node + express/koa
- (探索) WebRTC 实现日志获取


### IndexedDB 简介

简单的说，IndexedDB 是一个基于浏览器实现的支持事型务的键值对数据库，支持索引。IndexedDB 虽然不能使用 SQL 语句，但是存储要求数据结构化（既可以存文本，又可以存文件以及blobs)，通过索引产生的指针来完成查询操作。

IndexedDB 有以下优点：

- 基于 JavaScript 对象的键值对存储，简单易用。
- 异步 API。这点对前端来说非常重要，意味着访问数据库不会阻塞调用线程。
- 非常大的存储空间。理论上没有最大值限制，假如超过 50 MB 会需要用户确认请求权限。
- 支持事务，IndexedDB 中任何操作都发生在事务中。
- 支持 Web Workers。同步 API 必须在同 Web Workers 中使用。
- [同源策略](http://www.w3.org/Security/wiki/Same_Origin_Policy)，保证安全。
- 还算不错的[兼容性](https://caniuse.com/#feat=indexeddb)

<!--more-->


### 基本概念


由于 IndexedDB 是低级 API，所以想要使用 IndexedDB 还需要先理解一些基本概念。

- IDBFactory: window.indexedDB，提供对数据库的访问操作。
- IDBOpenDBRequest: indexedDB.open() 的返回结果，表示一个打开的数据库请求。
- IDBDatabase: 表示 IndexedDB 数据库连接，只能通过这个连接来拿到一个数据库事务。
- IDBObjectStore: 对象仓库，一个 IDBDatabase 中可以有多个 IDBObjectStore，类似于 table 或者 MongoDB 中的 document。
- IDBTransaction: 表示一个事务，创建事务的时候需要指明访问的范围和访问类型（读或者写）。
- IDBCursor: 数据库的索引，用来遍历对象存储空间。

### 基本操作

#### 第一步，打开数据库

```javascript
const request = window.indexedDB.open('test', 1)
```

test 表示数据库的名字，如果数据库不存在则主动创建。第二个参数表示数据库的版本，用整数表示，默认是 1。

`indexedDB.open()` 返回一个 IDBOpenDBRequest 对象，通过三个事件 `onerror`, `onsuccess`, `onupgradeneeded` 来处理打开数据库的操作。

```javascript
let db
const request = indexedDB.open('test')
request.onerror = function(event) {
  console.error('open indexedDB error')
}
request.onsuccess = function(event) {
  db = event.target.result
  console.log('open indexedDB success')
}
request.onupgradeneeded = function(event) {
  db = event.target.result
  console.log('upgrade indexedDB success')
}
```

在创建一个新的数据库或者增加已存在的数据库的版本号（当打开数据库时，指定一个比之前更大的版本号）， onupgradeneeded 事件会被触发。

在 `onsuccess` 和 `onupgradeneeded` 中通过 `event.target.result` 来获取数据库的实例。


#### 第二步，新建数据库和表


在使用 `indexedDB.open()` 方法后，数据库就已经新建了，不过里面还没有任何内容。我们通过 `db.createObjectStore()` 来创建表。

```javascript
request.onupgradeneeded = function(event) {
  db = event.target.result
  console.log('upgrade indexedDB success')
  if (!db.objectStoreNames.contains('logs')) {
    const objectStore = db.createObjectStore('logs', { keyPath: 'id' })
  }
}
```

上述代码会创建一个叫做 logs 的表，主键是 id，如果想要让自动生成主键，也可以这样写：

```javascript
const objectStore = db.createObjectStore('logs', { autoIncrement: true })
```

keyPath & autoIncrement

| keyPath | autoIncrement | 描述 |
| :-: | :-: | --- |
| No | No | objectStore 中可以存储任意类型的值，但是想要新增一个值的时候，必须提供一个单独的键参数。 |
| Yes | No | 只能存储 JavaScript 对象，并且对象必须具有一个和 key path 同名的属性。 |
| No | Yes | 可以存储任意类型的值。键会自动生成。 |
| Yes | Yes | 只能存储 JavaScript 对象，通常一个键被生成的同时，生成的键的值被存储在对象中的一个和 key path 同名的属性中。然而，如果这样的一个属性已经存在的话，这个属性的值被用作键而不会生成一个新的键。 |



#### 第三步，创建索引

通过 objectStore 来创建索引：

```javascript
// 创建一个索引来通过时间搜索，时间可能是重复的，所以不能使用 unique 索引。
objectStore.createIndex('time_idx', 'time', { unique: false })
// 使用邮箱建立索引，为了确保邮箱不会重复，使用 unique 索引
objectStore.createIndex("email", "email", { unique: true })
```

IDBObject.createIndex() 的三个参数分别为“索引名称”、“索引对应的属性”、索引属性（是否 unique 索引）。

#### 第四步，插入数据

IndexedDB 中插入数据必须通过事务来完成。

```javascript
// 使用事务的 oncomplete 事件确保在插入数据前对象仓库已经创建完毕
objectStore.transaction.oncomplete = function(event) {
  // 将数据保存到新创建的对象仓库
  const transaction = db.transaction('logs', 'readwrite')
  const store = transaction.objectStore('logs')

  store.add({
    id: 18,
    level: 20,
    time: new Date().getTime(),
    uin: 380034641,
    msg: 'xxxx',
    version: 1
  })
}
```

在初始化 IndexedDB 的时候，会触发 onupgradeneeded 事件，而在以后的对 DB 的调用中，都只会触发 onsuccess 事件。因此我们将对数据库的 CURD 操作做以下封装。

### CURD


#### 新增数据
 
假如前面已经创建了一个 keyPath 为 'id' 的名为 logs 数据库。

```javascript
function addLog (db, data) {
  const transaction = db.transaction('logs', 'readwrite')
  const store = transaction.objectStore('logs')

  const request = store.add(data)

  request.onsuccess = function (e) {
    console.log('write log success')	
  }

  request.onerror = function (e) {
    console.error('write log fail')	
  }
}

addLog(db, {
  id: 1,
  level: 20,
  time: new Date().getTime(),
  uin: 380034641,
  msg: 'add new log',
  version: 1
})
```

写数据的时候需要制定表名，然后创建事务，通过 objectStore 获取 IDBObjectStore 对象，再通过 add 方法进行插入。


#### 更新数据

通过 IDBObjectStore 对象的 put 方法，可以完成对数据的更新操作。

```javascript
function updateLog (db, data) {
  const transaction = db.transaction('logs', 'readwrite')
  const store = transaction.objectStore('logs')

  const request = store.put(data)

  request.onsuccess = function (e) {
    console.log('update log success')	
  }

  request.onerror = function (e) {
    console.error('update log fail')
  }	
}

updateLog(db, {
  id: 1,
  level: 20,
  time: new Date().getTime(),
  uin: 380034641,
  msg: 'this is new log',
  version: 1
})
```

IndexeDB 使用 put 方法更新数据，不过 put 的前提是必须有 unique 索引，IndexeDB 根据 unique 索引作为 key 更新数据。put 方法类似于 upsert，如果 unique 索引对应的值不存在，则直接插入新的数据。

#### 读取数据


通过 IDBObjectStore 对象的 get 方法，可以完成对数据的读取操作。与更新数据相同，通过 get 方法读取数据也需要 unique 索引。读取的数据在 onsuccess 事件中查看。

```javascript
function getLog (db, key) {
  const transaction = db.transaction('logs', 'readwrite')
  const store = transaction.objectStore('logs')

  const request = store.get(key)
  request.onsuccess = function (e) {
    console.log('get log success')
    console.log(e.target.result)
  }

  request.onerror = function (e) {
    console.error('get log fail')	
  }	
}

getLog(db, 1)
```


#### 删除数据


```javascript
function deleteLog (db, key) {
  const transaction = db.transaction('logs', 'readwrite')
  const store = transaction.objectStore('logs')

  const request = store.delete(key)
  request.onsuccess = function (e) {
    console.log('delete log success')
  }

  request.onerror = function (e) {
    console.error('delete log fail')
  }	
}
```

删除数据的时候即使数据不存在也会正常进入 onsuccess 事件中。


#### 使用游标

由于 IndexedDB 中并没有提供 SQL 的能力，所以很多时候我们想要查找一些数据，只能通过遍历的方式。

```javascript
function getAllLogs (db) {
  const transaction = db.transaction('logs', 'readwrite')
  const store = transaction.objectStore('logs')

  const request = store.openCursor()

  request.onsuccess = function (e) {
    console.log('open cursor success')
    const cursor = event.target.result
    if (cursor && cursor.value) {
      console.log(cursor.value)	
      cursor.continue()
    }
  }

  request.onerror = function (e) {
    console.error('oepn cursor fail')
  }	
}
```
cursor 使用类似递归的方式对表进行遍历，通过 cursor.continue() 方法进入下一次循环。

#### 使用索引

在前面的例子中，我们都是通过主键去获取数据的，通过索引的方式，可以让我们用别的属性查找数据。

假设在新建表的时候就创建了 uin 索引。

```javascript
objectStore.createIndex('uin_index', 'uin', { unique: false })
```

在查询数据的时候就可以通过 uin 索引的方式：


```javascript
function getLogByIndex (db) {
  const transaction = db.transaction('logs', 'readonly')
  const store = transaction.objectStore('logs')

  const index = store.index('uin_index')
  const request = index.get(380034641) // 注意这里数据类型要一致

  request.onsuccess = function (e) {
    const result = e.target.result
    console.log(result)
  }
}
```

使用上述索引查询的方式，只能查到第一个满足条件的数据，如果要查到更多的数据，还需要结合 cursor 来操作。

```javascript
function getAllLogsByIndex (db) {
  const transaction = db.transaction('logs', 'readonly')
  const store = transaction.objectStore('logs')

  const index = store.index('uin_index')
  const request = index.openCursor(IDBKeyRange.only(380034641)) // 这里可以直接写值

  request.onsuccess = function (e) {
    const cursor = event.target.result
    if (cursor && cursor.value) {
      console.log(cursor.value)	
      cursor.continue()
    }	
  }
}
```

- IDBKeyRange.only(val) 只获取指定数据
- IDBKeyRange.lowerBuund(val, isOpened) 获取在 val 以前或者小的数据，isOpened 是开闭区间，false 是包含 val（闭区间），true 是不包含 val（开区间）
- IDBKeyRange.upperBuund(val, isOpened) 获取在 val 以后或者大的数据，isOpened 是值开闭区间，false 是包含 val（闭区间），true 是不包含 val（开区间）
- IDBKeyRange.buund(val1, val2, isOpened1, isOpened2) 获取在 value1 与 value2 之间的数据，isOpened1 和 isOpened2 分别是左右开闭区间


一般通过 IDBKeyRange 对象上的上述几个方法来进行多模式的查询操作。


### 如何设计前端离线数据库

在前面的例子中已经可以看到数据库的雏形了，表结构如下：

- from - 日志来源
- id - 上报 id
- level - 日志登记
- msg - 日志信息
- time - 日志产生时间
- uin - 用户唯一标识
- version - 日志版本

这些是上报内容，那接口如何设计呢？

在一个前端离线日志系统中，至少要提供以下五个接口：

1. 清除日志接口。由于用户的日志不断产生，不能让数据无限积累，所以一般设定固定的天数，通过每次系统启动的时候对日志进行检查来清理过期的日志。
2. 写入日志接口。通过异步写日志的方式允许系统不断写入新的日志。
3. 搜索相关接口。包括搜索当前用户的日志，固定时间段日志，以及固定等级日志等。方便上报收集端得到合适的日志信息。
4. 数据整理压缩接口。由于用户的日志量可能非常大， 所以通过对数据进行整理和压缩，可能有效减少上报数据大小。
5. 数据上报接口。


具体可以查看 [wardjs-report](https://github.com/iv-web/wardjs-report/blob/master/src/offline/OfflineDB.js) 项目中的 offline 模块。

小程序中因为有 [`wx.getStorage(Object object)`](https://developers.weixin.qq.com/miniprogram/dev/api/wx.getStorage.html?search-key=getStorage) 接口，因此也可以模拟离线日志的存储功能。 这个分支 [feat_miniprogram](https://github.com/iv-web/wardjs-report/tree/feat_miniprogram) 是我们小程序离线上报的结局方案。


### IndexedDB 性能测试


IndexedDB 的性能非常好，而且基本都是异步操作，所以虽然作用于浏览器，但是常规的读写操作基本不会对产品有额外的影响。


#### 测试环境

> iMac 4GHz i7/16GB DDR3
macOS Majave 10.14.2
Chrome 72.0

#### 数据准备

插入 1w 条日志数据，每条日志长度为500。

#### 测试耗时

连接DB耗时（10次求平均）：3.5ms
插入1条数据（10次求平均）：不到 1 ms
连接DB -> 插入数据 -> 释放连接（10次求平均）：4.3ms
同时插入10条数据（10次求平均）：不到 1 ms

#### 手机端测试

> iPhone 6sp
iOS 12.1.4
safari

#### 测试耗时

连接DB耗时（10次求平均）：2.3ms
插入1条数据（10次求平均）：不到 1 ms
连接DB插入数据释放连接（10次求平均）：2.3ms
同时插入10条数据（10次求平均）：不到 1 ms


测试结果比较奇怪，竟然手机端的成绩要优于 PC 端的成绩。可能跟浏览器有关吧，还有当时测试的时候，电脑中有很多 app 和 chrome tab 没有关，这个可能也有影响吧。

不过我没有再去做测试了，因为上面的数据已经足够惊艳了，你可以理解为，我们简单地插入数据是基本不耗时的。没错，IndexedDB 就是这么强悍。


### 结语

由于内容太多，将文章分为多篇写。本篇简单介绍 IndexedDB 的用法以及性能测试。在前端离线日志系统的构建中，这是最关键的一环，数据存储，既要保证数据的可靠性，又要保持一定的性能，同时不能对用户正常的操作产生副作用，通过我们简单的测试，我觉得 IndexedDB 完全有能力胜任这份工作。



