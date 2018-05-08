---
title: 深入学习 JavaScript——Object 对象
date: 2016-11-25 15:52:44
tags:
- JavaScript
- Object
categories: JavaScript
---

# Object--JavaScript世界的起源

JavaScript的世界中「一切皆是对象」，而所有对象的起源就是 Object 对象。

神說：「要有光」。就有了光。

<!-- more -->
## Object简介

JavaScript中的对象其实是一组数据和功能的集合。我们通过执行 new 操作符 + **对象类型的名称**来创建对象。
创建 Object 类型的实例并为其添加属性和方法就可以创建自定义对象，Object既是一个对象，也是自身的构造函数。


```javascript
let o = new Object;  //如果不给构造函数传递参数可以省略圆括号，但不推荐这么写
```

仅仅创建 Object 实例并没有什么用处，但关键是理解一个重要的思想，即在JavaScript中，Object 类型是它所有实例的基础，换句话说，Object类型所具有的任何属性和方法同样存在于更具体的对象中。

## Object对象属性

Object 对象一共有三个属性： \__proto__, constructor, prototype。

### Object.\__proto__ 

1. 为对象设置原型

```javascript
function Rectangle() {
}

let rec = new Rectangle();
rec.__proto__ === Rectangle.prototype; // true
rec.__proto__ = Object.prototype;
rec.__proto__ === Rectangle.prototype; //false
```

2. \__proto__ 属性可用于设置对象的原型

```javascript
let proto = { y: 2 };

let obj = { x: 10 };
obj.__proto__ = proto;

proto.y = 20;
proto.z = 40;

obj.x === 10;  // true
obj.y === 20;  // true
obj.z === 40;  // true
```

3. 这只适用于可扩展的对象，一个不可扩展的对象的 \__proto__ 属性是不可变的

```javascript
let obj = {};
Object.preventExtensions(obj);

obj.__proto__ = {}; // 抛出异常TypeError
```

### Object.constructor

所有对象都会从它的原型上继承一个 constructor 属性， constructor 属性是保存当前对象的构造函数。

```javascript
let o = new Object; // 或者 o = {}
o.constructor === Object; // true
let a = new Array  // 或者 a = []
a.constructor === Array; // true
let n = new Number(3); // 或者 n = 3
n.constructor === Number; // true
```

### Object.prototype

Object.prototype 属性表示对象 Object 的原型对象，由于所有的对象都是基于 Object，所以 **所有的对象都继承了Object.prototype的属性和方法**，除非这些属性和方法被其他原型链更里层的改动所覆盖。

1. **Object.prototype.hasOwnProperty()**

返回一个布尔值 ，表示某个对象是否含有指定的属性，而且此属性非原型链继承的。

```javascript
let o = new Object();
o.name = 'object';
o.hasOwnProperty('name');             // true
o.hasOwnProperty('toString');         // false
o.hasOwnProperty('hasOwnProperty');   // false
```

2. **Object.prototype.isPrototypeOf()**

返回一个布尔值，表示指定的对象是否在本对象的原型链中。

```javascript
function Rectangle() {
}
let rec = new Rectangle();

Rectangle.prototype.isPrototypeOf(rec); // true
```

3. **Object.prototype.propertyIsEnumerable()**

判断指定属性是否可枚举。

```javascript 
object.propertyIsEnumerable(proName)
```

如果 proName 存在于 object 中，且可以使用 for 循环对其进行枚举，则 propertyIsEnumerable 方法返回 true。如果 object 不具有所指定名称的属性或者所指定的属性是不可枚举的，则 propertyIsEnumerable 方法将返回 false。

```javascript
let a = new Array("apple", "banana", "cactus");
a.propertyIsEnumerable(1); // true，0-2 都是true
a.propertyIsEnumerable(3); // false
```

4. **Object.prototype.toString()**

返回对象的字符串表示。

```javascript
let o = {};
o.toString() // "[object Object]"
```
上面代码调用空对象的 toString 方法，结果返回一个字符串 **"[object Object]"**，其中第二个Object表示该值的构造函数，
实例对象可能会自定义 toString 方法，覆盖掉 Object.prototype.toString 方法。通过函数的 call 方法，可以在任意值上调用 Object.prototype.toString 方法，帮助我们判断这个值的类型。

```javascript
Object.prototype.toString.call(0) // "[object Number]"
Object.prototype.toString.call('') // "[object String]"
Object.prototype.toString.call(true) // "[object Boolean]"
Object.prototype.toString.call(undefined) // "[object Undefined]"
Object.prototype.toString.call(null) // "[object Null]"
Object.prototype.toString.call(Math) // "[object Math]"
Object.prototype.toString.call({}) // "[object Object]"
Object.prototype.toString.call([]) // "[object Array]"
Object.prototype.toString.call(Symbol()) //"[object Symbol]"
Object.prototype.toString.call(/./) //"[object RegExp]"
```

5. **Object.prototype.valueOf()**

返回指定对象的原始值。valueOf() 方法的作用是返回一个对象的“值”，默认情况下返回对象本身。

valueOf方法的主要用途是，JavaScript自动类型转换时会默认调用这个方法。

```javascript
let o = new Object();
1 + o // "1[object Object]"  //默认调用valueOf()方法

//自定义valueOf() 方法

Object.prototype.valueOf = function() {
	return 2;
}

1 + new Object; // 3
```


## Object对象方法

