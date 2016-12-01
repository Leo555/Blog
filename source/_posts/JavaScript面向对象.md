---
title: 深入学习JavaScript——面向对象
date: 2016-12-01 18:14:29
categories: JavaScript
tags:
- JavaScript
- 面向对象
- Object-Oriented
---

# JavaScript 面向对象

几乎所有面向对象的语言都有一个标志，那就是类，通过类创建具有相同属性和方法的对象。而 ECMAScript 中没有类的概念，它把对象定义为：“无序属性的集合，其属性可以包含基本值、对象或者函数”。即对象是一组没有特定顺序的值，对象的每个属性或方法都有一个名字，而这个名字都映射到一个值。因此对象的本质是一个[散列表](http://www.lz5z.com/JavaScript-Object-Hash/)。

<!-- more -->
# 创建对象

虽然 Object 构造函数或对象字面量都可以创建单个对象，但是这些方式有个明显的缺点：使用同一个接口创建很多对象，会产生大量重复的代码。为了解决这个问题，就可以使用工厂模式来创建对象。

## 工厂模式

工厂模式用函数来封装特定接口创建对象。

```javascript
function createPerson(name, age, job) {
    let o = new Object();
    o.name = name;
    o.age = age;
    o.job = job;
    o.sayName = function () {
        console.log(this.name);
    };
    return o;
}
let leo = createPerson('Leo', 18, "Engineer");
```
工厂模式虽然解决了创建多个相似对象的问题，但没有解决对象识别的问题（即怎样知道一个对象的类型）。

## 构造函数模式

ECMAScript 中的构造函数可以用来创建特定类型的对象，像 Object 和 Array 的原生的构造函数，在运行时会自动出现在执行环境中。此外，也可以创建自定义的构造函数，从而定义自定义对象类型的属性和方法。代码如下所示：

```javascript
function Person(name, age, job) {
    this.name = name;
    this.age = age;
    this.job = job;
    this.sayName = function() {
        console.log(this.name);
    };
}
let leo = new Person('Leo', 18, "Engineer");
let jack = new Person('Jack', 18, "Engineer");
```
构造函数模式与工厂模式有以下不同：

1. 没有显式的创建对象； 
2. 直接将属性和方法赋给了this对象； 
3. 没有return语句； 

生成的对象 leo 中有一个 constructor 属性，该属性指向 Person，并且可以用 instanceof 做类型检测。

```javascript
leo.constructor === Person // true
leo instanceof  Object; // true
leo instanceof Person; // true
```

构造函数的缺点在于每个方法都要在每个实例上重新创建一遍。在前面例子中，leo 和 jack 都有一个名为 sayName 的方法，但是这两个方法不属于同一个对象。

那么我们能不能共享一个 sayName() 方法。如果想要完成这种需求，大可像下面代码一样，通过把函数定义转移到构造函数的外部。

```javascript
function Person(name, age, job) {
    this.name = name;
    this.age = age;
    this.job = job;
    this.sayName = sayName;
}

function sayName() {
    console.log(this.name);
};
let leo = new Person('Leo', 18, "Engineer");
let jack = new Person('Jack', 18, "Engineer");

console.log(leo.sayName === jack.sayName) // true
```

上面例子中的做法，确实解决了两个函数做同一件事的问题，但是无意中定义了很多全局函数，而这些全局函数中由于包含 “this” 关键字，又只能被某个函数调用。不仅污染了全局作用域，还使得这个自定义的引用类型完全丧失封装性。好在这些问题都可以通过原型模式解决。

## 原型模式




## 组合使用构造函数模式和原型模式

## 动态原型模式

## 寄生构造函数模式

## 稳妥构造函数模式

