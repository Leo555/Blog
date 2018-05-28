---
title: 《深入浅出Node.js》-理解Buffer
date: 2018-05-28 22:11:29
categories: Node
tags:
- Buffer
- 内存    
---

# 第六章 理解 Buffer

## Buffer 结构

Buffer 是一个像 Array 的对象，主要用来操作字节。Buffer 是一个典型的 JavaScript 与 C++ 结合的模块，它将性能相关的部分用 C++ 实现，将非性能相关的部分用 JavaScript 实现。

Buffer 所占用的内存不是通过 V8 分配的，而是堆外内存。由于 V8 垃圾回收性能的影响，将 Buffer 对象用更高效的专有内存分配回收策略来管理。

Buffer 在 Node 进程启动的时候已经载入了，并将其放在全局对象 global 上，因此无需 require() 就能使用。

### Buffer 对象

Buffer 的元素为 16 进制的两位数，即 0 到 255 的数值。

```javascript
var str = '深入浅出node.js'
var buf = new Buffer(str, 'utf8')
console.log(buf) // <Buffer e6 b7 b1 e5 85 a5 e6 b5 85 e5 87 ba 6e 6f 64 65 2e 6a 73>
```

不同编码的字符串占用的元素个数各不相同，中文在 UTF-8 编码下占用 3 个元素，字母和半角标点占用 1 个元素。

Buffer 可以通过 length 属性得到长度，也可以通过下标访问元素。

<!--more-->

```javascript
var buf = new Buffer(100)
console.log(buf.length) // 100
console.log(buf[10]) // 0
buf[10] = 100
console.log(buf[10]) // 100
```

如果给元素赋值不是 0 到 255 的整数而是小数，Buffer 通过不断 +256 或者不断 -256 得到一个位于 0 - 255 之间的整数。如果是小数，则直接舍弃小数部分，只保留整数部分。

```javascript
buf[10] = -100
console.log(buf[10]) // 156
buf[10] = 300
console.log(buf[10]) // 44
buf[10] = 3.1415
console.log(buf[10]) // 3
```

### Buffer 内存分配

Buffer 对象的内存不是在 V8 堆内存中，而且 Node 的 C++ 层面实现的内存申请。因为处理大量的字节数据不能采用需要一点内存就像操作系统申请一点内存的方式，这可能造成大量内存申请的系统调用，对操作系统有一定压力。Node 使用的策略是在 C++ 层面申请内存，在 JavaScript 中分配内存。

Node 操作 Buffer 使用 slab 内存分配策略。slab 是一种动态内存管理机制，最早出现于 SunOS，目前广泛应用于 Linux。

slab 是一块申请好的固定大小的内存区域。一共有三种状态： full：完全分配状态，partial：部分分配状态；empty：没有分配状态。

当我们需要一个 Buffer 对象，可以通过传入 size 来指定 Buffer 对象大小：

```javascript
new Buffer(size)
```
Node 以 8kb 为界限来区分 Buffer 是大对象还是小对象。这个 8kb 也就是每个 slab 的值，在 JavaScript 层面，以它作为单位进行内存分配。

(1) 小 Buffer 对象

如果指定 Buffer 的大小小于 8kb，Node会按照小对象的方式进行分配。

(2) 大 Buffer 对象

如果是超过 8kb 的对象，将会直接分配一个 SlowBuffer 对象作为 slab 单元，这个 slab 单元将被这个大 Buffer 对象独占。

## Buffer 转换

Buffer 对象可以与字符串直接互相转换，目前支持的字符串编码类型有：ASCII、UTF-8、UTF-16LE/USC-2、Base64、Binary、Hex。

### 字符串转 Buffer

字符串可以通过 Buffer 构造函数转换为 Buffer 对象，存储的只能说一种编码类型。encoding 参数不传递时，默认按照 UTF-8 编码进行转码和存储。一个 Buffer 对象可以存储不同编码类型的字符串转码的值，调用 write() 可以实现。

```javascript
new Buffer(str, [encoding])
buf.write(string, [offset], [length], [encoding])
```

由于可以不断写内容到 Buffer 对象中，并且每次都可以指定编码，所以 Buffer 对象中可以存在多种编码转化后的内容，需要注意的是，每种编码所用的字节长度不同，反转 Buffer 回字符串时需要谨慎处理。

### Buffer 转字符串

```javascript
buf.toString([encoding], [start], [end])
```
可以设置 encoding，start，end 这 3 个参数实现整体或者局部的转化。

### Buffer 不支持的编码类型

由于 Node 中 Buffer 对象只支持上述几种类型的编码，因此可以用 isEncoding() 函数判断编码是否支持转化。

```javascript
Buffer.isEncoding(encoding)
Buffer.isEncoding('GBK') // false
Buffer.isEncoding('UTF-8') // true
```
如果需要转化其它类型的编码，可以借助 [iconv](https://github.com/bnoordhuis/node-iconv) 和 [iconv-lite](https://github.com/ashtuchkin/iconv-lite) 两个模块。

iconv-lite 由纯 JavaScript 实现，iconv 则是通过 C++ 调用 libiconv 库实现，前者比后者更轻量，无需编译和处理环境依赖。

```javascript
var iconv = require('iconv-lite')
// Buffer 转字符串
var str = icon.decode(buf, 'win1251')
// 字符串转 Buffer 
var buf = iconv.encode('Sample input string', 'win1251')
```

## Buffer 拼接

Buffer 常用于从输入流中读取内容

```javascript
var fs = require('fs')
var rs = fs.createReadStream('./test.md')
var data = ''
rs.on('data', function (chunk) {
  data += chunk
})
rs.on('end', function (chunk) {
  console.log(data)
})
```

上述代码在英文环境中一般不会出现问题，但是在中文环境中，经常会看到乱码。data 事件中获取的 chunk 对象为 Buffer 对象，上述代码将其当做字符串处理：`data += chunk` 本质上是 `data = data.toString() + chunk.toString()`。在英文环境中，toString() 不会造成任何问题，但是对于宽字节的中文，却会形成问题。

我们创建 test.md，内容为李白的《静夜思》，修改刚才的代码。

```javascript
var rs = fs.createReadStream('./test.md' { highWaterMark: 11 })
```

输出结果如下：

```
窗前明��光，疑���地上霜，举头��明月，���头思故乡。
```

下面我们来分析乱码是怎么来的。

### 乱码是如何产生的

上面传的参数 highWaterMark 的作用是限制 Buffer 对象的长度为 11。前面说到中文 UTF-8 为 3 个字节，所以前 3 个字“床前明”能够正常输出，后面 11 - 3 * 3 = 2 个字节无法正常解析为 UTF-8 的中文字符串，所以输出乱码。在调用 toString() 的时候，默认使用 UTF-8 编码。后面的乱码都是相同的道理。

### setEncoding() 与 string_decoder()

```javascript
var rs = fs.createReadStream('./test.md', { highWaterMark: 11 })
rs.setEncoding('utf8')
```

setEncoding() 的作用是让 data 事件中传递的不再是一个 Buffer 对象，而是编码后的字符串。改进后重新执行，得到正确的输出。

```
窗前明月光，疑是地上霜，举头望明月，低头思故乡。
```

在调用 setEncoding() 的时候，可读流对象在内部设置了一个 decoder 对象，每次 data 事件都是通过 decoder 对象进行 Buffer 到字符串的解析。

## Buffer 性能

## 总结


