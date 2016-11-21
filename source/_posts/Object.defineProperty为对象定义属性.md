title: 使用Object.defineProperty为对象定义属性
date: 2016-11-21 22:38:27
tags: 
- defineProperty
- JavaScript
- Object
categories: JavaScript
---

# 先说句题外话

目前前端开发中比较流行的两个框架： [Angular](https://angularjs.org/) 和 [Vue](https://cn.vuejs.org/) 都采用了数据双向绑定的技术。
Angular1 中数据双向绑定是通过「脏检测」的方式实现，每当数据发生变更，对所有的数据和视图的绑定关系进行一次检测，识别是否有数据发生了变化以及这个变化是否会影响其它数据的变化，然后将变更的数据发送到视图，更新页面展示。

Vue 数据双向绑定的原理与Angular有所不同，网上人称「数据劫持」<img src="/assets/img/scary.gif" alt="scary" width="5%">。Vue使用的是 ES5 提供的 Object.defineProperty() 结合发布者-订阅者模式，通过Object.defineProperty() 来劫持各个属性的setter，getter，在数据变动时发布消息给订阅者，触发相应的监听回调。

<!-- more -->
# Object.defineProperty 

## 定义以及使用
Object.defineProperty() 方法会直接在一个对象上定义一个新属性，或者修改一个已经存在的属性， 并返回这个对象。

我们来看下一般使用方法：

```javascript
'use strict';
let Leo = Object.defineProperty({}, 'name', {
    value: 'Leo'
});

console.log(Leo.name); //Leo
```

其基本语法规则如下：

```javascript
Object.defineProperty(obj, prop, descriptor)
```

1. obj: 需要定义属性的对象。
2. prop: 需定义或修改的属性的名字。
3. descriptor: 将被定义或修改的属性的描述符。
4. 返回值: 返回传入函数的对象，即第一个参数obj

所以 **Object.defineProperty(obj, 'name', { value: 'Leo'})** 相当于 **obj.name = 'Leo'** 或者 **obj['name'] = 'Leo'**喽。

那我们之间使用「对象.属性」就好了，为什么要用 Object.defineProperty 这么复杂的方法呢？

## Object.defineProperty 解决什么问题

如果你想定义一个对象的属性为只读怎么办？
「对象.属性」能做到吗？显然不能！Object.defineProperty 却可以做到。因此 **Object.defineProperty 方法是对属性更加精确的定义**。

### 属性的状态设置

我们可以在descriptor参数中设置如下值，来实现对属性的控制：
 - value：默认为 undefined。该属性的值。
 - writable：默认为 false。该属性是否可写，如果设置成 false，则任何对该属性改写的操作都无效（[严格模式](http://www.lz5z.com/JavaScript%E4%B8%A5%E6%A0%BC%E6%A8%A1%E5%BC%8F/)会报错，正常模式则什么都不做）
 - configurable：默认为 false。当且仅当该属性的 configurable 为 true 时，该属性描述符才能够被改变，也能够被删除。
 - enumerable：默认为 false。当且仅当该属性的 enumerable 为 true 时，该属性才能够出现在对象的枚举属性中（for...in 或者 Object.keys）
 - get: 默认为 undefined。一个给属性提供 getter 的方法。该方法返回值被用作属性值。
 - set: 默认为 undefined。一个给属性提供 setter 的方法。该方法将接受唯一参数，并将该参数的新值分配给该属性。

### value、writable
```javascript
'use strict';
let Leo = Object.defineProperty({}, 'name', {
    writable: true, //writable 为true的时候name属性才可以被更改
    value: 'Leo'
});

Leo.name = 'Jack'; //strict mode下修改writable为false的属性会报错
console.log(Leo.name);
```

### configurable

```javascript
'use strict';
let Leo = Object.defineProperty({}, 'name', {
    configurable: true,
    value: 'Leo'
});

delete Leo.name; //configurable为false的时候删除属性会报错
```

configurable 参数不仅负责属性的删除，也与属性修改有关。

```javascript
'use strict';
let Leo = Object.defineProperty({}, 'name', {
    configurable: false,
    value: 'Leo'
});

Object.defineProperty(Leo, 'name', {
    configurable: true, // Cannot redefine property: name
    value: 'Jack', //Cannot redefine property: name
    writable: true, //Cannot redefine property: name
    enumerable: true //Cannot redefine property: name
});
```

假如一个属性被定义成 configurable 为 false，则这个属性既不能修改值（value），又不能修改属性的属性（configurable，writable，enumerable）；如果 configurable 为 true 就可以放心修改了。

```javascript
'use strict';
let Leo = Object.defineProperty({}, 'name', {
    configurable: true,
    value: 'Leo'
});

Object.defineProperty(Leo, 'name', {
    configurable: true,
    value: 'Jack',
    writable: true,
    enumerable: true
});
```

### enumerable

属性特性 enumerable 定义了对象的属性是否可以在 for...in 循环和 Object.keys() 中被枚举。

```javascript
'use strict';
let o = Object.defineProperty({}, "a", {value: 1, enumerable: true});
Object.defineProperty(o, "b", {value: 2, enumerable: false});
Object.defineProperty(o, "c", {value: 3}); // enumerable defaults to false
o.d = 4; // 如果使用直接赋值的方式创建对象的属性，则这个属性的enumerable为true

for (let i in o) {    
  console.log(i); // "a" "d" 
}

Object.keys(o); // ["a", "d"]

o.propertyIsEnumerable('a'); // true
o.propertyIsEnumerable('b'); // false
o.propertyIsEnumerable('c'); // false

```

### get、set

```javascript
'use strict';
'use strict';
let name = 'Leo';
let Leo = Object.defineProperty({}, 'name', {
    get: function() {
        console.log('get');
        return name;
    },
    set: function(newName) {
        console.log('set');
        name = newName;
    },
    enumerable: true,
    configurable: true
});

Leo.name = 'Jack'; // 'set'
console.log(Leo.name); // 'get' 'Jack'
```

在对Leo.name进行赋值的时候，其实是调用了name的set方法；而使用Leo.name的时候则调用了get方法。这就是Vue数据双向绑定的原理：每当数据方式改变，其实是调用了set方法，set方法里面发布数据变动的消息给订阅者，触发相应的监听回调。

注意： 如果 get 方法与 value 同时出现，会报错。
```javascript
'use strict';
let name = 'Leo';
let Leo = Object.defineProperty({}, 'name', {
    value: name, // A property cannot both have accessors and be writable or have a value
    get: function() {
        return name;
    }
});

```

# 最后

了解了 Object.defineProperty 的用法，接下来就是写一个自己的 Vue.js 了。敬请期待。<img src="/assets/img/smiling.png" alt="smiling">
