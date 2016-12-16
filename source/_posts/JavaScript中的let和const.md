---
title: JavaScript中的let和const
date: 2016-10-16 10:12:21
categories: JavaScript
tags:
- JavaScript
- ES6
---

在 JavaScript 中，是没有块级作用域的概念的，在代码块内声明的变量，其作用域是整个函数作用域而不是块级作用域。let 和 const 作为加强版的 var，让程序员写出更安全，更高效的代码。
<!-- more -->

## let

用 let 定义的变量与 var 有三个区别：块级作用域、不会变量提升，不能定义同名变量。

### 块级作用域

在 ES6 之前，是没有块级作用域的说法的：

```javascript
while (true) {
    var name = 'Leo';
    break;
}
console.log(name); // Leo
```

在 while 体里面定义的变量，在代码块外也可以访问到，而使用 let 就不会出现这个问题。

```javascript
while (true) {
    let name = 'Leo';
    break;
}
console.log(name); // ReferenceError: name is not defined
```

### 变量提升

```javascript
function test() {
    console.log(value); // undefined
    var value = 'something';
    console.log(value); // something
}
test();
```

使用 var 定义的变量，JavaScript 解析器会自动把定义搬到最前面，然后在原来定义的地方赋值。所以上述代码就变成了：

```javascript
var value;
console.log(value); // undefined
value = 'something';
console.log(value); // something
```

而 let 则不会出现这样的问题

```javascript
function test () {
  console.log(value); // ReferenceError: value is not defined
  let value = 'something';
}

test();
```

### 同名变量

用var定义变量时，我们可以多次对它进行定义，例如：

```javascript
var a = 1;
var a = 2;
var a = 3;
```

这样的代码是不会报错的，在let定义的相同块中定义同名变量时就会报错了，例如：

```javascript
let a = 1;
let a = 2; // SyntaxError: Identifier 'a' has already been declared

// or
var a = 1;
let a = 2; // SyntaxError: Identifier 'a' has already been declared
```

## const

const除了具有let的块级作用域和不会变量提升外，还有就是它定义的是常量，在用const定义变量后，我们就不能修改它了。

```javascript
const AA = 2;
AA = 3; //TypeError: Assignment to constant variable.
```

