---
title: 深入学习JavaScript——理解原型
date: 2016-12-02 13:21:53
categories: JavaScript
tags:
- JavaScript
- prototype
- 原型  
---

## 理解原型对象

在 JavaScript 中，只要创建了新函数，都会根据一组特定的规则为该函数创建一个 prototype 属性，这个属性指向函数的原型对象。默认情况下，所有原型对象都会自动获取一个 constructor（构造函数）属性，这个属性包含一个指向 prototype 属性所在函数的指针。比如：

```javascript
function Person () {}
Person.prototype.constructor === Person
```

通过 constructor，我们可以继续为原型对象添加其他属性和方法。

创建自定义的构造函数之后，其原型对象默认只会取得 constructor 属性，其它属性和方法都是从 Object 继承而来的。

当调用构造函数创建一个新实例后，该实例的内部将包含一个指针（[[Prototype]]），指向构造函数的原型对象，该指针在常用的浏览器中被定义为 `__proto__`。需要说明的一点是，该连接存在于实例和构造函数的原型对象之间，而不是存在于原型和构造函数之间。

```javascript
let leo = new Person()
leo.__proto__ === Person.prototype
```

<!--more-->

### 关系

构造函数，实例，prototype，`__proto__` 之间的关系可以理解为下图：

<img src="/assets/img/js_prototype.png" alt="js_prototype">

注意：`__proto__` 并非 JS 标准属性，而是浏览器的实现。

从图中可以看出构造函数 Person 和实例 leo 之间并没有直接关系，而是通过 Person.prototype 原型对象进行关联。虽然实例中并不包含属性和方法，但是可以通过调用 `leo.sayName` 进行调用。在非浏览器环境或者浏览器不支持 `__proto__` 的环境中，我们可以通过 isPrototypeOf() 方法来确定对象之间是否存在这种关系。

```javascript
Person.prototype.isPrototypeOf(leo) // true
leo.__proto__ === Person.prototype // 一些浏览器可能不支持
```

ECMAScript5 中增加了 Object.getPrototypeOf() 方法，该方法返回 [[Prototype]] 的值。

```javascript
Object.getPrototypeOf(leo) === Person.prototype
```

每当代码读取某个对象的属性时，都会执行一次搜索：首先判断实例是否具有给定名字的属性，如果没有的话，继续搜索实例的原型对象。

原型对象中的属性对于实例来说是只读的，比如：

```javascript
function Person () {}
Person.prototype.name = 'JavaScript'
let p1 = new Person()
let p2 = new Person()
p1.name = 'CSS'
console.log(p1.name) // CSS
console.log(p2.name) // JavaScript
delete p1.name
console.log(p1.name) // JavaScript
```

### hasOwnProperty() 与 in 操作符

hasOwnProperty 可以检测一个属性是存在于实例中，还是存在于原型对象中，这个方法继承自 Object 对象；无论属性存在于实例中还是原型中，使用 in 操作符都能得到 true。

```javascript
function Person () {}
Person.prototype.name = 'JavaScript'
let p1 = new Person()
p1.hasOwnProperty('name') // false
console.log('name' in p1) // true
p1.name = 'nobody'
p1.hasOwnProperty('name') // true
console.log('name' in p1) // true
```

注：ES5 中 Object.getOwnpropertyDescriptor() 方法只能用于实例属性，要取得原型属性的描述符，必须直接在原型对象上调用 Object.getOwnpropertyDescriptor()。

```javascript
Object.getOwnPropertyDescriptor(p1, 'name')
// {
//  configurable: true
//  enumerable: true
//  value: "nobody"
//  writable:true
//}
```

要取得对象上所有的可枚举的实例属性，可以使用 Object.keys() 方法。

```javascript
function Person () {}
Person.prototype.name = 'JavaScript'
Person.prototype.age = 18
Person.prototype.sayName = function () {}

Object.keys(Person.prototype) // ["name", "age", "sayName"]
let p1 = new Person()
Object.keys(p1) // []
p1.name = 'JavaScript'
Object.keys(p1) // ["name"]
```

可以看出，Object.keys() 方法只枚举实例属性，并不枚举原型对象中的属性，而且 constructor 属性也是不可枚举的。

### 更简单的原型语法

```javascript
function Person () {}
Person.prototype = {
  constructor: Person,
  name: 'JavaScript',
  age: 18,
  sayName: function () {
    console.log(this.name)
  }    
}
```

这种写法存在一个问题，就是重设的 constructor 属性的 [[Enumerable]] 特性被设置为 true，默认情况下，原生的 constructor 属性是不可枚举的。所以可以写成如下情况：

```javascript
function Person () {}
Person.prototype = {
  name: 'JavaScript',
  age: 18,
  sayName: function () {
    console.log(this.name)
  }    
}
Object.definedProperty(Person.prototype, 'constructor', {
  enumerable: false,
  value: Person
})
```

### 原型的动态性

在修改原型的过程中，我们可以随时为原型添加属性和方法，但是如果重写整个原型对象，那有可能切断构造函数与原型之间的联系。

```javascript
function Person () {}
let p1 = new Person()
Person.prototype = {
  constructor: Person,
  name: 'JavaScript',
  age: 18,
  sayName: function () {
    console.log(this.name)
  }        
}
p1.sayName() // p1.sayName is not a function
```

为什么在调用 p1.sayName() 的时候会发生错误呢，因为 p1 指向的原型对象中并不包含 sayName 方法。

其关系可看下图：

<img src="/assets/img/js_prototype_new.png" alt="js_prototype_new">

重写原型对象后，切断了现有原型与任何之前已经存在的对象实例之间的联系，它们引用的任然是最初的原型。

### 原型对象的缺点

原型对象省略了为构造函数传递参数这一环节，使得所有实例在默认情况下都取得相同的属性值，而且原型中所有的属性是被全部实例共享的，这种共享对于函数来说非常合适，但是对于属性值，尤其是引用类型的属性值来说，问题就比较严重了。

```javascript
function Person () {}
Person.prototype = {
  constructor: Person,
  name: 'JavaScript',
  age: 18,
  friends: ['Lily', 'Tony'],
  sayName: function () {
    console.log(this.name)
  }        
}

let p1 = new Person()
let p2 = new Person()
p1.friends.push('Jack')
console.log(p2.friends) // ["Lily", "Tony", "Jack"]
p1.friends === p2.friends // true
```

修改实例 p1 的值的过程中，p2 的值也被修改了。这就导致了仅仅使用原型模式创建对象存在很大的问题。具体解决请查看[深入学习JavaScript——面向对象](https://lz5z.com/JavaScript%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1/)。


