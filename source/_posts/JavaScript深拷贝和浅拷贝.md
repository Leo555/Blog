---
title: JavaScript 深拷贝和浅拷贝
date: 2018-03-10 22:02:49
categories: JavaScript
tags:
- clone
- 深拷贝
- 浅拷贝
- lodash
---

在 JavaScript 引用数据类型中，变量保存的是一个指向堆内存的指针，当需要访问引用类型（如对象，数组等）的值时，首先从栈中获得该对象的地址指针，然后再从堆内存中取得所需的数据。

```javascript
let obj1 = { x: 1, y: 2 }
let obj2 = obj1
obj2.x = 2
console.log(obj1) // { x: 2, y: 2 }
console.log(obj2) // { x: 2, y: 2 }
```

以上的拷贝方式就是浅拷贝，当 obj2 的值改变时，obj1 的值也随之发生改变。

<!--more-->

### 浅拷贝

```javascript
let arr1 = [0, 1, ['a', 'b']]
let arr2 = arr1.concat()
let arr3 = arr1.slice()
let arr4 = Array.from(arr3)

arr2 === arr1 // false 看起来像深拷贝
arr3 === arr1 // false 看起来像深拷贝
arr4 === arr3 // false 看起来像深拷贝

// 然鹅

let arr5 = [{name: 'Leo'}]
let arr6 = arr4.slice()
let arr7 = arr4.concat()
let arr8 = Array.from(arr4)

arr5[0].name = 'Jack'
arr6[0].name === 'Jack' // 其实还是浅拷贝
arr7[0].name === 'Jack' // 其实还是浅拷贝
arr8[0].name === 'Jack' // 其实还是浅拷贝
```

Array.prototype.concat(), Array.prototype.slice(), Array.from() 只能实现对一维数组的深拷贝。

### Object.assign()

```javascript
let obj1 = { x: 1, y: 2 }
let obj2 = Object.assign({}, obj1)
obj1 === obj2 // false
obj1.x = 2
console.log(obj1) // { x: 2, y: 2 }
console.log(obj2) // { x: 1, y: 2 } // 一维对象可以进行深拷贝
// 然鹅
let obj3 = { x: {name: 'Leo'} }
let obj4 = Object.assign({}, obj3)
obj3 === obj4 // false
obj3.x.name = 'Jack'
obj4.x.name === 'Jack' // true // 其实还是浅拷贝
```


### 深拷贝

使用 JSON.parse() + JSON.stringify() 实现深拷贝

```javascript
let obj1 = {
  x: 1,
  y: {
    name: 'Leo',
    friends: ['Lily', 'Elsa']
  }    
}

let obj2 = JSON.parse(JSON.stringify(obj1))

obj1 === obj2 // false
obj1.y.name = 'Jack'
obj1.y.friends.push('Tim')
obj2.y.name === 'Leo' // 深拷贝
console.log(obj2.y.friends) // ["Lily", "Elsa"] // 深拷贝
```

JSON.parse 和 JSON.stringify 看起来不错，不过存在一些[问题](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify)：

1. undefined、任意的函数以及 symbol 值，在序列化过程中会被忽略（出现在非数组对象的属性值中时）或者被转换成 null（出现在数组中时）。
2. 所有以 symbol 为属性键的属性都会被完全忽略掉。
3. 不可枚举的属性会被忽略。

```javascript
JSON.stringify({a: function add (){}}) // '{}'

JSON.stringify({x: undefined, y: Object, z: Symbol("")}) // '{}'

JSON.stringify([undefined, Object, Symbol("")]) // '[null,null,null]' 

JSON.stringify({[Symbol("foo")]: "foo"}) // '{}'

```

### 使用递归

```javascript
function deepClone(o) {
  // if o is not an object 
  if (!o || (typeof o) != 'object') return o
  let res = Array.isArray(o) ? [] : {}
  let keys = Object.keys(o) 
  for (let i = 0; i< keys.length; i++) {
    let key = keys[i]
    if (typeof key === 'object') {
        res[key] = deepClone(o[key])
    } else {
        res[key] = o[key]
    }
  }
  return res
}
```

测试代码：

```javascript
let obj1 = {
  x: {name: 'Leo'},
  y: undefined,
  z: function add () {},
  t: Symbol('tt'),
  m: [1, 2, 3, 4, 5],
  n: [[1, 2]]
}

let obj2 = deepClone(obj1)
obj1.n[0].push(3)

console.log(obj2.n[0]) // [1, 2]
```
注意：由于使用 `for in` 循环，所以只能深度拷贝对象自身属性（非原型链上的属性），并且属性为 enumerable。

使用递归拷贝对象的方法，在目标非常大，层级关系非常深的时候会出现性能问题，具体解决方案可以参考我之前写的 [JavaScript递归优化](https://lz5z.com/JavaScript%E9%80%92%E5%BD%92%E4%BC%98%E5%8C%96/) 使用栈代替递归的方式解决。

### lodash

lodash 中提供 4 个对象[拷贝](https://lodash.com/docs/4.17.10#clone)相关的方法： 

```javascript
_.clone() // 提供浅拷贝
_.cloneDeep() // 提供深拷贝
_.cloneDeepWith() // 提供递归拷贝，并且可以自定义拷贝内容
_.cloneWith() // 提供浅拷贝，并且可以自定义拷贝内容
```

demo

```javascript
function customizer(value) {
  if (_.isElement(value)) {
    return value.cloneNode(true)
  }
}
 
let el = _.cloneDeepWith(document.body, customizer)
 
console.log(el === document.body) // => false
console.log(el.nodeName) // => 'BODY'
console.log(el.childNodes.length) // => 20
```

相信上述几种方法已经能够满足我们平时大部分的需求了，如果有额外的需求，只能自己定义实现深/浅拷贝的方式了。