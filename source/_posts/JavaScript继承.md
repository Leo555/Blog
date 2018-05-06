---
title: 深入学习JavaScript——继承
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
    this.property = true;
}
SuperType.prototype.getSuperValue = function() {
    return this.property;
}
function SubType() {
    this.subProperty = false;
}
//继承了 SuperType
SubType.prototype = new SuperType();
SubType.prototype.getSubValue = function() {
    return this.subProperty;
}
let instance = new SubType();
console.log(instance.getSuperValue()); // true
```