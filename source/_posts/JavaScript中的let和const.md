---
title: JavaScript 中的 let 和 const
date: 2016-10-16 10:12:21
categories: JavaScript
tags:
- let 
- const
- ES6
- TDZ
---

在 JavaScript 中，是没有块级作用域的概念的，在代码块内声明的变量，其作用域是整个函数作用域而不是块级作用域。let 和 const 作为加强版的 var，让程序员写出更安全，更高效的代码。
<!-- more -->

## let

用 let 定义的变量与 var 有三个区别：块级作用域、不会变量提升，不能定义同名变量。

### 块级作用域

var 是函数作用域；let 是块作用域。在 ES6 之前，是没有块级作用域的说法的：

```javascript
while (true) {
  var name = 'Leo'
  break
}
console.log(name) // Leo
```

while 体里面定义的变量在代码块外也可以访问到，而使用 let 就不会出现这个问题。

```javascript
while (true) {
  let name = 'Leo'
  break
}
console.log(name) // ReferenceError: name is not defined
```

### 变量提升

```javascript
function test() {
  console.log(value) // undefined
  var value = 'something'
  console.log(value) // something
}
test()
```

使用 var 定义的变量，JavaScript 解析器会自动把定义搬到最前面，然后在原来定义的地方赋值。所以上述代码就变成了：

```javascript
var value
console.log(value) // undefined
value = 'something'
console.log(value) // something
```

而 let 则不会出现这样的问题

```javascript
function test () {
  console.log(value) // ReferenceError: value is not defined
  let value = 'something'
}

test()
```

### 同名变量

用 var 定义变量时，我们可以多次对它进行定义，例如：

```javascript
var a = 1
var a = 2
var a = 3
```

这样的代码是不会报错的，在 let 定义的相同块中定义同名变量时就会报错了，例如：

```javascript
let a = 1
let a = 2 // SyntaxError: Identifier 'a' has already been declared

// or
var a = 1
let a = 2 // SyntaxError: Identifier 'a' has already been declared
```

## const

const 除了具有 let 的块级作用域和不会变量提升外，还有就是它定义的是常量，在用 const 定义变量后，我们就不能修改它了。

```javascript
const AA = 2
AA = 3 //TypeError: Assignment to constant variable.
```

每一个通过 const 声明的变量必须进行初始化，否则抛出语法错误。

```javascript
const name //Uncaught SyntaxError: Missing initializer in const declaration
```

const 声明的对象不能修改绑定，但是允许修改值，这也就意味着 const 声明的对象可以修改属性值。

```javascript
const person = {
  name: 'Leo'
}
// 可以修改属性值
person.name = 'Leo555'
person.age = 18
// {name: "Leo555", age: 18}
person = {
  name: 'Leo'
} // Uncaught TypeError: Assignment to constant variable. 
```

## 临时死区

var 声明的变量会自动提升， let 和 const 声明的变量则不会，如果在声明之前访问这些变量，则会引发错误。从作用域顶部到声明变量语句之前的这个区域，成为临时死区(temporal dead zone) 简称 TDZ。

```javascript
if (true) {
  console.log(typeof value) // undefined
  var value = '555'
}

if (true) {
  console.log(typeof value) // Uncaught ReferenceError: value is not defined
  let value = '555'
}
```

是不是很神奇，如果 js 解释器逐句解释，在函数作用域内，不解释到最后一句，都无法知道会发生什么。

如果在 let 和 const 作用域之外使用该变量则不会报错。

```javascript
console.log(value) // undefined
if (true) {
  let value = '555'
}
```

## 循环绑定

var 声明使得在循环中创建和使用函数总是有一些问题。比如想要每一秒输出一个递增的数字

```javascript
for (var i = 0; i < 5; i++) {
  setTimeout(() => {
    console.log(i)
  }, i * 1000)
}
```
本来预期输出 0 - 4，结果输出了 5 个 5。 

```javascript
// 在 let 和 const 出现之前是使用闭包
for (var i = 0; i < 5; i++) {
  (function (a) {
    setTimeout(() => {
      console.log(a)
    }, a * 1000)
  })(i)
}
// 使用 let 就简单很多了
for (let i = 0; i < 5; i++) {
  setTimeout(() => {
    console.log(i)
  }, i * 1000)
}
```
let 在循环中每一次都创建一个新的变量，并且将其初始化为当前 i 的值，所以循环内部创建的每个函数都能得到 i 值得副本。for-in 循环和 for-of 循环也是一样的。

而 const 不能用于下面的循环，由 const 声明的 i 为常量，当对齐运行 ++ 运算的时候报错。

```javascript
for (const i = 0; i < 5; i++) { //TypeError: Assignment to constant variable.
  console.log(i)
}
```

for-in 循环和 for-of 循环由于都是创建新的变量将其绑定为当前迭代值，所以不会出现上述问题

```javascript
const aa = [0, 1, 2, 3, 4, 5]
for (const a of aa) {
  console.log(a)
}

for (const a in aa) {
  console.log(a)
}
```