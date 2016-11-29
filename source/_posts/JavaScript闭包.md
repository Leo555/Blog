---
title: 深入学习JavaScript——闭包
date: 2016-11-24 22:39:45
tags:
- JavaScript
- 闭包
categories: JavaScript
---
# 什么是闭包（Closure）

“函数挂载父环境的时机，如果是定义时就是闭包，如果是执行时就不是闭包。”——忘记哪里看到的。

“闭包是指那些能够访问独立(自由)变量的函数 (变量在本地使用，但定义在一个封闭的作用域中)。换句话说，这些函数可以“记忆”它被创建时候的环境。”——[MDN](https://developer.mozilla.org/cn/docs/Web/JavaScript/Closures)

刚学JavaScript的时候看了这些定义后我就哭了，要想理解闭包还是要看例子。
<!-- more -->

## 举个栗子

```javascript
function foo() {
    let a = 1;
    function inner () {
        console.log(a++);
    };
    return inner;
}

let fun = foo();
fun(); //1
fun(); //2
fun = null; //a被垃圾回收
```

函数 foo 返回一个内部函数 inner，所以“let fun = foo()”的结果应该是“fun = inner” 也就是 “fun = function (){console.log(a++)};”

那么当执行 fun() 的时候 **a=?**，显然在 fun 的外部环境中是没有 a 的定义的，于是就向 inner 函数定义时候的父环境中找 **a**，果然在 foo 函数中找到了。这样就可以理解上面给出的第一个闭包的定义了：一个函数在执行的时候，如果能拿到定义时候父环境的值，这样就是闭包，反之则不是闭包。

那闭包究竟是一个什么东西呢？我们可以把闭包理解成 “函数 + 函数创建时的环境”的组合，比如上面的 inner 函数 + 变量a 就是一个闭包。

# 闭包的用途

通过使用闭包，我们可以做很多事情。

1. JavaScript面向对象
2. 提升代码效率
2. 编写更优雅的代码

## 匿名自执行函数（立即执行函数表达式）

匿名自执行函数有两个作用：
1. 不污染全局变量
2. 函数执行完立刻释放垃圾回收

比如我上面栗子中创建的函数 foo 会自动绑定到全局变量中

```javascript
window.foo()(); //1
```

这样我们每次创建一个函数都必须要使用 const/let/var 去声明一个变量等于函数，不然全局对象的属性会越来越多，从而影响访问速度(因为变量的取值是需要从原型链上遍历的)，而且可能会导致变量冲突。

## 结果缓存

结果缓存是闭包能显著提高程序效率的一个用途。假如有一个处理过程很耗时的函数对象，我们可以将每次处理的结果缓存起来，当再次调用这个函数的时候，就先从缓存中查找。

```javascript
const cacheSearch = (function() {
    var cache = {};

    function search(key) {
        if (key in cache) {
            return cache[key];
        } else {
            cache[key] = `Hello ${key}`; //假如这是一步比较复杂的计算
            return cache[key];
        }
    }
    return search;
})();

```

## 封装

```javascript
const foo = (function() {
    let name = 'name'; // “闭包”内的函数可以访问 name 变量，而 name 变量对于外部却是隐藏的
    return {
        getName: function() { // 通过定义的接口来访问 name
            return name;
        },
        setName: function(new_name) { // 通过定义的接口来修改 name
            name = new_name;
        }
    };
}());

foo.getName(); // 得到 'name'
foo.setName('newName'); // 通过函数接口，我们访问并修改了 name 变量
foo.getName(); // 得到 'newName'
foo.name; // Type error，访问不能
```

## 实现类和继承

```
function Person() {
  let name = 'God';

  return {
    getName: function() {
      return name;
    },
    setName: function(newName) {
      name = newName;
    }
  }
};

let Student = function() {};
//继承自Person
Student.prototype = new Person();
//添加私有方法
Student.prototype.Say = function(name) {
  console.log(`Hello ${name}`);
};
let leo = new Student();
leo.setName('Leo');
leo.Say('World');
console.log(leo.getName());
```

这里的 Person 是一个函数，由于 JavaScript “没有” class 的概念（有 class 关键字）
，所以在 JavaScript 中，new 后面跟的是构造函数。
上面的代码里面定义了 Student 继承自 Person，所以拥有 getName 方法，然后通过prototype添加自己的方法。

# 闭包总结

闭包三个特性：
1. 函数嵌套函数
2. 函数内部可以引用外部的参数和变量
3. 参数和变量不会被垃圾回收机制回收


闭包的优点：
1. 希望一个变量长期驻扎在内存中
2. 避免全局变量的污染
3. 私有成员的存在


闭包的缺点：
1. 闭包的缺点就是常驻内存，会增大内存使用量，使用不当很容易造成内存泄露。
