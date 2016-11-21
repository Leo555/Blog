---
title: JavaScript严格模式
date: 2016-11-09 12:58:12
tags: 
- JavaScript
categories: JavaScript
---

![](http://tuku02-qn.icp114.cn/public/16-11-9/47166681.jpg)

# 简介

ECMAScript 5 引入了严格模式（strict mode）的概念。严格模式为JavaScript定义了一种不同的解析与执行模型。在严格模式下，ECMAScript 3中的一些不确定的行为将得到处理，而且对于某些不安全的操作也会抛出错误。（[JavaScript高级程序设计](https://github.com/Leo555/JavaScript/blob/master/books/JavaScript%E9%AB%98%E7%BA%A7%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1%EF%BC%88%E7%AC%AC3%E7%89%88%EF%BC%89%E3%80%91%E4%B8%AD%E6%96%87%20%E9%AB%98%E6%B8%85%20%E5%AE%8C%E6%95%B4%20%E8%AF%A6%E7%BB%86%E4%B9%A6%E7%AD%BE%E7%89%88.pdf)）

<!-- more -->
设立严格模式的目的：
1. 严格模式会将JavaScript陷阱直接变成明显的错误。
2. 严格模式修正了一些引擎难以优化的错误。
3. 同样的代码有些时候严格模式会比非严格模式下更快。
4. 严格模式禁用了一些有可能在未来版本中定义的语法。

# 开启严格模式

使用 'use strict'; 进入严格模式。 严格模式可以应用到整个script标签或个别函数中。

## 为整个script标签开启严格模式

```JavaScript
// 整个语句都开启严格模式的语法
"use strict";
console.log('严格模式script')
```

注意： 如果要为整个script开启严格模式，'use strict'; 一定要放在第一行。 如果担心文件合并带来严格模式与正常模式的混合，可以将script写成自执行函数的形式。

## 为某个函数开启严格模式

```JavaScript
function strict() {
    "use strict";　　
    return "严格模式函数";
}
function notStrict() {
    return "正常模式函数";
}
```

# 严格模式有哪些不同

## 全局变量显式声明

在正常模式下，如果一个变量未声明就直接赋值，相当于创建一个全局变量。这给新人开发者带来便利的同时，给整个项目留下巨大隐患。严格模式将这种失误当成错误。

```JavaScript
'use strict';
a = '严格模式';  //ReferenceError: a is not defined
```

## 不再Silently Fail

严格模式会使引起静默失败(silently fail,注:不报错也没有任何效果)的赋值操作抛出异常。

### 不可变量赋值

例如： NaN 是一个不可写的全局变量. 在正常模式下, 给 NaN 赋值不会产生任何作用; 开发者也不会受到任何错误反馈. 但在严格模式下, 给 NaN 赋值会抛出一个异常。

```JavaScript
'use strict';
NaN = 3; //TypeError: Cannot assign to read only property 'NaN' of #<Object>
```

给不可写属性赋值, 给只读属性(getter-only)赋值赋值, 给不可扩展对象(non-extensible object)的新属性赋值) 都会抛出异常:

```JavaScript
"use strict";

// 给不可写属性赋值
var obj1 = {};
Object.defineProperty(obj1, "x", {
    value: 42,
    writable: false
});
obj1.x = 9; // TypeError: Cannot assign to read only property 'x' of #<Object>

// 给只读属性赋值
var obj2 = {
    get x() {
        return 17;
    }
};
obj2.x = 5; // TypeError: Cannot set property x of #<Object> which has only a getter

// 给不可扩展对象的新属性赋值
var fixed = {};
Object.preventExtensions(fixed);
fixed.newProp = "haha"; // TypeError: Can't add property newProp, object is not extensible
```

### 删除不可删除属性

在严格模式下, 试图删除不可删除的属性时会抛出异常(之前这种操作不会产生任何效果)

```JavaScript
"use strict";
delete Object.prototype; //TypeError: Cannot delete property 'prototype' of function Object()
```

### 参数名唯一

严格模式要求函数的参数名唯一。在正常模式下, 最后一个重名参数名会掩盖之前的重名参数。 之前的参数仍然可以通过 arguments[i] 来访问。

```JavaScript
function sum(a, a, c) { //SyntaxError: Strict mode function may not have duplicate parameter names
    "use strict";
    return a + b + c;
}
```

### 禁止八进制数字语法

```JavaScript
"use strict";
var sum = 015 + // SyntaxError: Octal literals are not allowed in strict mode.
          197 +
          142;
```

## 简化变量的使用

### 禁用 with

先看一个with的例子：

```JavaScript
var x = 17;
var obj = {
    //x: 4
};
with(obj) {
    x = 2;
}

console.log(x);  
```
结果是2， with块内x为全局变量x。

```JavaScript
var x = 17;
var obj = {
    x: 4
};
with(obj) {
    x = 2;
}

console.log(x);  
```
结果是17， with块内x为变量obj.x。

所以with中块内的x究竟是指全局变量x还是obj.x在运行之前是无法得知的，这对编译器优化十分不利，因此严格模式禁用 with。

### eval作用域

严格模式下的 eval 不在为上层范围(surrounding scope,注:包围eval代码块的范围)引入新变量。

在正常模式下,  代码 eval("var x;") 会给上层函数(surrounding function)或者全局引入一个新的变量 x 。
严格模式下，eval语句本身就是一个作用域，它所生成的变量只能用于eval内部。

```JavaScript
var x = 17;
var evalX = eval("'use strict'; var x = 32; x");
console.log(x); //17

var y = 17;
var evalY = eval("var y = 32; y");
console.log(y); //32
```
### 禁止删除声明变量

严格模式禁止删除声明变量。delete name 在严格模式下会引起语法错误

```JavaScript
"use strict";

var x;
delete x; // SyntaxError: Delete of an unqualified identifier in strict mode.

eval("var x; delete x;"); // SyntaxError
```

## 让eval和arguments变的简单

### 绑定或赋值

eval 和 arguments 不能通过程序语法被绑定或赋值。 以下的所有尝试将引起语法错误:

```JavaScript
"use strict";
eval = 17;
arguments++;
++eval;
var obj = {
    set p(arguments) {}
};
var eval;
try {} catch (arguments) {}

function x(eval) {}

function arguments() {}
var y = function eval() {};
var f = new Function("arguments", "'use strict'; return 17;");
```

### arguments对象

arguments对象不再追踪参数的变化

```JavaScript
function f(a) {
    "use strict";
    a = 42;
    return [a, arguments[0]];
}
var pair = f(17);
console.assert(pair[0] === 42);
console.assert(pair[1] === 17);
```

### 不再支持 arguments.callee

正常模式下，arguments.callee 指向当前正在执行的函数。这个作用很小：直接给执行函数命名就可以了。

```JavaScript
"use strict";
var f = function() { return arguments.callee; };
f(); // TypeError: 'caller', 'callee', and 'arguments' properties may not be accessed on strict mode functions or the arguments objects for calls to them
```

## "安全的" JavaScript

严格模式下更容易写出“安全”的JavaScript。


### this关键字

在严格模式下通过this传递给一个函数的值不会被强制转换为一个对象。

```JavaScript
function f() {　　　　
    console.log(this);　　
}　
function f1() {　　　　
    "use strict";　　　　
    console.log(this);
}

f.bind(3)();  //[Number: 3]
f1.bind(3)();  //3
```

对一个普通的函数来说，this总会是一个对象：不管调用时this它本来就是一个对象；还是用布尔值，字符串或者数字调用函数时函数里面被封装成对象的this；还是使用undefined或者null调用函数时this代表的全局对象（使用call, apply或者bind方法来指定一个确定的this）。

这种自动转化为对象的过程不仅是一种性能上的损耗，同时在浏览器中暴露出全局对象也会成为安全隐患。

所以对于一个开启严格模式的函数，指定的this不再被封装为对象，而且如果没有指定this的话它值是undefined。

```JavaScript
"use strict";
function fun() { return this; }
assert(fun() === undefined);
assert(fun.call(2) === 2);
assert(fun.apply(null) === null);
assert(fun.call(undefined) === undefined);
assert(fun.bind(true)() === true);
```


## 为未来的ECMAScript版本铺平道路

### 保留的关键字

在严格模式中一部分字符变成了保留的关键字。这些字符包括implements, interface, let, package, private, protected, public, 
static和yield。在严格模式下，你不能再用这些名字作为变量名或者形参名。

```JavaScript
function package(protected) // !!!
{
    "use strict";
    var implements; // !!!

    interface: // !!!
        while (true) {
            break interface; // !!!
        }

    function private() {} // !!!
}

function fun(static) {
    'use strict';
} // !!!
```

### 函数声明

严格模式只允许在全局作用域或函数作用域的顶层声明函数。也就是说，不允许在非函数的代码块内声明函数。

```JavaScript
"use strict";
if (true)
{
  function f() { } // !!! 语法错误
  f();
}
for (var i = 0; i < 5; i++)
{
  function f2() { } // !!! 语法错误
  f2();
}
function baz() // 合法
{
  function eit() { } // 同样合法
}
```

# 总结

严格模式虽然限制了一部分JavaScript书写和运行的自由，但是随着JavaScript在更大的工程中扮演更重要的角色，规范化是必经之路。


# 参考链接

* [MDN严格模式](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Strict_mode)
* [Javascript 严格模式详解](http://www.ruanyifeng.com/blog/2013/01/javascript_strict_mode.html)