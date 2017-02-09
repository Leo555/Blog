---
title: ReactJS学习——组件
date: 2017-02-08 17:02:15
categories: React
tags:
- JavaScript
- ES6
- React
---

# [ReactJS 组件](https://facebook.github.io/react/docs/react-component.html)

React 提倡组件化的开发方式，每个组件只关心自己部分的逻辑，使得应用更加容易维护和复用。

React 还有一个很大的优势是基于组件的状态更新视图，对于测试非常友好。

<!-- more -->

## 数据模型

### state

React 每一个组件的实质是状态机（State Machines），在 React 的每一个组件里，通过更新 this.state，再调用 render() 方法进行渲染，React 会自动把最新的状态渲染到网页上。

```javascript
class HelloMessage extends React.Component {
  constructor() {
    super();
    this.handleClick = this.handleClick.bind(this);
    this.state = {enable: false};
  }
  //
  handleClick() {
    this.setState({enable: !this.state.enable})
  }
  //
  render() {
    return (
      <div>
        <input type="text" disabled={this.state.enable} /> 
        <button onClick={this.handleClick}>click this</button>
      </div>
    );
  }
}
ReactDOM.render(
    <HelloMessage />,
    document.getElementById('root')
);
```
通过在组件的 constructor 中给 this.state 赋值，来设置 state 的初始值，每当 state 的值发生变化， React 重新渲染页面。

注意： 

(1) **请不要直接编辑 this.state**，因为这样会导致页面不重新渲染

```javascript
// Wrong
this.state.comment = 'Hello';
```

使用 this.setState() 方法来改变它的值

```javascript
// Correct
this.setState({comment: 'Hello'});
```

(2) **this.state** 的更新可能是异步的(this.props 也是如此)

React 可能会批量地调用 this.setState() 方法，this.state 和 this.props 也可能会异步地更新，所以你不能依赖它们目前的值去计算它们下一个状态。

比如下面更新计数器的方法会失败：

```javascript
// Wrong
this.setState({
  counter: this.state.counter + this.props.increment,
});
```
第二种形式的 setState() 方法接收的参数为一个函数而不是一个对象。函数的第一个参数为 previous state，第二个参数为当前的 props

```javascript
// Correct
this.setState((prevState, props) => ({
  counter: prevState.counter + props.increment
}));
```

实现一个计数器

```javascript
class HelloMessage extends React.Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
    this.state = {counter: 0};
  }

  handleClick() {
    this.setState((prevState, props) => ({
      counter: prevState.counter + parseInt(props.increment)
    }));
  }

  render() {
    return (
      <div>
        <h1>{this.state.counter}</h1> 
        <button onClick={this.handleClick}>click this</button>
      </div>
    );
  }
}
ReactDOM.render(
    <HelloMessage increment="1" />,
    document.getElementById('root')
);
```

### props

React 的数据流是单向的，是自上向下的层级传递的，props 可以对固定的数据进行传递。

```javascript
class Welcome extends React.Component {
  render() {
    return <h1>Hello, {this.props.name}</h1>;
  }
}
```

### state vs props

state 和 props 看起来很相似，其实是完全不同的东西。

一般来说，this.props 表示那些一旦定义，就不再改变的特性，比如购物车里的商品名称、价格，而 this.state 是会随着用户互动而产生变化的特性，比如用户购买商品的个数。

## 获取 DOM

在 React 中，我们可以通过 this.refs 方便地获取 DOM：

```javascript
class HelloMessage extends React.Component {
  constructor() {
    super();
    this.handleClick = this.handleClick.bind(this);
  }
  //
  handleClick() {
    alert(this.refs.myInput.value);
  }
  //
  render() {
    return (
      <div>
        <input ref="myInput" /> 
        <button onClick={this.handleClick}>click this</button>
      </div>
    );
  }
}
ReactDOM.render(
    <HelloMessage />,
    document.getElementById('root')
);
```

## 生命周期

React 组件的生命周期大体分为三类：

- 挂载(Mounting): 已插入真实 DOM
- 更新(Updating): 正在被重新渲染
- 移除(Unmounting): 已移出真实 DOM

从流程上讲，是这样的：

(1) Mounting:

componentWillMount()： 在初次渲染之前执行一次，最早的执行点
componentDidMount()： 在初次渲染之后执行

getInitialState() –> componentWillMount() –> render() –> componentDidMount()

(2) Updating:

componentWillReceiveProps()： 在组件接收到新的 props 的时候调用。在初始化渲染的时候，该方法不会调用。
shouldComponentUpdate()： 在接收到新的 props 或者 state，将要渲染之前调用。
componentWillUpdate()： 在接收到新的 props 或者 state 之前立刻调用。
componentDidUpdate()： 在组件的更新已经同步到 DOM 中之后立刻被调用。

componentWillReceiveProps() –> shouldComponentUpdate() –> componentWillUpdate –> render() –> componentDidUpdate()

(3) Unmounting:

componentWillUnmount()： 在组件从 DOM 中移除的时候立刻被调用。


下面举 React 官网的一个输出时间的例子，在 Clock 渲染之前设置一个定时器，每隔一秒更新一下 this.state.date 的值，并在组件移除的时候清除定时器。

```javascript
class Clock extends React.Component {
  constructor(props) {
    super(props);
    this.state = {date: new Date()};
  }
  //组件初次渲染之后执行
  componentDidMount() {
    this.timerID = setInterval(
      () => this.tick(),
      1000
    );
  }
  //组件移除的时候执行
  componentWillUnmount() {
    clearInterval(this.timerID);
  }
  //
  tick() {
    this.setState({
      date: new Date()
    });
  }
  //
  render() {
    return (
      <div>
        <h1>Hello, world!</h1>
        <h2>It is {this.state.date.toLocaleTimeString()}.</h2>
      </div>
    );
  }
}
//渲染
ReactDOM.render(
  <Clock />,
  document.getElementById('root')
);
```
