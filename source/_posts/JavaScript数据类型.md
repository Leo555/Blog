---
title: JavaScript 数据类型
date: 2016-12-27 14:02:32
categories: JavaScript
tags:
- 数据类型
- typeof
---

JavaScript 语言可以识别 7 中不同的数据类型，除 Object 外，其它均为基本数据类型，Object 为引用数据类型。

- Undefined, 只有一个值，即特殊值 undefined，使用 var/let/const 声明但未初始化的值。
- Null，只有一个值，即特殊值 null，null 值表示一个空对象指针。
- Boolean，布尔型，true 和 false。
- Number, 整数和浮点数。
- String, 字符串，由零个或者多个 16 位 Unicode 字符串组成的字符序列。
- Symbol, ES6 新增类型，它的实例是唯一且不可改变的。
- Object, 一组数据和功能的集合。可以通过 new 加对象名称创建。

<!--more-->

### Undefined 类型

```javascript
var message // 变量声明之后默认取得了 undefined 值
message == undefined // true
message === undefined // true
```

### Null 类型

Null 类型只有一个值 null，null 表示一个空指针对象。

```javascript
typeof null // "objec"
```

如果定义变量准备在将来保存对象，最好讲该变量初始化为 null，这样可以通过检查 null 来判断是否已经保存了一个对象的引用。

实际上，undefined 值派生自 null

```javascript
null == undefined // true
null === undefined // false
```

null vs undefined

尽管 null 和 undefined 之间的相等操作符（==）返回 true，不过它们的用途完全不同，如前所述，无论什么情况下，没有必要把一个变量的值设为 undefined，而如果一个变量将来要保存对象，应该将其显式地设为 null。

### Boolean 类型

对于任何数据类型，调用 Boolean() 函数，总是会返回一个 Boolean 值。

```javascript
Boolean(0) // false
Boolean(NaN) // false
Boolean(null) // false
Boolean(undefined) // false
Boolean('/t') // false
```

### Number 类型

(1) 整数：

```javascript
var intNum = 55
var octalNum = 070 // 八进制的 56
var hexNum = 0xA // 十六进制的 10

+0 === -0 // true
```

(2) 浮点数：

```javascript
3e-17 // 0.000...03

0.1 + 0.2 // 0.30000000000000004 浮点数最高精度为 17 位小数
0.1 + 0.2 === 0.3 // false
```

ECMAScript 最小数：Number.MIN_VALUE，在大多数浏览器中为 5e-324。
ECMAScript 最大数：Number.MAX_VALUE，在大多数浏览器中为 1.7976931348623157e+308。

如果计算超过 JavaScript 数值范围，会自动转为特殊的 Infinity 值，负数则为 -Infinity。Infinity 不能参与数值计算。通过 isFinite() 函数判断参数是否位于最大值和最小值之间。

```javascript
1 / 0 // Infinity
isFinite(Number.MAX_VALUE + Number.MAX_VALUE) // false
```

(3) NaN （Not a Number）

NaN 用来表示本来要返回数值的操作数未返回数值的情况，避免抛出错误。

NaN 的设计有两个特点：

1.任何涉及 NaN 的操作都返回 NaN
2.NaN与任何值都不相等，包括 NaN 本身

```javascript
0/0 // NaN
NaN/10 // NaN
NaN == NaN // false
```

针对这两个特点，ECMAScript 设计了 isNaN() 函数。这个函数帮助我们判断参数是否 “不是数值”。isNaN() 接受参数后，会尝试将这个值转换为数值，如果这个值不能被转换为数值，则返回 true。

```javascript
isNaN(NaN) // true
isNaN(10) // false
isNaN('10') // false 可以转换为数值 10
isNaN('blue') // true 不能转换为数值
isNaN(true) // false 可以转换为数值 1
```

(4) 数值转换

Number() 函数转换规则如下：

1.如果是 Boolean 值，返回 1 或者 0。
2.数字直接返回。
3.null 返回 0。
4.undefined 返回 NaN。
5.字符串：如果是十进制整数，八进制整数或者十六进制整数返回十进制整数，空字符串返回 0，其它均返回 NaN。
6.如果是对象，调用对象的 valueOf() 方法，然后按照前面的转换规则转换，如果转换值为 NaN，则调用对象的 toString() 方法。

parseInt()

```javascript
parseInt('1234blue') // 1234
parseInt('') // NaN
parseInt('0xA') // 10
parseInt(22.5) // 22
parseInt(070) // 56
```

parseInt() 解析八进制字面量的字符串时，ES3 和 ES5 存在区别，在 ES3 中 '070' 被当做八进制字面量，ES5 则当做 '70'。
因此 parseInt 可以接收第二个参数，表示以多少进制解析第一个参数。

```javascript
parseInt('0xAF', 16) // 175
parseInt('070') // 70
parseInt('070', 8) // 56
```

### Symbol 类型

Symbol 是 ES6 新增的数据类型，用来解决对象中属性名重复的问题，Symbol 表示独一无二的值，通过 Symbol 函数生成。

```javascript
Symbol("foo") !== Symbol("foo") // true
const foo = Symbol()
const bar = Symbol()
typeof foo === "symbol" // true
typeof bar === "symbol" // true
let obj = {}
obj[foo] = "foo"
obj[bar] = "bar"
JSON.stringify(obj) // {}
Object.keys(obj) // []
Object.getOwnPropertyNames(obj) // []
Object.getOwnPropertySymbols(obj) // [ foo, bar ]
```

