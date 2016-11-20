title: JavaScript中的this
date: 2016-10-08 21:48:25
tags:
- JavaScript
- this
categories: JavaScript
---
# 变幻莫测的 this

在JavaScript中，this的指向变幻莫测。首先必须要说的是，this的指向在函数定义的时候是确定不了的，只有函数执行的时候才能确定this到底指向谁，大概可以分为以下这几种情况。
<!-- more -->

## this 与 window 对象

```javascript
function hi() {
    var name = 'Leo'
    console.log(this.name); //undefined
    console.log(this);  //window
}
hi();
```
在这里this指向调用它的对象，也就是window对象，所以上面的调用 **hi()** 相当于 **window.hi()**

## this 与普通对象

```javascript
var person = {
    name: 'Leo',
    hi: function() {
        console.log(this.name); //Leo
    }
}
person.hi();
```

这里的this指向的是对象 person，因为你调用这个 hi 是通过 person.hi() 执行的。这里再次强调一点，this的指向在函数创建的时候是决定不了的，在调用的时候才能决定，谁调用的就指向谁(是这样的吗？)。

我们再看一个例子：

```javascript
window.name = 'window';
var person = {
    name: 'Leo',
    hi: function() {
        console.log(this.name); //Leo
    }
}
window.person.hi();
```

此时 hi 函数是由 window 对象调用，如果上述说法成立的话应该输出 **window** 才对，那究竟为什么this没有指向window呢？

```javascript
var o = {
    a:10,
    b:{
        a:12,
        fn:function(){
            console.log(this.a); //12
        }
    }
}
o.b.fn();
```
很明显 fn 函数是由对象 o 调用的，而这里的 this 指向了对象 b 呢。

所以this的指向应该为：

1. 如果函数被上一级的对象所调用，那么this指向的就是上一级的对象(上级对象可能为window)。
2. 如果函数中包含多个对象，尽管这个函数是被最外层的对象所调用，this指向的也只是它上一级的对象。

```javascript
var o = {
    a:10,
    b:{
        a:12,
        fn:function(){
            console.log(this.a); //undefined
            console.log(this); //window
        }
    }
}
var j = o.b.fn;
j();
```
这里this指向的是window，因为函数最后是由window对象调用。

总结：**this永远指向的是最后调用它的对象，也就是看它执行的时候是谁调用的**


## 严格模式

在严格模式中，this的指向稍有不同

```javascript
'use strict';
window.name = 'window';
var person = {
    name: 'Leo',
    hi: function() {
        console.log(this.name); //Leo
    }
}
person.hi() // Leo
var hi = person.hi
hi() //  Cannot read property 'name' of undefined
```

第二次调用 hi() 的时候，正常模式会输出 window，而严格模式则会报错，因为在严格模式中，禁止this指向全局对象，所以此时的 this 为 undefined。

## this 与 new

假如函数为构造函数，那this会指向什么呢？

```javascript
function Fn(){
    this.name = "Leo";
}
var a = new Fn();
console.log(a.name); //Leo
```

使用new关键字创建了一个Fn的实例，并且将变量 a 指向这个实例（相当于复制了一份Fn到对象a里面）。此时仅仅只是创建，并没有执行，而调用这个函数Fn的是对象a，那么this指向的自然是对象a。

## this 与 return

如果 new 出来的对象中return一个新对象的时候，情况会有所不同。
```javascript
function Fn() {  
    this.name = 'Leo';  
    return function(){};
}
var a = new Fn;  
console.log(a.name); //undefined
```

JavaScript中所有的函数都是有返回值的，如果没有显式地指明返回值，则默认返回 undefined。

在上面的例子中，Fn返回了一个对象，此时this指向这个对象，所以结果为 undefined。

虽然null也是对象，但是在这里this还是指向那个函数的实例。

```javascript
function Fn() {  
    this.name = 'Leo';  
    return null;
}
var a = new Fn;  
console.log(a.name); //Leo
```

如果返回值是一个对象(非null对象)，那么this指向的就是那个返回的对象，如果返回值不是一个对象那么this还是指向函数的实例。


# 总结

1. 如果一个函数中有this，但是它没有被上级对象调用，那么this指向window或者undefied(严格模式)。
2. 如果一个函数中有this，这个函数有被上一级的对象所调用，那么this指向的就是上一级的对象。
3. 如果一个函数中有this，这个函数中包含多个对象，尽管这个函数是被最外层的对象所调用，this指向的也只是它上一级的对象
4. 如果一个函数中有this，当使用「new + 函数」实例化一个对象时，如果函数的返回值是一个对象(非null对象)，那么this指向的就是那个返回的对象，如果返回值不是一个对象那么this还是函数的实例。
