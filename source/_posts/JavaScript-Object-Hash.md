---
title: JavaScript对象与Hash表
date: 2016-12-01 10:02:04
categories: JavaScript
tags:
- JavaScript
- Hash
---

# 简介

哈希表(Hash table，也叫散列表)，是根据关键码值(Key value)而直接进行访问的数据结构。也就是说，它通过把关键码值映射到表中一个位置来访问记录，以加快查找的速度。这个映射函数叫做散列函数，存放记录的数组叫做散列表。

JavaScript 中的对象也是以 Key-Value 的形式访问，那么 JavaScript 的对象是否以 Hash 的结构存储呢？

我们首先来看一下 Hash 表结构。
<!-- more -->

## Hash 表结构

数组的特点是：寻址容易，插入和删除困难；而链表的特点是：寻址困难，插入和删除容易，Hash 表综合两者的特性，做出一种寻址容易，插入删除也容易的数据结构。

下图是最常见的 **拉链法** 做出的 Hash 表

<img src="/assets/img/hash.jpg" alt="hash">

左边是一个数组，数组的每个成员包括一个指针，指向一个链表的头，当然这个链表可能为空，也可能元素很多。我们根据元素的一些特征把元素分配到不同的链表中去，也是根据这些特征，找到正确的链表，再从链表中找出这个元素。

元素特征转变为数组下标的方法就是散列法。上图运用的方法为 **整除法**，公式为：

> index = value % 16

hash表的工作原理：

1. 第一步 先根据给定的key和散列算法得到具体的散列值，也就是对应的数组下标。
2. 第二步，根据数组下标得到此下标里存储的指针，若指针为空，则不存在这样的键值对，否则根据此指针得到此链式数组。
3. 遍历此链式数组，分别取出Key与给定的Key比较，若找到与给定key相等的Key，即在此hash表中存在此要查找的<Key,Value>键值对，此后便可以对此键值对进行相关操作；若找不到，即为不存在此键值对。

# JavaScript 对象存储形式

## JavaScript 对象 Key 存储形式

在我们创建或者访问对象属性的时候，如果使用 **对象.属性名** 的方式，属性名只能为字符串类型，而且不能以数字开头：

```javascript
let obj = {};
obj.2 = 2;  //Uncaught SyntaxError: Unexpected number
obj.12s = '12s';  //Uncaught SyntaxError: Invalid or unexpected token
```
而使用字面量的形式创建对象，或者用 **对象[属性名]** 的方法，却没有这样的限制:

```javascript
let o = {};
let obj = {
    x: 1,
    2: 2,
    o: 'object',
    {name: 'Leo'}: 'object'
};
obj['12s'] = '12s';
obj[{name: 'Leo'}] = 'object'; //使用 对象[属性名] 的方式甚至可以把对象当做属性名传入
```
此时 obj 里面的属性 **2** 是一个整数吗？

```javascript
for (let i in obj) {
    console.log(typeof i, i, obj[i]);
}
// string 2 2
// string x 1
// string o object
// string 12s 12s
// string [object Object] object
```
由此可见 JavaScript 中对象的 Key 均是 string 类型。

```javascript
console.log(obj[2] === obj['2']);  // true
object[2]=3;
console.log(object['2']);//3
```
可见解释器在访问 object[2] 的时候，先将方括号里面的 2 转换成字符串，然后再访问。

而使用 obj[{name: 'Leo'}] = 'object' 的时候，也是同样的，解释器先调用 Objcet.toString 方法把对象 {name: 'Leo'} 转换成字符串，然后再访问。

```javascript
let object = {
  x: 1,
  2: 2
}
Object.prototype.toString = function () {
  return '2';
}
console.log(object[{name: 'Leo'}]);　　// 2
```
上述的 **object[{name: 'Leo'}]** 相当于 **object[{name: 'Leo'}.toString()]** 亦相当于 **object['2']**，于是就得到结果 2。

这里也间接证明了 JavaScript 对象中，所有的 key 都是字符串，即使你访问的时候不是字符串的形式，解释器也会先将其转化为字符串。

可是我们知道整数值直接调用 toString 方法是会报错的，因为 JavaScript 解析器会试图将点操作符解析为浮点数字面值的一部分。不过有很多变通方法可以让数字的字面值看起来像对象。

```javascript
2.toString() // Uncaught SyntaxError: Invalid or unexpected token
//解决方案
2..toString(); // 第二个点号可以正常解析
2 .toString(); // 注意点号前面的空格
(2).toString(); // 2先被计算
```
所以 JavaScript 解释器应该有帮我们做这一部分工作。

## JavaScript 对象 Value 存储形式

在JavaScript高级程序设计（第三版）中，是这么描述属性的：属性在创建时都带有一些特征值，JavaScript引擎通过这些特征值来定义他们的行为。

```javascript
var person = {};
person.name = 'Leo';
var descriptor=Object.getOwnPropertyDescriptor(person,"name");
console.log(descriptor); 
//Object
	// configurable: true
	// enumerable: true
	// value: "Leo"
	// writable: true
	// __proto__: Object
```
可见 value 的数据类型是结构体。

## JavaScript 对象存储形式

在 JavaScript 中，我们可以任意给对象添加或者删除属性，由此可以推断，对象不是由数组结构存储；链表虽然能够任意伸缩但是其查询效率低下，因此也排除链表。如果用树作为存储结构，效率较高的可能就是平衡树了。平衡树的查询效率还可以接受，但是当删除属性的时候，平衡树在调整的时候代价相比于 hash 表要大很多。于是 Hash 成为最好的选择。

假如有这么一段代码：

```javascript
function Person(id, name, age) {
	this.id = id;
	this.name = name;
	this.age = age;
}
let num = 10;
let bol = true;
let obj = new Object;
let arr = ['a', 'b', 'c'];
let person = new Person(100, 'Leo', 18);
```

JavaScript 内存分析图	如下：
<img src="/assets/img/js_obj_mem.png" alt="memory">

变量 num、bol、str 为基本数据类型，它们的值直接存放在栈中。obj、person、arr 为复合数据类型，他们的引用变量存储在栈中，指向于存储在堆中的实际对象。

在 JavaScript 中变量分为基本类型和引用类型（对象类型），分别对应着两种不同的存储方式–栈存储和堆存储。

基本类型一旦初始化则内存大小固定，访问变量就是访问变量的内存上实际的数据，称之为按值访问。而对象类型内存大小不固定，无法在栈中维护，所以 JavaScript 就把对象类型的变量放到堆中，让解释器为其按需分配内存，而通过对象的引用指针对其进行访问，因为对象在堆中的内存地址大小是固定的，因此可以将内存地址保存在栈内存的引用中。这种方式称之为按引用访问。

# 总结

在 JavaScript 中对象是以 Hash 结构存储的，用 <Key, Value> 键值对表示对象的属性，Key 的数据类型为字符串，Value 的数据类型是结构体，即对象是以 <String, Object> 类型的 HashMap 结构存储的。