### Object 类型

Object 对象是一组数据和功能的集合。

```javascript
var o = new Object()
var o = new Object
```

关于 Object 对象的详细内容，可以参考 [深入学习JavaScript——Object对象](https://lz5z.com/JavaScript%E4%B8%AD%E7%9A%84Object%E5%AF%B9%E8%B1%A1/) 和 [使用 Object.defineProperty 为对象定义属性](https://lz5z.com/Object.defineProperty%E4%B8%BA%E5%AF%B9%E8%B1%A1%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7/)。

### 如何判断数据类型

(1) typeof 操作符

typeof 操作符返回值一共有7种：number，boolean，symbol，string，object，undefined，function。

```javascript
typeof '' // string 有效
typeof 1 // number 有效
typeof Symbol() // symbol 有效
typeof true //boolean 有效
typeof undefined //undefined 有效
typeof null //object 无效
typeof [] //object 无效
typeof new Function() // function 有效
typeof new Date() //object 无效
typeof new RegExp() //object 无效
```

- 对于基本类型，除 null 以外，均可以返回正确的结果。
- 对于引用类型，除 function 以外，一律返回 object 类型。
- 对于 null ，返回 object 类型。
- 对于 function 返回  function 类型。

(2) instanceof

instanceof 用来判断 A 是否为 B 的实例，需要注意的是，instanceof 检测的是原型。

可以理解为：

```javascript
instanceof (A, B) {
  var L = A.__proto__
  var R = B.prototype
  return L === R    
}
```

```javascript
[] instanceof Array // true
{} instanceof Object // true
new Date() instanceof Date // true

function A () {}
new A() instanceof A // true

[] instanceof Object // true
new Date() instanceof Object // true
new A() instanceof Object // true
```

[] 的 `__proto__` 指向了 Array.prototype，而 `Array.prototype.__proto__` 又指向了 Object.prototype，而 `Object.prototype.__proto__` 指向了 null，因此 []、Array、Object 在内部形成了一条原型链。instanceof 只能用来判断两个对象是否属于实例关系，而不能判断一个对象实例具体属于哪种类型。

(3) constructor

当一个函数 F 被定义的时候，JS 引擎会自动帮其添加 prototype，并在 prototype 上添加一个 constructor 属性，并让其指向 F 的引用。

<img src="/assets/img/js_constructor.png" alt="js_constructor">

当实例化 F 的时候，`var f = new F()`，F 原型上的 constructor 传递到了 f 上，因此 `f.constructor === F`。

F 利用原型对象上的 constructor 引用了自身，当 F 作为构造函数来创建对象时，原型上的 constructor 就被遗传到了新创建的对象上， 从原型链角度讲，构造函数 F 就是新对象的类型。这样做的意义是，让新对象在诞生以后，就具有可追溯的数据类型。

```javascript
''.constructor === String
(1).constructor === Number
new Number(1).constructor === Number
new Function().constructor === Function
new Date().constructor === Date
new Error().constructor === Error
[].constructor === Array
document.constructor === HTMLDocument
window.constructor === Window
```

利用 constructor 判断数据类型存在的问题：

1. null 和 undefined 是无效对象，因此没有 constructor 存在。
2. 函数的 constructor 可以被重写，因此可能会出现判断错误。

(4) toString

toString() 是 Object 的原型方式，调用该方法，默认返回当前对象的 `[[CLass]]`，其格式为 [object Xxx]，其中 Xxx 就是对象的类型。

```javascript
Object.prototype.toString.call('') // [object String]
Object.prototype.toString.call(1) // [object Number]
Object.prototype.toString.call(true) // [object Boolean]
Object.prototype.toString.call(Symbol()) //[object Symbol]
Object.prototype.toString.call(undefined) // [object Undefined]
Object.prototype.toString.call(null) // [object Null]
Object.prototype.toString.call(new Function()) // [object Function]
Object.prototype.toString.call(new Date()) // [object Date]
Object.prototype.toString.call([]) // [object Array]
Object.prototype.toString.call(new RegExp()) // [object RegExp]
Object.prototype.toString.call(new Error()) // [object Error]
Object.prototype.toString.call(document) // [object HTMLDocument]
Object.prototype.toString.call(window) // [object Window]
```

## 引用数据类型 vs 基本数据类型

基本数据类型复制相当于在内存中新开辟一块内存，引用数据类型的复制相当于在内存中创建了一个新的指针，指向存储在堆中的一个对象。

ECMAScript 中所有的函数都是 **按值传递参数** 的。也就是说，把函数外部的值复制给函数内部的参数，就和把值从一个变量复制到另外一个变量一样。
在向参数传递基本数据类型的值时，被传递的值会被复制给一个局部变量（即命名参数，也就是 arguments 对象中的一个元素）。在向参数传递引用类型的值时，会把这个值在内存中的地址复制给一个局部变量，因此这个局部变量的变化会反映在函数外部。

```javascript
function setName (obj) {
  obj.name = 'Leo'
}
var person = new Object()
setName(person)
console.log(person.name) // "Leo"
```


## 参考资料

- 《JavaScript高级程序设计》
- [判断JS数据类型的4种方法](https://www.cnblogs.com/onepixel/p/5126046.html)
- [语法和数据类型](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide/Grammar_and_types)