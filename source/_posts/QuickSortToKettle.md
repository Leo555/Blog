---
title: 快速排序思想解决水桶问题
date: 2016-11-16 09:41:44
tags:
  - JavaScript
  - Algorithm
  - 快速排序
  - 水桶问题
categories: Algorithm
---

# 水桶问题

<img src="/assets/img/Bucket.png" alt="我是一只的图片">

假设给你n个红色的水壶和n个蓝色的水壶。它们的形状和尺寸都各不相同。所有的红色水壶盛水量都各不相同，蓝色水壶也是如此。但对于每一个红色水壶来说，都有一个蓝色水壶盛水量和其相同；反之亦然。
你的任务是配对出全部盛水量相同的红色水壶和蓝色水壶。为此，可以执行的操作为，挑出一对水壶，一只红色一只蓝色，将红色水壶灌满水，将红色水壶的水倒入蓝色水壶中，看其是否恰好灌满来判断，这个红色水壶的盛水量大于、小于或等于蓝色水壶。假设这样的比较需要花费一个单位时间。
请找出一种算法，它能够用最少的比较次数来确定所有水壶的配对。
注意:不可直接比较两个红色或者两个蓝色水壶，一次比较必须取一只红色一只蓝色。

<!--more-->
# 解决方案

## 快速排序思想解

1.首先在集合中选取一个元素作为 「基准」 pivot
2.将集合中所有元素与「基准」元素进行对比，所有小于「基准」的元素，都移到「基准」的左边；所有大于「基准」的元素，都移到「基准」的右边。
3.对「基准」元素左右两边的集合，分别进行上述两步，直到所有的子集只剩下一个元素。

代码描述：

```javascript
const quickSort = arr=> {
    if (arr.length <= 1) {
        return arr;
    }
    let pivotIndex = Math.floor(arr.length / 2);
    let pivot = arr.splice(pivotIndex, 1)[0];
    let left = [], right = [];
    for (let ai of arr) {
        if (ai < pivot) {
            left.push(ai);
        } else {
            right.push(ai);
        }
    }
    return quickSort(left).concat([pivot], quickSort(right));
};
```


## 水壶问题

1.依次从红色水壶中选取一个水壶与蓝色水壶集合对比，对比过程如下：
2.红色水壶与每一个蓝色水壶对比，盛水量大于红色水壶的蓝水壶放在右边，小于的放在左边，水量相等的为当前集合的 「基准」 元素。
3.如果当前集合中已有 「基准」 元素，则拿红色水壶与「基准」元素对比： 红色水壶大于基准元素，则选取基准元素右边的集合重复第二步; 如果红色水壶小于基准元素，则选取基准元素左边边的集合重复第二步。

### 举个栗子

现在有红色水壶容量为： [3, 5, 1, 4, 8, 2, 6]
蓝色水壶： [6, 2, 3, 1, 8, 5, 4]

第一步，选取红色水壶中第一个水壶 3 跟蓝色水壶依次对比，大于 3 的放右边，小于 3 的放左边，等于 3 的水壶为当前集合的 「基准」 元素。
```
[2, 1, ③, 6, 8, 5, 4]
```
然后选取红色水壶中的第二个水壶 5 与 「基准」 元素对比，5 > 3, 因此使用第一步的方法，拿 5 与 「基准」 元素右边的元素依次对比。
```
[2, 1, ③, 4, ⑤, 6, 8]
```
红色第三个水壶为 1， 拿 1 与第一个 「基准」 元素比较， 1 < 3, 因此使用第一步的方法， 拿 1 与 「基准」 元素左边的元素依次对比。
```
[①, 2, ③, 4, ⑤, 6, 8]
```
红色第四个水壶为 4， 拿 4 与第一个 「基准」 元素比较， 4 > 3, 因此使用第一步的方法， 拿 4 与 「基准」 元素右边的元素依次对比。
右边元素集合中又有 「基准」 元素 5 ，因此先与 「基准」 元素对比， 4 < 5， 所以拿 4 与 「基准」 元素左边的元素依次对比。
```
[①, 2, ③, ④, ⑤, 6, 8]
```
后面的顺序为
```
[①, 2, ③, ④, ⑤, 6, ⑧]

[①, ②, ③, ④, ⑤, 6, ⑧]

[①, ②, ③, ④, ⑤, ⑥, ⑧]
```

代码描述：
```javascript
'use strict';

Array.prototype.pivot = -1;
const quickMatch = (key, arr) => {
    if (arr.length <= 1) {
        console.log(`${key} matched!`);
        return;
    }
    if (arr.pivot < 0) {
        arr.left = new Array();
        arr.right = new Array();
        arr.map(ai=> {
            if (ai < key) {
                arr.left.push(ai);
            } else if (ai > key) {
                arr.right.push(ai);
            } else if (ai === key) {
                arr.pivot = key;
                console.log(`${key} matched!`)
            }
        });
    } else {
        if (key > arr.pivot) {
            quickMatch(key, arr.right);
        } else if (key < arr.pivot) {
            quickMatch(key, arr.left);
        }
    }
};
```

测试：
```javascript
let arrRed = [3, 5, 1, 4, 8, 2, 6];
let arrBlue = [6, 2, 3, 1, 8, 5, 4];

for (let key of arrRed) {
    quickMatch(key, arrBlue);
}
```

# 总结

这个算法有点类似于二叉树的思想，将红色水壶与蓝色水壶依次对比的时候，构建蓝色水壶二叉树，每个二叉树的根结点为红色水壶。平均时间复杂度为O(nlgn)。