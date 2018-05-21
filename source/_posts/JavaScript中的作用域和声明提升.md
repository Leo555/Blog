---
title: JavaScript 中的作用域和声明提升
date: 2017-04-03 20:19:35
categories: JavaScript
tags:
- Scoping
- Hoisting
---

首先看一个小问题：

```javascript
var a = 'Hello';
(function(){
  alert(a)
  var a = 'World'
})()
```

猜猜弹框中会输出 'Hello' 还是 'World'。揭晓答案： 'undefined'。这里是一个 JavaScript 的小陷阱--JavaScript 变量提升（Hoisting）。

<!--more-->

## JavaScript Scoping

在 ES6 之前，JavaScript 没有块状作用域（block-level scope），只有函数级作用域（function-level scope）。

```javascript
// 块级作用域
var name = 'Leo'
if (name) {
  name = 'Jack' // 这里的 name 是全局变量
  console.log(name) // Jack
}
console.log(name) // Jack
// 函数作用域
var name = 'Leo'
function sayName () {
  var name = 'Jack'
  console.log(name) // Jack    
}
console.log(name) // Leo
```
如果在声明一个变量的时候没有使用 var 关键字，那么变量将成为一个全局变量。

```javascript
(function() {
  a = 'Hello World'
})()
alert(a) // Hello World
```

在 setTimeout 中的函数是在全局作用域中执行的。

```javascript
var a = 1
var b = 2

var obj = {
  a: 10,
  b: 20,
  doCalculate: function () {
    setTimeout(function () {
      console.log(this.a + this.b) // 3
    }, 1000)
  }  
}
obj.doCalculate() // 3
```
为了避免对全局作用域的污染， 所以一般情况下我们尽可能少的声明全局变量。 

关于 ES6 中 使用 let 和 const 声明块级作用域的内容，可以参考 [JavaScript 中的 let 和 const](https://lz5z.com/JavaScript%E4%B8%AD%E7%9A%84let%E5%92%8Cconst/)。

关于 ES5 中严格模式的内容可以参考 [JavaScript 严格模式](https://lz5z.com/JavaScript%E4%B8%A5%E6%A0%BC%E6%A8%A1%E5%BC%8F/)。

关于 JavaScript 中 this 的详细用法可以参考 [JavaScript 中 的this](https://lz5z.com/JavaScript中的this/)。

## JavaScript Hoisting

在 JavaScript 中，函数、变量的声明都会被提升（hoisting）到该函数或变量所在的 scope 的顶部。

```javascript
var a 
console.log(a) // undefined
console.log(b) // undefined
var b
b = a = 10
console.log(a, b) // 10 10
```

在 JavaScript 中，如果声明一个变量，但是为对其进行赋值，那么 JS 引擎会默认让其等于 undefined。所以上述例子中可以看到变量 b 在声明后，被提升到作用域顶部，和 a 一样，获得了 undefined 的值。

除了变量声明会提升，函数声明也会提升。

```javascript
console.log(add(1, 2, 3)) // 6
function add () {
  return eval(Array.prototype.join.call(arguments, '+'))
}
```

值得注意的是：函数声明可以提升，但是函数表达式不能提升。

函数声明： `function fun(arguments) {}`
函数表达式： `var fun = function (arguments) {}`

```javascript
add(1, 2) // 报错：Uncaught TypeError: add is not a function
var add = function () {
  return eval(Array.prototype.join.call(arguments, '+'))  
}
add(1, 2) // 3
```

函数声明会覆盖变量声明。

```javascript
var test 
function test () {
  console.log('test')  
}
console.log(typeof test) // 'function'
```

如果变量已经赋值，则无法别覆盖：

```javascript
var test = 'test'
function test () {}
console.log(typeof test) // 'string'
test = function () {}
console.log(typeof test) // 'function'
```

## 优先级

在 JavaScript 中，一个变量以四种方式进入作用域 scope：

1. 语言内置：所有的作用域中都有 this 和 arguments 关键字（global 没有 arguments）;
2. 形式参数：函数的参数在函数作用域中都是有效的;
3. 函数声明：形如 `function foo() {}`;
4. 变量声明：形如 `var bar`;

函数声明和变量声明总是会被移动（即 hoisting）到它们所在的作用域的顶部。而变量的解析顺序（优先级），与变量进入作用域的 4 种方式的顺序一致，如果一个变量的名字与函数的名字相同，那么函数的名字会覆盖变量的名字，无论其在代码中的顺序如何，但是名字的初始化却是按其在代码中书写的顺序进行的，不受以上优先级的影响。

而变量的解析顺序（优先级），与变量进入作用域的 4 种方式的顺序一致。

```javascript
// 1. var 声明并且赋值高于函数声明
var test = 'test'
function test () {}
console.log(typeof test) // 'string'

// 2. 函数声明高于形参
function test (a) {
  console.log(typeof a) // 'function'
  function a () {}
}
test(100)

// 3. 形参高于语言内置变量
function test (arguments) {
  alert(arguments)
}
test(100) // 100
/*--对比以下--*/
function test1 (a) {
  alert(arguments) // [object Arguments]
}
test1(100)

// 4. 形参优先级高于 var 声明不赋值
function test(){
  alert(arguments)
  var arguments
}
test() // [Object Arguments]
```

变量声明（赋值） > 形参 > 语言内置变量 > 变量声明不赋值 > 函数外部作用域的其他所有声明

总结变量优先级正好验证了作用域链式查找，局部作用域 -> 上一级局部作用域 -> 全局作用域 -> TypeError。

最后看一个例子：

```javascript
function test(arguments) {
  alert(typeof arguments) // 'function'
  var arguments = 20
  function arguments () {}
  alert(arguments) // 20
}
test(100)
```

## 参考文章

[javascript变量声明优先级](http://enml.github.io/site/2014/06/13/js-resolution/)
[深入理解JS中声明提升、作用域（链）和 this 关键字](https://github.com/creeperyang/blog/issues/16)