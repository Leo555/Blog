---
title: React Hooks 是什么
date: 2019-01-07 22:34:24
categories: React
tags:
- React
- Hooks
---


最近在重构 BadJS 的管理页面，使用 TypeScript + React Hooks 的技术栈，趁这个机会好好理一理 React Hooks 那些事儿。

React Hooks 是 16.7.0-alpha 版本的新特性，安装即可享用。

## React Hooks 简介

React Hooks 是对 React function 组件的一种扩展，通过一些特殊的函数，让无状态组件拥有状态组件才拥有的能力。

Hooks 是 React 函数组件中的一类特殊函数，通常以 use 开头，比如 useRef，useState，useReducer 等。通常在我们写 React 组件的时候，如果这个组件比较复杂，拥有自己的生命周期或者 state，就将其写成 class 组件；如果这个组件仅仅用来展示，就将其写成 function 组件。

React Hooks 使用 function 组件的写法，通过 useState 这样的 API 解决了 function 组件没有 state 的问题，通过 useEffect 来解决生命周期的问题，通过自定义 hooks 来复用业务逻辑。

### Hooks 解决哪些问题

- 复用与状态有关的逻辑，之前引申出来 HOC 的概念，但是 HOC 会导致组件树的臃肿。
- 解决组件随着业务扩展变得难以维护的问题。
- 使用更容易理解并且对初学者更友好的 function 组件。

<!--more-->


## 用法

Hooks 主要分三种：

- State hooks: 允许开发者在 function 组件中使用 state。
- Effect hooks: 允许开发者在 function 组件中使用生命周期和 side effect。
- Custom hooks: 自定义 hooks，可以在里面使用 State Hooks 和 Effect Hooks，达到组件之间逻辑复用。


### State Hooks

看一下官方给出的 demo

```jsx
import { useState } from 'react';

function Example() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>
        Click me
      </button>
    </div>
  );
}
```

这里的 useState 就是一个 hook，返回一个数组，第一个 count 表示一个 state，默认值为 0；第二个 setCount 相当于 class function 中的 setState，表示对 count 的更新操作。

这样写的好处是每个 state 独立管理，避免状态复杂的时候 state 臃肿。


### Effect Hooks

Effect Hooks 允许在组件中执行副作用（side effects），类似于类中的生命周期方法。通常我们需要在 componentDidMount 和 componentDidUpdate 写一些操作，可能是更新数据，也可能是更新 Dom。除此之外，我们还会在 componentWillUnmount 的时候解绑一些事件监听防止内存泄露。这些都导致了组件维护成本的增大。而在 function 组件中，又没有这些生命周期，因此 Hooks 使用 Effect Hooks 来取代这些生命周期，完成一部分能力。

看一下官方给出的动态更改 title 的 demo：


```javascript
import { useState, useEffect } from 'react';

function Example() {
  const [count, setCount] = useState(0);

  // Similar to componentDidMount and componentDidUpdate:
  useEffect(() => {
    // Update the document title using the browser API
    document.title = `You clicked ${count} times`;
  });

  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>
        Click me
      </button>
    </div>
  );
}
```

如果没有 useEffect，我们需要在 componentDidMount 和 componentDidUpdate 中同时去调用更改 title 的方法，以完成组件初始化的状态和数据更新的状态。useEffect 本质上就是传递一个函数给 React，React 在组件渲染完成后和更新后调用这个函数。默认情况下，它在第一次渲染之后和每次更新之后都运行。

可以将 useEffect Hook 视为 componentDidMount，componentDidUpdate 和 componentWillUnmount 的组合。

那 useEffect 什么时候执行 componentWillUnmount 的操作呢？

如果 useEffect 中返回一个函数，在 React 卸载当前的组件的时候，会执行这个函数，用于清理 effect。

对比需要清理 effect 和不需要清理 effect 的两种写法：

```javascript
function FriendStatusWithCounter(props) {
  const [count, setCount] = useState(0);
  useEffect(() => {
    document.title = `You clicked ${count} times`;
  });

  const [isOnline, setIsOnline] = useState(null);
  useEffect(() => {
    ChatAPI.subscribeToFriendStatus(props.friend.id, handleStatusChange);
    return () => {
      ChatAPI.unsubscribeFromFriendStatus(props.friend.id, handleStatusChange);
    };
  });

  function handleStatusChange(status) {
    setIsOnline(status.isOnline);
  }

  return (/*...*/);
}  
```

通过跳过 Effect 来优化性能。

