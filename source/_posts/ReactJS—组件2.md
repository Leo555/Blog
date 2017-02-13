---
title: ReactJS学习——组件2
date: 2017-02-13 19:35:03
categories: React
tags:
- JavaScript
- ES6
- React
---

## 组件列表

使用循环的方式创建组件列表

```javascript
const numbers = [1, 2, 3, 4, 5];
const listItems = numbers.map((number) =>
  <li>{number}</li>
);
ReactDOM.render(
  <ul>{listItems}</ul>,
  document.getElementById('root')
);
```
<!-- more -->
使用参数

```javascript
function NumberList(props) {
  const numbers = props.numbers;
  const listItems = numbers.map((number) =>
    <li key={number.toString()}>
      {number}
    </li>
  );
  return (
    <ul>{listItems}</ul>
  );
}

const numbers = [1, 2, 3, 4, 5];
ReactDOM.render(
  <NumberList numbers={numbers} />,
  document.getElementById('root')
);
```
注意上面代码中的 `key`，它是一个 string 类型的属性，在创建 lists 元素的时候，你需要添加这个属性，如果不添加会有 warning。

## Keys

React 元素可以具有一个特殊的属性 key，这个属性不是给用户用的，而是给 React 自己用的。如果我们动态地创建 React 元素，而且 React 元素内包含数量或顺序不确定的子元素时，我们就需要提供 key 这个特殊的属性。

为什么需要给每一个元素一个标识呢？我们知道当组件的属性发生了变化，其 render 方法会被重新调用，组件会被重新渲染。比如元素里面 `[{name: 'Leo'}] => [{name: 'Jack'}]` 那么有可能是删除了 Leo，然后为 Jack 新建了一个，也有可能是更改了 name 属性，因此为数组中的元素传一个唯一的 key（比如用户的 ID），就很好地解决了这个问题。React 比较更新前后的元素 key 值，如果相同则更新，如果不同则销毁之前的，重新创建一个元素。

### Keys 的用法

Keys 只能被定义在循环里面

以下用法都是错误的

```javascript
function ListItem(props) {
  const value = props.value;
  return (
    // Wrong! There is no need to specify the key here:
    <li key={value.toString()}>
      {value}
    </li>
  );
}

function NumberList(props) {
  const numbers = props.numbers;
  const listItems = numbers.map((number) =>
    // Wrong! The key should have been specified here:
    <ListItem value={number} />
  );
  return (
    <ul>
      {listItems}
    </ul>
  );
}

const numbers = [1, 2, 3, 4, 5];
ReactDOM.render(
  <NumberList numbers={numbers} />,
  document.getElementById('root')
);
```

下面是正确的用法：

```javascript
function ListItem(props) {
  // Correct! There is no need to specify the key here:
  return <li>{props.value}</li>;
}

function NumberList(props) {
  const numbers = props.numbers;
  const listItems = numbers.map((number) =>
    // Correct! Key should be specified inside the array.
    <ListItem key={number.toString()}
              value={number} />
  );
  return (
    <ul>
      {listItems}
    </ul>
  );
}

const numbers = [1, 2, 3, 4, 5];
ReactDOM.render(
  <NumberList numbers={numbers} />,
  document.getElementById('root')
);
```
