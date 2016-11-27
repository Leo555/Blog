title: 深入学习JavaScript——Object对象
date: 2016-11-25 15:52:44
tags:
- JavaScript
- 闭包
categories: JavaScript
---

# Object--JavaScript世界的起源

JavaScript的世界中“一切皆是对象”，而所有对象的起源就是 Object 对象。

--神說：「要有光」。就有了光。

<!-- more -->
## Object简介

ECMAScript中的对象其实是一组数据和功能的集合。我们通过执行 new 操作符 + 对象类型的名称来创建对象。而创建 Object 类型的实例并为其添加属性和方法就可以创建自定义对象。Object即是一个对象，也是自身的构造函数。


```javascript
let o = new Object;  //如果不给构造函数传递参数可以省略圆括号，但不推荐这么写
```

仅仅创建 Object 实例并没有什么用处，但关键是理解一个重要的思想，即在ECMAScript中，Object 类型是它所有实例的基础，换句话说，Object类型所具有的任何属性和方法同样存在于更具体的对象中。

## Object对象属性

Object 对象一共有三个属性： _proto_, constructor, prototype。

### Object.prototype

### Object.constructor

### Object.prototype

## Object对象方法