通常，每次组件渲染或者更新都去执行某些逻辑会带来无谓的消耗，所以我们经常会写这样的代码：

```javascript
componentDidUpdate(prevProps, prevState) {
  if (prevState.count !== this.state.count) {
    document.title = `You clicked ${this.state.count} times`;
  }
}
```

只有组件更新前后的 state.count 发生变化的时候，才去更新 title。

用 Hooks 可以更简单地处理这个问题

```javascript
useEffect(() => {
  document.title = `You clicked ${count} times`;
}, [count]); // Only re-run the effect if count changes
```

给 useEffect 传入第二个参数，这个参数是一个数组。如果组件重新渲染，只有这个 count 发生变化的时候 React 才会执行函数 中的内容，否则会直接跳过这个 effect。如果数组中是多个参数，那么只要其中一个发生变化，React 都会执行函数中的内容。


这也适用于具有清理阶段的 effect ：

```javascript
useEffect(() => {
  ChatAPI.subscribeToFriendStatus(props.friend.id, handleStatusChange);
  return () => {
    ChatAPI.unsubscribeFromFriendStatus(props.friend.id, handleStatusChange);
  };
}, [props.friend.id]); // Only re-subscribe if props.friend.id changes
```

如果希望 effect 只在组件 componentDidMount 和 componentWillUnmount 的时候执行，则只需要给第二个参数传一个空数组即可。


## Hooks 的规则

React Hooks 其实不仅仅是功能层面的增强，也给 React 注入了新的软件思想。这就是最近几年开始流行的 “约定大于配置”，比如 Hooks 函数必须使用 use 开头，还有接下来要讲的规则。前面在我的文章 [webpack4 新特性](https://lz5z.com/webpack4-new/) 也提到了这个内容。


### 只在顶层调用 Hooks

Hooks 只能在顶层调用，不要在循环，条件或嵌套函数中调用 Hook。原因是 React 需要保证每次组件渲染的时候都以相同的顺序调用 Hooks。


假如一个组件中有多个 Hooks，React 如何知道哪个 state(状态) 对应于哪个 useState 调用呢？答案是 React 依赖于调用 Hooks 的顺序。本质上来说 Hooks 就是数组（[React hooks: not magic, just arrays](https://medium.com/@ryardley/react-hooks-not-magic-just-arrays-cd4f1857236e)）。每次执行 useState 都会改变下标，如果 useState 被包裹在 condition 中，那每次执行的下标就可能对不上，导致 useState 更新错数据。


### 只能在 React Function 中调用 Hooks


Hooks 只能在 React function 组件中调用，或者在自定义 Hooks 中调用。通过遵循此规则，可以确保组件中的所有 stateful （有状态）逻辑在其源代码中清晰可见。


### eslint

[eslint-plugin-react-hooks](https://www.npmjs.com/package/eslint-plugin-react-hooks) 可以保证强制执行上述两个规则。


```shell
$ npm install eslint-plugin-react-hooks@next
```

```javascript
// Your ESLint configuration
{
  "plugins": [
    // ...
    "react-hooks"
  ],
  "rules": {
    // ...
    "react-hooks/rules-of-hooks": "error"
  }
}
```


## 自定义 Hooks

自定义 Hooks 就是将组件之间需要共有的逻辑抽出来写成单独的函数。与一般的函数的区别是，自定义 Hooks 是一个以 use 开头的函数，内部可以调用其它的 Hooks。

```javascript
import { useState, useEffect } from 'react';

function useFriendStatus(friendID) {
  const [isOnline, setIsOnline] = useState(null);

  function handleStatusChange(status) {
    setIsOnline(status.isOnline);
  }

  useEffect(() => {
    ChatAPI.subscribeToFriendStatus(friendID, handleStatusChange);
    return () => {
      ChatAPI.unsubscribeFromFriendStatus(friendID, handleStatusChange);
    };
  });

  return isOnline;
}

export useFriendStatus;
```

在另外一个组件中，将其引入后，就可以使用了

```javascript
import {useFriendStatus} from 'hooks/xxx.js';

function FriendListItem(props) {
  const isOnline = useFriendStatus(props.friend.id);

  return (
    <li style={{ color: isOnline ? 'green' : 'black' }}>
      {props.friend.name}
    </li>
  );
}
```

可以看出，自定义 Hooks 就是一个 JavaScript 函数而已，并没有什么特别。

- 自定义 Hooks 函数名必须以 use 开头（规约优先）。
- 两个组件使用相同的 Hooks，但是其内部 state 是独立的。




























