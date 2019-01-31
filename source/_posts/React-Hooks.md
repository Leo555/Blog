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


### 什么是 Hooks ？

React Hooks 是对 React function 组件的一种扩展，通过一些特殊的函数，让无状态组件拥有状态组件才拥有的能力。

Hooks 是 React 函数组件中的一类特殊函数，通常以 use 开头，比如 useRef，useState，useReducer 等。通常在我们写 React 组件的时候，如果这个组件 比较复杂，拥有自己的生命周期或者 state，就将其写成 class 组件；如果这个组件仅仅用来展示，就将其写成 function 组件。

React Hooks 使用 function 组件的写法，通过 useState 这样的 API 解决了 function 组件没有 state 的问题，通过 useEffect 来解决生命周期的问题，通过自定义 hooks 来复用业务逻辑。所以 React Hooks 要解决的根本问题是组件之间状态处理逻辑共享的问题。


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


再来看下 Effect Hooks

### Effect Hooks

Effect Hooks 允许在组件中执行副作用（side effects），类似于类中的生命周期方法。

> 副作用：






























