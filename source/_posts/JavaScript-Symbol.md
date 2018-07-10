---
title: Symbol
date: 2018-07-09 21:31:49
categories: JavaScript
tags:
- Symbol    
---

[ES2018新特性学习](https://lz5z.com/ES2018%E6%96%B0%E7%89%B9%E6%80%A7%E5%AD%A6%E4%B9%A0/) 中又回顾到了 symbol 数据类型。Symbol 作为一种原始数据类型，除了其 `Symbol.iterator` 属性和 `Symbol.asyncIterator` 属性为数据提供 `for...of` 和 `for...await...of` 访问机制外，它还有什么功能呢？或者说，ES6 中增加 Symbol 数据类型主要面对什么场景呢？

## Symbol 简介

Symbol() 函数返回 symbol 类型的值，该类型具有静态属性和静态方法，并且不支持 `new Symbol()` 语法。每个从 Symbol() 函数中返回的 symbol 值都是唯一的。一个 symbol 值能作为对象属性的标识符，这是该数据类型最大的目的。

<!--more-->

### Symbol vs symbol

1. Symbol 是一个不支持 new 操作符的函数，用于创建 symbol 类型的值。
2. symbol 是一种基本数据类型。目前 JavaScript 支持的 7 种数据类型是：undefined、null、Boolean、String、Number、Object、symbol。

## Symbol 使用

我们可以直接使用 Symbol() 函数创建 symbol 类型，并且用一个字符串作为其描述，每次都会创建一个新的 symbol 类型。

```javascript
let a = Symbol()
typeof a // 'symbol'
Object.prototype.toString.call(a) // '[object Symbol]'
let a1 = Symbol('a')
let a2 = Symbol('a')
a1 == a2 // false
a1 === a2 // false
Symbol('foo') === Symbol('foo') // false
```

Symbol() 函数不能使用 new 操作符。因为 JavaScript 中 new 操作符用来创建对象，Symbol 生成的是一个原始类型的值，并不是对象。通过原始数据类型创建一个显式包装器对象的方式从 ECMAScript 6 开始不再被支持。 然而现有的原始包装器对象，如 `new Boolean()`、`new String()` 以及 `new Number()` 因为遗留原因仍可被创建。

```javascript
new Symbol() // TypeError: Symbol is not a constructor at new Symbol
```

Symbol 可以接收字符串或者对象作为参数，如果参数是对象的话，Symbol 会调用该对象的 toString() 方法，将其转换为字符串，再生成 symbol 值。

```javascript
let a = {
  toString () {
    return 'abc'
  }
}
let sa = Symbol(a)
sa // Symbol(abc)
```

Symbol 值不能与其它数据类型的值进行运算，但是 Symbol 值可以**显式转换**为字符串或者 Boolean，其它类型的转换都会报 TypeError 错误。

```javascript
let a = Symbol('World')
'Hello ' + a // TypeError: Cannot convert a Symbol value to a string
`Hello ${a}` // TypeError: Cannot convert a Symbol value to a string  
a.toString() // 'Symbol(World)'
String(a) // 'Symbol(World)'
Boolean(a) // true
!a // false
```

每一个 Symbol 函数生成的值都不相等，因此 Symbol 可以作为标识符，当做对象属性名，这样就可以保证不会出现相同的属性名。这可以有效避免属性被覆盖。

```javascript
let a = Symbol()
// 第一种写法
let obj = {}
obj[a] = 'Hello'
// 第二种写法
let obj = {
  [a]: 'Hello'
}
// 第三种写法
let a = {}
Object.defineProperty(a, mySymbol, {value: 'Hello'})

// 以上写法都得到同样结果
a[mySymbol] // 'Hello'
```
注意，Symbol 值作为对象属性名时，不能用点运算符，因为点运算符后面是字符串，而 symbol 值并不是字符串。

```javascript
let a = Symbol()
let obj = {}

obj.a = 'Hello!' // 此时 a 相当于一个字符串，并不是 a 值
obj[a] // undefined
obj['a'] // 'Hello!'
```

在对象内部使用 Symbol 的时候，必须放在方括号中。

```javascript
let a = Symbol()
let obj = {
  [a]: function(arg){...}  
}
obj[a](123)
```

## Symbol 属性

### Symbol.length

```javascript
Symbol.length // 0
```

### Symbol.iterator

返回对象默认迭代器方法，使用 `for...of` 进行迭代。

```javascript
const iterable = {
  [Symbol.iterator]() {
    return {
      i: 0,
      next() {
        if (this.i < 3) {
          return { value: this.i++, done: false }
        }
        return { value: undefined, done: true }
      }
    }
  }
}

for (var value of iterable) {
  console.log(value)
}
// 0
// 1
// 2
```

### Symbol.asyncIterator

返回对象默认的异步迭代器的方法，使用 `for await of` 进行迭代。

```javascript
const myAsyncIterator = {
  [Symbol.asyncIterator]: () => {
    const items = ['a', 'b', 'c', 'd']
    return {
      next: () => Promise.resolve({
        done: items.length === 0,
        value: items.shift()
      })
    }
  }
}
const foo = async function () {
  for await (const item of myAsyncIterator) {
    console.log(item)
  }
}
foo()
```

### [Symbol.match](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Symbol/match)

指定了匹配的是正则表达式而不是字符串。`String.prototype.match()` 方法会调用此函数。此函数还用于标识对象是否具有正则表达式的行为。比如： `String.prototype.startsWith()`，`String.prototype.endsWith()` 和 `String.prototype.includes()` 这些方法会检查其第一个参数是否是正则表达式，是正则表达式就抛出一个 TypeError。现在，如果 match symbol 设置为 false（或者一个 假值），就表示该对象不打算用作正则表达式对象。

```javascript
var re = /foo/
re[Symbol.match] = false
'/foo/'.startsWith(re) // true
'/baz/'.endsWith(re)   // false
// 下面代码会抛出一个 TypeError：
'/bar/'.startsWith(/bar/) // Throws TypeError, 因为 /bar/ 是一个正则表达式且 Symbol.match 没有修改。
```

[Symbol.replace](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Symbol/replace)，[Symbol.search](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Symbol/search)、[Symbol.split](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Symbol/split) 使用方法都与 [Symbol.match](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Symbol/match) 比较类似，这里就不赘述了。

### [Symbol.hasInstance](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Symbol/hasInstance)

用于判断某对象是否为某构造器的实例，因此你可以用它自定义 instanceof 操作符在某个类上的行为。

```javascript
class MyArray {
  static [Symbol.hasInstance](instance) {
    return Array.isArray(instance)
  }
}
console.log([] instanceof MyArray) // true
```

### [Symbol.isConcatSpreadable](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Symbol/isConcatSpreadable)

用于配置某对象作为 `Array.prototype.concat()` 方法的参数时是否展开其数组元素。

对于数组对象，默认情况下，用于 concat 时，会按数组元素展开然后进行连接（数组元素作为新数组的元素）。

```javascript
var arr1 = ['a', 'b', 'c']
var arr2 = numeric = [1, 2, 3]
var arr3 = arr1.concat(arr2)
console.log(arr3) // 结果: ['a', 'b', 'c', 1, 2, 3]
```

重置 `Symbol.isConcatSpreadable` 可以改变默认行为。

```javascript
var arr1 = ['a', 'b', 'c']
var arr2 = numeric = [1, 2, 3]
arr2[Symbol.isConcatSpreadable] = false 
var arr3 = arr1.concat(arr2)
console.log(arr3) // 结果: ['a', 'b', 'c', 1, 2, 3]
```

对于类似数组的对象，默认是不展开的，如果期望使用 concat 时，展开其元素用于连接，重置 `Symbol.isConcatSpreadable` 为 true。

```javascript
var arr1 = [1, 2, 3]

var obj = {
  [Symbol.isConcatSpreadable]: true, 
  length: 2, 
  0: 'hello', 
  1: 'world' 
}

arr1.concat(obj) // [1, 2, 3, 'hello', 'world']
```

### [Symbol.unscopables]()


### [Symbol.species]()

### [Symbol.toPrimitive]()

### [Symbol.toStringTag]()


## Symbol 方法

### Symbol.for(key)

使用给定的 key 搜索现有的 symbol，如果找到则返回该 symbol。否则将使用给定的 key 在全局 symbol 注册表中创建一个新的 symbol。

```javascript
Symbol.for('foo') // 创建一个 symbol 并放入 symbol 注册表中，键为 'foo'
Symbol.for('foo') // 从 symbol 注册表中读取键为'foo'的 symbol


Symbol.for('bar') === Symbol.for('bar') // true
Symbol('bar') === Symbol('bar') // false，Symbol() 函数每次都会返回新的一个 symbol

var sym = Symbol.for('mario')
sym.toString() // 'Symbol(mario)'，mario 既是该 symbol 在 symbol 注册表中的键名，又是该 symbol 自身的描述字符串
```

### Symbol.keyFor(sym)

用来获取 symbol 注册表中与某个 symbol 关联的键。

```javascript
// 创建一个 symbol 并放入 Symbol 注册表，key 为 'foo'
var globalSym = Symbol.for('foo') 
Symbol.keyFor(globalSym) // 'foo'

// 创建一个 symbol，但不放入 symbol 注册表中
var localSym = Symbol()
Symbol.keyFor(localSym) // undefined，所以是找不到 key 的

// Symbol 默认属性并不在 symbol 注册表中
Symbol.keyFor(Symbol.iterator) // undefined
```

## 参考资料

- [MDN-Symbol](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Symbol)
- [Symbol](http://es6.ruanyifeng.com/#docs/symbol)
- 