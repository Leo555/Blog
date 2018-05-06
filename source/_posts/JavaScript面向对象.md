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

几乎所有面向对象的语言都有一个标志，那就是类，通过类创建具有相同属性和方法的对象。而 ECMAScript 中没有类的概念，它把对象定义为：“无序属性的集合，其属性可以包含基本值、对象或者函数”。即对象是一组没有特定顺序的值，对象的每个属性或方法都有一个名字，而这个名字都映射到一个值。因此对象的本质是一个[散列表](https://lz5z.com/JavaScript-Object-Hash/)。

<!-- more -->
# 创建对象

虽然 Object 构造函数或对象字面量都可以创建单个对象，但是这些方式有个明显的缺点：使用同一个接口创建很多对象，会产生大量重复的代码。为了解决这个问题，就可以使用工厂模式来创建对象。

## 工厂模式

工厂模式用函数来封装特定接口创建对象。

```javascript
function createPerson(name, age, job) {
    let o = new Object()
    o.name = name
    o.age = age
    o.job = job
    o.sayName = function () {
        console.log(this.name)
    };
    return o
}
let leo = createPerson('Leo', 18, "Engineer")
```

工厂模式虽然解决了创建多个相似对象的问题，但没有解决对象识别的问题（即怎样知道一个对象的类型）。

## 构造函数模式

ECMAScript 中的构造函数可以用来创建特定类型的对象，像 Object 和 Array 的原生的构造函数，在运行时会自动出现在执行环境中。此外，也可以创建自定义的构造函数，从而定义自定义对象类型的属性和方法。代码如下所示：

```javascript
function Person(name, age, job) {
    this.name = name
    this.age = age
    this.job = job
    this.sayName = function() {
        console.log(this.name)
    }
}
let leo = new Person('Leo', 18, "Engineer")
let jack = new Person('Jack', 18, "Engineer")
```

构造函数模式与工厂模式有以下不同：

1. 没有显式的创建对象； 
2. 直接将属性和方法赋给了this对象； 
3. 没有return语句； 

构造函数应该以大写字母开头，使用 new 操作符。new 操作符创建对象经历以下 4 个步骤：

1. 创建新的对象；
2. 将构造函数的作用域赋给新对象（因此 this 就指向了这个新对象）；
3. 执行构造函数中的代码（为这个新对象添加属性）；
4. 返回新对象；

生成的对象 leo 中有一个 constructor 属性，该属性指向 Person，并且可以用 instanceof 做类型检测。

```javascript
leo.constructor === Person // true
leo instanceof  Object // true
leo instanceof Person // true
```

构造函数的缺点在于每个方法都要在每个实例上重新创建一遍。在前面例子中，leo 和 jack 都有一个名为 sayName 的方法，但是这两个方法不属于同一个对象。

那么我们能不能共享一个 sayName() 方法。如果想要完成这种需求，大可像下面代码一样，通过把函数定义转移到构造函数的外部。

```javascript
function Person(name, age, job) {
    this.name = name
    this.age = age
    this.job = job
    this.sayName = sayName
}

function sayName() {
    console.log(this.name)
};
let leo = new Person('Leo', 18, "Engineer")
let jack = new Person('Jack', 18, "Engineer")

console.log(leo.sayName === jack.sayName) // true
```

上面例子中的做法，确实解决了两个函数做同一件事的问题，但是无意中定义了很多全局函数，而这些全局函数中由于包含 “this” 关键字，又只能被某个函数调用。不仅污染了全局作用域，还使得这个自定义的引用类型完全丧失封装性。好在这些问题都可以通过原型模式解决。

## 原型模式

JavaScript 中创建的每个函数都有一个 prototype 属性，这个属性是一个指针，指向一个对象，而这个对象的用途是包含可以由特定类型的 **所有实例共享的属性和方法**。prototype是通过调用构造函数而创建的那个对象实例的对象原型，使用原型对象的好处是可以让所有对象实例共享它所包含的属性和方法。

```javascript
function Person() {}
Person.prototype.name = 'Leo'
Person.prototype.age = 18
Person.prototype.sayName = function() {
	console.log(this.name)
}
let leo1 = new Person
let leo2 = new Person
leo1.sayName()
leo2.sayName()
```

在此，我们将 sayName() 方法和所有的属性直接添加到了 Person 的 prototype 属性中，构造函数变成了空函数，而通过 new 创建出来的对象具有相同的属性和方法。但是与构造函数模式不同对的是，新对象的这些属性和方法是由所有的实例共享的，也就是说

```javascript
leo1.sayName === leo2.sayName; // true
```

## 组合使用构造函数模式和原型模式

创建自定义对象最常见的形式就是组合使用构造函数模式和原型模式，构造函数用于定义类的实例属性，而原型模式用于定义对象的共享属性。

```javascript
function Person(name, age) {
    this.name = name;
    this.age = age;
    this.friends = [];
}
Person.prototype = {
    constructor: Person,
    sayName: function() {
        console.log(this.name);
    }
}
let leo = new Person('Leo', 18);
let jack = new Person('Jack', 18);
leo.friends.push('Elsa');
jack.friends.push('Lucy');
leo.sayName === jack.sayName; // true
jack.friends === leo.friends; // false
```

实例属性都是在构造函数中定义的，而实例共享属性 constructor 和方法 sayName() 则是在原型中定义的。这种构造函数与原型混成的模式，是目前 ECMAScript 中使用最广泛、认同度最高的一种创建自定义对象的方法。

## 动态原型模式

动态原型模式将所有信息封装在了构造函数中，而通过构造函数中初始化原型（仅第一个对象实例化时初始化原型），又保持了同时使用构造函数和原型的优点。换句话说，可以通过检查某个应该存在的方法是否有效，来决定是否需要初始化原型。

```javascript
function Person(name, age) {
    this.name = name;
    this.age = age;
    if (typeof this.sayName != 'function') {
        Person.prototype.sayName = function() {
            console.log(this.name);
        }
    }
}
let leo = new Person('Leo', 18);
leo.sayName();
```


Person 是一个构造函数，通过 new Person() 来生成实例对象。每当一个 Person 的对象生成时，Person 内部的代码都会被调用一次。

如果去掉 if 的话，你每 new 一次(即每当一个实例对象生产时)，都会重新定义一个新的函数，然后挂到 Person.prototype.sayName 属性上。而实际上，你只需要定义一次就够了，因为所有实例都会共享此属性的。而加上 if 后，只在 new 第一个实例时才会定义 sayName 方法，之后就不会了。
 
假设除了sayName 方法外，你还定义了很多其他方法，比如 sayBye、cry、smile 等等。此时你只需要把它们都放到对 sayName 判断的 if 块里面就可以了。

```javascript
if (typeof this.sayName != "function") {
    Person.prototype.sayName = function() {...};
    Person.prototype.sayBye = function() {...};
    Person.prototype.cry = function() {...};
}
```
这样一来，要么它们全都还没有定义(new 第一个实例时)，要么已经全都定义了(new 其他实例后)，即它们的存在性是一致的，用同一个判断就可以了，而不需要分别对它们进行判断。

使用动图原型模式时，不能使用对象字面量重写原型，如果在已经创建实例的情况下重写原型，会切断现有实例和原型之间的联系。


## 寄生构造函数模式

寄生构造函数的基本思想是创建一个函数，该函数的作用仅仅是封装创建对象的代码，然后返回新创建的对象。

```javascript
function Person(name, age) {
    let o = new Object();
    o.name = name;
    o.age = age;
    o.sayName = function() {
        console.log(this.name)
    }
    return o;
}
let leo = new Person('Leo', 18);
leo.sayName();
```

在这个例子中，Person 函数创建了一个新对象，并以相应的属性和方法初始化该对象，然后返回这个对象。除了使用 new 操作符并把使用的包装函数叫做构造函数外，这个模式跟工厂模式一模一样。构造函数在不返回值的情况下，默认会返回新的对象实例。

这个模式在特殊的情况下可以用来为对象创建构造函数。假如我们想创建一个具有额外方法的特殊数组，由于不能直接修改 Array 的构造函数，因此可以使用这种模式。

```javascript
function SpecialArray() {
    let values = new Array();
    values.push.apply(values, arguments);
    values.toPipedString = function() {
        return this.join('|');
    }
    return values;
}
let colors = new SpecialArray('red', 'blue', 'green');
console.log(colors.toPipedString()); // 'red|blue|green'
```

关于寄生构造函数模式，有一点需要说明：返回的对象与构造函数或者构造函数的原型属性直接没有关系，所以不能依赖 instanceof 操作符来确定对象类型。

## 稳妥构造函数模式

稳妥对象，是指没有公共属性，而且方法也不引用 this 的对象，适合在一些安全环境中（禁用 this 和 new），或者在防止数据被其它应用程序改动时使用。稳妥构造函数遵循与寄生构造函数类似的模式，但是有两点不同：一是新创建对象的实例方法不引用 this，二是不使用 new 操作符调用构造函数。

```javascript
function Person(name, age) {
    let o = new Object();
    o.sayName = function() {
        console.log(this.name);
    };
    return o;
}

let leo = Person('Leo', 18);
leo.sayName();
```
注意在这种模式创建的对象中，除了使用 sayName 方法之外，没有其他办法访问 name 属性，即使有其他代码给这个对象添加属性或者方法，也不可能有别的办法访问传入到构造函数中的原始数据。

与寄生构造函数类似，稳妥构造函数模式创建的对象与构造函数直接也没有什么关系，所以不能依赖 instanceof 操作符来确定对象类型。

# 总结

组合使用构造函数模式和原型模式是目前使用最广的方法，如果不希望构造函数和原型相互分离的话，可以使用动态原型模式。

