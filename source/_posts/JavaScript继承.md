---
title: 深入学习 JavaScript——继承
date: 2016-12-05 23:50:08
categories: JavaScript
tags:
- JavaScript
- 面向对象
- Object-Oriented
- 继承
---

# 继承

继承是面向对象语言中最重要的概念之一，许多 OO 语言都支持两种继承方式：接口继承和实现继承。接口继承只继承方法签名，而实现继承则继承实际的方法。由于 ECMAScript 中没有方法签名，所以不能实现接口继承，而是通过原型链的方式完成实现继承。

## 原型链

每个构造函数都有一个原型对象，原型对象包含一个指向构造函数的指针，而所有实例中都包含一个指向原型对象的内部指针。下面是一个实现原型链的基本方法：

```javascript
function SuperType() {
  this.property = true
}
SuperType.prototype.getSuperValue = function() {
  return this.property
}
function SubType() {
  this.subProperty = false
}
// 继承了 SuperType
SubType.prototype = new SuperType()
SubType.prototype.getSubValue = function() {
  return this.subProperty
}
let instance = new SubType()
console.log(instance.getSuperValue()) // true
```

上述代码定义了 SuperType 和 SubType 两种类型，每个类型分别有一个属性和一个方法，SubType 通过改写原型对象的方式实现对 SuperType 的继承。原来存在于 SuperType 中的属性和方法，现在也存在于 SubType.prototype 中。在确立了继承关系后，我们给 SubType.prototype 又添加了一个新方法，这个例子中的关系图如下：

<img src="/assets/img/js_inherit.png" alt="js_inherit">

在上述代码中，我们修改 SubType 默认的原型为 SuperType 的实例，新原型不仅具有作为一个 SuperType 的实例所拥有的全部属性和方法，而且其内部还有一个指针，指向了 SuperType 的原型。最终的结果是这样的：instance 指向了 SubType 的原型，SubType 的原型又指向了 SuperType 的原型。

```javascript
instance.__proto__ === SubType.prototype // true
SubType.prototype.__proto__ === SuperType.prototype //true
instance.__proto__.__proto__ === SuperType.prototype //true
```