|函数|描述|
|:-| :- |
|Object.assign(target, ...sources) |将来自一个或多个源对象中的值复制到一个目标对象。|
|Object.create(prototype, descriptors) |创建具有指定原型并可选择包含指定属性的对象。|
|Object.defineProperties(obj, props) |将一个或多个属性添加到对象，和/或修改现有属性的特性。|
|Object.defineProperty(obj, prop, descriptor) |将属性添加到对象，或修改现有属性的特性。|
|Object.freeze(obj) |防止修改现有属性的特性和值，并防止添加新属性。|
|Object.getOwnPropertyDescriptor(obj, prop) |返回数据属性或访问器属性的定义。|
|Object.getOwnPropertyNames(obj) |返回对象属性及方法的名称。|
|Object.getOwnPropertySymbols(obj) |返回对象的符号属性。|
|Object.getPrototypeOf(obj) |返回对象的原型。|
|Object.is(value1, value2) |返回一个值，该值指示两个值是否相同。|
|Object.isExtensible(obj) |返回指示是否可将新属性添加到对象的值。|
|Object.isFrozen(obj)|如果无法在对象中修改现有属性的特性和值，并且无法将新属性添加到对象，则返回 true。|
|Object.seal(obj) |防止修改现有属性的特性，并防止添加新属性。|
|Object.isSealed(obj) |如果无法在对象中修改现有属性特性，并且无法将新属性添加到对象，则返回 true。|
|Object.keys(obj) |返回对象的 **可枚举**属性和方法的名称。|
|Object.preventExtensions(obj) |防止向对象添加新属性。|
|Object.setPrototypeOf(obj, prototype) |设置对象的原型。|

---
### Object.assign(target, ...sources) 

Object.assign() 方法可以把任意多个的源对象自身的可枚举属性拷贝给目标对象，然后返回目标对象。

如果存在分配错误，此函数将引发 TypeError，这将终止复制操作。如果目标属性不可写，则将引发 TypeError。

```javascript
let first = { name: "Leo" };
let last = { lastName: "Li" };

let person = Object.assign(first, last);
console.log(person); //{ name: "Leo", lastName: "Li" } 

let clone = Object.assign({}, person); //使用 Object.assign 克隆对象。
```

### Object.create(prototype, descriptors)

创建一个具有指定原型且包含指定属性的对象。

```javascript
let newObj = Object.create(null, {
  size: {
    value: "large",
    enumerable: true
  },
  shape: {
    value: "round",
    enumerable: true
  }
});

console.log(newObj.size); // large
console.log(newObj.shape); // round
console.log(Object.getPrototypeOf(newObj)); //null
```

使用Object.create实现类式继承

```javascript
function Shape() {
  this.x = 0;
  this.y = 0;
}

Shape.prototype.move = function(x, y) {
    this.x += x;
    this.y += y;
    console.info("Shape moved.");
};

// Rectangle - subclass
function Rectangle() {
  Shape.call(this); //call super constructor.
}

Rectangle.prototype = Object.create(Shape.prototype);

let rect = new Rectangle();

rect instanceof Rectangle //true.
rect instanceof Shape //true.

rect.move(1, 1); //Outputs, "Shape moved."
```
### Object.keys(obj)

返回对象可枚举的属性名组成的数组。

```javascript
let a = ["Hello", "World"];

Object.keys(a)
// ["0", "1"]

Object.getOwnPropertyNames(a)
// ["0", "1", "length"]
```

### Object.getOwnPropertyNames(obj)

返回一个由指定对象的所有自身属性的属性名（包括不可枚举属性）组成的数组。

```javascript
let arr = ["a", "b", "c"];
Object.getOwnPropertyNames(arr).sort(); //[ '0', '1', '2', 'length' ]
```

### Object.getOwnPropertySymbols(obj)

该特性属于 ECMAScript 2015（ES6）规范。

Object.getOwnPropertySymbols() 方法会返回一个数组，该数组包含了指定对象自身的（非继承的）所有 symbol 属性键。

```javascript
let obj = {};
let a = Symbol("a");
let b = Symbol.for("b");

obj[a] = "a";
obj[b] = "b";

let objectSymbols = Object.getOwnPropertySymbols(obj);

objectSymbols.length; // 2
objectSymbols;        // [Symbol(a), Symbol(b)]
objectSymbols[0];     // Symbol(a)
```

### 对象限制型方法

ES5中提供了一系列限制对象被修改的方法，用来防止被某些对象被无意间修改导致的错误。每种限制类型包含一个判断方法和一个设置方法。

#### 阻止对象扩展

Object.preventExtensions() 用来限制对象的扩展，设置之后，对象将无法添加新属性。

1. 对象的属性不可用扩展，但是已存在的属性可以被删除。
2. 无法添加新属性指的是无法在自身上添加属性，如果是在对象的原型上，还是可以添加属性的。
3. Object.isExtensible() 方法用来判断一个对象是否可扩展。

#### 将对象密封

Object.seal() 可以密封一个对象并返回被密封的对象。
密封对象无法添加或删除已有属性，也无法修改属性的enumerable，writable，configurable，但是可以修改属性值。

通过 Object.isSealed() 判断一个对象是否密封。

#### 冻结对象

Object.freeze() 方法用来冻结一个对象，被冻结的对象将无法添加，修改，删除属性值，也无法修改属性的特性值，即这个对象无法被修改。被冻结的对象无法删除自身的属性，但是通过其原型对象还是可以新增属性的。

通过 Object.isFrozen() 可以用来判断一个对象是否被冻结了。


### 其它

Object.defineProperties、Object.defineProperty、Object.freeze、Object.getOwnPropertyDescriptor 的用法请参考[使用Object.defineProperty为对象定义属性](https://lz5z.com/Object.defineProperty%E4%B8%BA%E5%AF%B9%E8%B1%A1%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7/)。

## 总结

Object 对象虽然平时我们很少直接用到，但是很多对象的属性和方法都是由 Object 继承而来的，因此非常具有学习意义。
这篇 Blog 虽然都是 API 级别的学习，可是很多东西都是欠下的技术债，就当补课了。