---
title: JavaScript函数式编程—数组方法
date: 2016-9-23 10:59:11
tags: 
- JavaScript
- Node
categories: JavaScript
---
# 背景
---

闲逛的时候发现一个有趣的网站，[ECMAScript](http://kangax.github.io/compat-table/es5/) 里面介绍了各种JS引擎和Node版本对JavaScript特性的支持，从ECMAScript5开始到未来2017将会有的特性。 ES5是JavaScript历史上最具革命的一个版本，开发者们开始摒弃对旧版本 IE 浏览器的支持，使用统一的风格编写JavaScript，并且新的ECMAScript规范也开始启动。目前几乎所有的浏览器环境和Node.JS环境都支持ES5。

本文将介绍在JavaScript函数式编程中最常使用的几个数组方法，这些我们都习以为常的方法，来自[ES5](http://kangax.github.io/compat-table/es5/)
ES5中一共有10个数组方法
![数组方法](http://i1.piimg.com/567571/14b64c75ee0bcc33.png)
从后面的全绿我们可以知道，ES5的标准以及普及，以上这些方法可以放心使用。
下面是JavaScript函数式编程最常见的三个方法：filter、 map、 reduce。

# Array.prototype.filter()

filter方法用于对数组进行条件过滤

不用 filter() 时

```JavaScript
'use strict';
let arr = [
    {"name":"apple", "count": 2},
    {"name":"orange", "count": 5},
    {"name":"pear", "count": 3},
    {"name":"orange", "count": 16},
];
    
let newArr = [];

for(let i of arr){
    if(i.name === "orange" ){
        newArr.push(i);
    }
}

console.log("Filter results:", newArr);
```

使用filter()

```JavaScript
'use strict';
let arr = [
    {"name":"apple", "count": 2},
    {"name":"orange", "count": 5},
    {"name":"pear", "count": 3},
    {"name":"orange", "count": 16},
];

let newArr = arr.filter((item) => {
  return item.name === 'orange';
});

console.log("Filter results:", newArr);
```

## Polyfill（兼容旧版浏览器）

```JavaScript
if (!Array.prototype.filter) {
  Array.prototype.filter = function(fun/*, thisArg*/) {
    'use strict';

    if (this === void 0 || this === null) {
      throw new TypeError();
    }

    var t = Object(this);
    var len = t.length >>> 0;
    if (typeof fun !== 'function') {
      throw new TypeError();
    }

    var res = [];
    var thisArg = arguments.length >= 2 ? arguments[1] : void 0;
    for (var i = 0; i < len; i++) {
      if (i in t) {
        var val = t[i];

        // NOTE: Technically this should Object.defineProperty at
        //       the next index, as push can be affected by
        //       properties on Object.prototype and Array.prototype.
        //       But that method's new, and collisions should be
        //       rare, so use the more-compatible alternative.
        if (fun.call(thisArg, val, i, t)) {
          res.push(val);
        }
      }
    }

    return res;
  };
}
```

# Array.prototype.map()

你可以把map当做一个 **for each** 循环来使用，它对数组中的每一个元素操作后，返回新的数组。
下面是我们经常会写的循环代码：

```JavaScript
let nums = [1, 2, 3, 4];
let newNums = [];

for(let i = 0; i < nums.length; i++) {
    newNums[i] = nums[i] * 2;
}

console.log(newNums); // [2, 4, 6, 8]
```

我们可以使用ES5中加入的forEach()方法进行改进：

```JavaScript
let nums = [1, 2, 3, 4];
let newNums = [];

nums.forEach((num, index) => {
  newNums[index] = num * 2;
});

console.log(newNums); // [2, 4, 6, 8]
```
注意ES5还不支持Arrow Function **()=>{}** 和 **let**

不过这样改进以后似乎也没有省多少代码
下面我们看一下比较函数式编程的map方法

```JavaScript
let nums = [1, 2, 3, 4];
let newNums = nums.map((num) => {
  return num * 2;
})

console.log(newNums); // [2, 4, 6, 8]
```
似不似瞬间代码少了很多呢，下面我们来看下map的源码。

## Polyfill（兼容旧版浏览器）

``` JavaScript
// Production steps of ECMA-262, Edition 5, 15.4.4.19
// Reference: http://es5.github.io/#x15.4.4.19
if (!Array.prototype.map) {

  Array.prototype.map = function(callback, thisArg) {

    var T, A, k;

    if (this == null) {
      throw new TypeError(' this is null or not defined');
    }

    // 1. Let O be the result of calling ToObject passing the |this| 
    //    value as the argument.
    var O = Object(this);

    // 2. Let lenValue be the result of calling the Get internal 
    //    method of O with the argument "length".
    // 3. Let len be ToUint32(lenValue).
    var len = O.length >>> 0;

    // 4. If IsCallable(callback) is false, throw a TypeError exception.
    // See: http://es5.github.com/#x9.11
    if (typeof callback !== 'function') {
      throw new TypeError(callback + ' is not a function');
    }

    // 5. If thisArg was supplied, let T be thisArg; else let T be undefined.
    if (arguments.length > 1) {
      T = thisArg;
    }

    // 6. Let A be a new array created as if by the expression new Array(len) 
    //    where Array is the standard built-in constructor with that name and 
    //    len is the value of len.
    A = new Array(len);

    // 7. Let k be 0
    k = 0;

    // 8. Repeat, while k < len
    while (k < len) {

      var kValue, mappedValue;

      // a. Let Pk be ToString(k).
      //   This is implicit for LHS operands of the in operator
      // b. Let kPresent be the result of calling the HasProperty internal 
      //    method of O with argument Pk.
      //   This step can be combined with c
      // c. If kPresent is true, then
      if (k in O) {

        // i. Let kValue be the result of calling the Get internal 
        //    method of O with argument Pk.
        kValue = O[k];

        // ii. Let mappedValue be the result of calling the Call internal 
        //     method of callback with T as the this value and argument 
        //     list containing kValue, k, and O.
        mappedValue = callback.call(T, kValue, k, O);

        // iii. Call the DefineOwnProperty internal method of A with arguments
        // Pk, Property Descriptor
        // { Value: mappedValue,
        //   Writable: true,
        //   Enumerable: true,
        //   Configurable: true },
        // and false.

        // In browsers that support Object.defineProperty, use the following:
        // Object.defineProperty(A, k, {
        //   value: mappedValue,
        //   writable: true,
        //   enumerable: true,
        //   configurable: true
        // });

        // For best browser support, use the following:
        A[k] = mappedValue;
      }
      // d. Increase k by 1.
      k++;
    }

    // 9. return A
    return A;
  };
}
```


# Array.prototype.reduce()

> arr.reduce(callback, initialValue)

reduce函数传入两个参数: 第一个是回调函数，第二个是初始化值（可选）。
回调函数里面可以传入四个参数： previousValue， currentValue， currentIndex， array

先看一个求数组最大值的简单例子：

```JavaScript
'use strict';
let maxCallback = (pre, cur) => Math.max(pre, cur);
let max = [2, 33, 12, 22].reduce(maxCallback);
console.log(max); //33
```
“max =” 右边的执行顺序是怎样的呢？
1. pre = 2, cur = 33, Math.max(pre, cur) = 33
2. pre = 33, cur = 12, Math.max(pre, cur) = 33
3. pre = 33, cur = 22, Math.max(pre, cur) = 33
最后 max = 33

如果initialValue不为null，则会将initialValue作为函数第一次计算的pre传入：

```JavaScript
'use strict';
let arr = [
  [0, 1],
  [2, 3],
  [4, 5]
];
let flattened = arr.reduce(function(a, b) {
  return a.concat(b);
}, [-1]);

console.log(flattened); // [ -1, 0, 1, 2, 3, 4, 5 ]
```

计算顺序为：
1. pre = [-1], cur = [0 ,1], return [-1].concat([0, 1]) = [-1, 0, 1]
2. pre = [-1, 0, 1], cur = [2, 3], return [-1, 0, 1, 2, 3]
3. pre = [-1, 0, 1, 2, 3], cur = [4, 5], return [ -1, 0, 1, 2, 3, 4, 5 ]

利用reduce函数可以简化代码，比如求和：

```JavaScript
arr.reduce((a, b) =>{
  return a + b;
});
```

求最大值：

```JavaScript
arr.reduce((pre, cur) => Math.max(pre, cur));
```

把数组转换为对象（数组去重）：

```JavaScript
arr.reduce((o, v) => {
    o[v] = 1;
    return o;
}, {});
```

## Polyfill

```JavaScript
// Production steps of ECMA-262, Edition 5, 15.4.4.21
// Reference: http://es5.github.io/#x15.4.4.21
if (!Array.prototype.reduce) {
  Array.prototype.reduce = function(callback /*, initialValue*/) {
    'use strict';
    if (this === null) {
      throw new TypeError('Array.prototype.reduce called on null or undefined');
    }
    if (typeof callback !== 'function') {
      throw new TypeError(callback + ' is not a function');
    }
    var t = Object(this), len = t.length >>> 0, k = 0, value;
    if (arguments.length == 2) {
      value = arguments[1];
    } else {
      while (k < len && !(k in t)) {
        k++; 
      }
      if (k >= len) {
        throw new TypeError('Reduce of empty array with no initial value');
      }
      value = t[k++];
    }
    for (; k < len; k++) {
      if (k in t) {
        value = callback(value, t[k], k, t);
      }
    }
    return value;
  };
}
```
