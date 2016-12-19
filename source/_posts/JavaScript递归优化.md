---
title: JavaScript递归优化
date: 2016-11-03 00:35:34
tags: 
- JavaScript
categories: Algorithm
---

# 背景 

在之前的项目 **Regional Guideline** 中，有一个操作点击 Ext 树的一个结点，展开这个结点的全部子树（树的深度未知），刚开始看到 TreeNode 中有一个名为 expand 的 Public Method， 其API如下：

![](http://i1.piimg.com/567571/c1346477e1e277a6.png)
[公司使用的版本为ExtJS 3.3]

<!-- more -->

简单明了，expand 第一个参数 deep 是一个 Boolean 型参数，如果为true的话，就展开当前结点以及子结点的所有子结点。

于是没有多加思考就用了。在开发测试环节一直没有出现什么问题，可是到了Production测试，帮忙测试的同学发现： 在操作树的时候，有时候浏览器会崩溃。刚开始以为是特殊情况，浏览器问题之类的，没有在意。可是不断地测试发现浏览器崩溃的情况是可复现的，就是在某几个固定的树展开的时候会出现这个问题。可见这不是浏览器的问题，是我代码的问题。

排查代码，发现这个 expand 方法似乎是罪魁祸首。查看ExtJS源码，果然是这个家伙的问题，原来这个函数使用递归的方式去展开所有的子结点，而当子结点比较多的时候，内存和CPU的消耗变得非常大，于是浏览器就崩溃了。

# 分析问题

首先查看 ExtJS 源码， TreeNode 中的 expand 方法的源码如下

```javascript
/**
 * Expand this node.
 * @param {Boolean} deep (optional) True to expand all children as well
 * @param {Boolean} anim (optional) false to cancel the default animation
 * @param {Function} callback (optional) A callback to be called when
 * expanding this node completes (does not wait for deep expand to complete).
 * Called with 1 parameter, this node.
 * @param {Object} scope (optional) The scope (this reference) in which the callback is executed. Defaults to this TreeNode.
 */
expand : function(deep, anim, callback, scope){
    if(!this.expanded){
        if(this.fireEvent('beforeexpand', this, deep, anim) === false){
            return;
        }
        if(!this.childrenRendered){
            this.renderChildren();
        }
        this.expanded = true;
        if(!this.isHiddenRoot() && (this.getOwnerTree().animate && anim !== false) || anim){
            this.ui.animExpand(function(){
                this.fireEvent('expand', this);
                this.runCallback(callback, scope || this, [this]);
                if(deep === true){
                    this.expandChildNodes(true, true);
                }
            }.createDelegate(this));
            return;
        }else{
            this.ui.expand();
            this.fireEvent('expand', this);
            this.runCallback(callback, scope || this, [this]);
        }
    }else{
       this.runCallback(callback, scope || this, [this]);
    }
    if(deep === true){
        this.expandChildNodes(true);
    }
}
```

expandChildNodes 的源码如下

```javascript
/**
 * Expand all child nodes
 * @param {Boolean} deep (optional) true if the child nodes should also expand their child nodes
 */
expandChildNodes : function(deep, anim) {
    var cs = this.childNodes,
        i,
        len = cs.length;
    for (i = 0; i < len; i++) {
            cs[i].expand(deep, anim);
    }
}
```

查看调用关系，发现 expand 方法如果传参 deep = true 的话会调用 expandChildNodes 方法去展开当前结点的子结点，而 expandChildNodes 方法又调用 expand  方法逐个展开子结点的所有子结点。 这样就变成了递归。


## 说说递归

假设有一个求和函数sum： sum(n) = ∑ k

### 循环

```javascript
function sum(n) {
  var result = n;
  while (n > 1) {
    result += --n;
  }
  return result;
}
```

循环自然是速度和性能最好的，但是在编写复杂的代码时，循环代码的数学描述性不够强。

### 普通递归

```javascript
function sum(n) {
  if (n === 1) {
    return 1;
  }
  return n + sum(--n);
}
```

使用上述递归的方式可以说是将代码与数学描述完美结合，以上代码给一个完全不懂编程的人也看得懂。

但是我们分析其计算过程，比如计算sum(5)的时候，其计算过程是这样的:

```
sum(5)
(5 + sum(4))
(5 + (4 + sum(3)))
(5 + (4 + (3 + sum(2))))
(5 + (4 + (3 + (2 + sum(1)))))
(5 + (4 + (3 + (2 + 1))))
(5 + (4 + (3 + (3))))
(5 + (4 + (6))
(5 + 10)
15
```

这样的计算有什么问题呢？

我们知道线程在执行代码的时候，计算机会分配一定大小的栈空间，每次方法调用时都会在栈里储存一定信息（如参数、局部变量、返回地址、调用位置等等），这些信息会占用一定空间，成千上万个此类空间累积起来，可能会导致栈溢出。

### 尾递归

```javascript
function sum(x, total = 0) {
    if (x === 1) {
        return x + total;
    }
    return sum(--x, x + total);
}
```

计算 sum(5)的时候，其过程是这样的:

```
sum(5, 0)
sum(4, 5)
sum(3, 9)
sum(2, 12)
sum(1, 14)
15
```

sum()函数多了一个total参数，这个参数记录在递归调用时上一次计算的结果，并将其传入下一次递归调用中。每一次函数调用都发生在函数最后一步操作，所以不需要保留外层函数的调用记录，因为调用位置、内部变量等信息都不会再用到了，只要直接用内层函数的调用记录，取代外层函数的调用记录就可以了。

函数在尾部调用自身，就称为尾递归。

尾递归的本质，其实是将递归方法中的需要的“所有状态”通过方法的参数传入下一次调用中。

与普通递归相比，由于尾递归的调用处于方法的最后，因此方法之前所积累下的各种状态对于递归调用结果已经没有任何意义，因此完全可以把本次方法中留在堆栈中的数据完全清除，把空间让给最后的递归调用。这样的优化使得递归不会在调用堆栈上产生堆积，意味着即使是“无限”递归也不会让堆栈溢出。这便是尾递归的优势。

## ES6对尾递归的支持

ES6中将会资磁zīcí尾递归优化，通过尾递归优化，JavaScript代码在解释成机器码的时候，会将尾递归函数解释成while函数，达到写的时候表达性强，运行的时候速度高的效果。

下面来看Babel编译的效果，将上述为递归的sum函数编译后如下：

```javascript
"use strict";

function sum(_x2) {
    var _arguments = arguments;
    var _again = true;

    _function: while (_again) {
        var x = _x2;
        _again = false;
        var total = _arguments.length <= 1 || _arguments[1] === undefined ? 0 : _arguments[1];

        if (x === 1) {
            return x + total;
        }
        _arguments = [_x2 = --x, x + total];
        _again = true;
        total = undefined;
        continue _function;
    }
}
```

## 严格模式

ES6的尾递归优化只在严格模式下开启，正常模式是无效的。
这是因为在正常模式下，函数内部有两个变量，可以跟踪函数的调用栈。
    
    * arguments：返回调用时函数的参数。
    * func.caller：返回调用当前函数的那个函数。

尾调用优化发生时，函数的调用栈会改写，因此上面两个变量就会失真。严格模式禁用这两个变量，所以尾调用模式仅在严格模式下生效。

# 解决问题

回到最早的问题，如何高效地展开一棵不知深浅的树？

当时并没有尾递归方面的知识，而且改Ext源码也不是那么方便，于是通过Google知道了一个比较好的解决方案：使用栈代替递归。

怎么做呢？

要展开一棵树，首先将树的根结点入栈，然后一个节点一个节点出栈，每次出栈后，将出栈节点的所有子节点入栈，以此达到遍历一颗树的效果。出栈的过程中逐一展开当前节点的字结点。

```javascript
expandAllChildNodes: function(node) {
    var nodeStack = [];
    nodeStack.push(node);
    while (nodeStack.length > 0) {
        var nodeTop = nodeStack.pop();
        if (nodeTop.hasChildNodes()) {
            nodeTop.expand();
            nodeStack = nodeStack.concat(nodeTop.childNodes);
        }
    }
}
```

这个方法将递归转化为栈，可读性也不是很差，算是一个不错的解决方案。测试发现之前几个导致浏览器崩溃的树都可以完美展开，O(∩_∩)O~~。

# 总结

递归本质上是一种循环操作。纯粹的函数式编程语言没有循环操作命令，所有的循环都用递归实现，这就是为什么尾递归对这些语言极其重要。

循环代表着高效，递归代表着易读，如果能将递归方便地转化为循环是想必那是极好的，可是如果转化不是那么方便的话，尽量使用尾递归。
