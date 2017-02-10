---
title: ReactJS学习——入门
date: 2017-02-05 14:45:55
categories: React
tags:
	- JavaScript
	- ES6
	- React
---

# ReactJS 简介

[React](https://facebook.github.io/react/) 首次被提出是在2014年的 F8 大会上，当期的主题为 “Rethinking Web App Development at Facebook”，这也是 React 名字的由来。

React 以组件化的开发方式，专注于 MVC 架构中的 View，即视图， 这使得React很容易和开发者已有的开发栈进行融合。React 推荐将 UI 上每一个功能相对独立的模块定义成组件，然后将小的组件通过组合或者嵌套的方式构成大的组件，最终完成整体 UI 的构建。

<!-- more -->
# ReactJS 原理

Web 开发的最终目的是把数据反映到 UI 上，这时就需要对 DOM 进行操作，复杂或者频繁的 DOM 操作通常是性能瓶颈产生的原因。React 为此引入了虚拟 DOM（Virtual DOM） 的机制：开发者操作虚拟 DOM，React 在必要的时候将它们渲染到真正的 DOM 上。 

## Virtual DOM

基于 React 进行开发时所有的 DOM 构造都是通过虚拟 DOM 进行，每当数据变化时，React 都会重新构建整个 DOM 树，然后 React 将当前整个 DOM 树和上一次的 DOM 树进行对比，得到 DOM 结构的区别，然后仅仅将需要变化的部分更新到实际的浏览器。

同时 React 能够批处理虚拟 DOM 的刷新，在一个事件循环（Event Loop）内的两次数据变化会被合并，例如你连续的先将节点内容从 A 变成 B，然后又从 B 变成 A，React 会认为 UI 不发生任何变化。尽管每一次都需要构造完整的虚拟 DOM 树，但是因为虚拟 DOM 是内存数据，性能是极高的，而对实际 DOM 进行操作的仅仅是 Diff 部分，因而能达到提高性能的目的。

## Hello World

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Hello World</title>
    <script src="https://unpkg.com/react@latest/dist/react.js"></script>
    <script src="https://unpkg.com/react-dom@latest/dist/react-dom.js"></script>
    <script src="https://unpkg.com/babel-standalone@6.15.0/babel.min.js"></script>
  </head>
  <body>
    <div id="root"></div>
    <script type="text/babel">
      ReactDOM.render(
        <h1>Hello, world!</h1>,
        document.getElementById('root')
      );
    </script>
  </body>
</html>
```
上面的 Hello World 的例子中，引入了三个库文件，react.js，react-dom.js 和 babel.js，它们必须首先加载。在之前的版本中，需要加载 “JSXTransformer.js”，后来 React 官方不再维护这个库，由 babel 对 JSX 语法进行编译。
ReactDOM.render 是 React 的最基本方法，用于将模板转为 HTML 语言，并插入指定的 DOM 节点。

## [JSX](https://facebook.github.io/react/docs/introducing-jsx.html)

HTML 语言直接写在 JavaScript 语言之中，不加任何引号，这就是 JSX 的语法，它允许 HTML 与 JavaScript 的混写。

例如：

```html
let names = ['Leo', 'Jack', 'John'];
ReactDOM.render(
  <div>
  {
    names.map((name)=>{
      return <div>{name}</div>
    })
  }
  </div>,
  document.getElementById('root')
);
```
上面代码体现了 JSX 的基本语法规则：遇到 HTML 标签（以 < 开头），就用 HTML 规则解析；遇到代码块（以 { 开头），就用 JavaScript 规则解析。

JSX 允许直接在模板插入 JavaScript 变量。如果这个变量是一个数组，则会展开这个数组的所有成员，代码如下：

```html
let arr = [
  <h1>Hello</h1>, 
  <h1>world</h1>
];
ReactDOM.render(
  <div>
  {arr}
  </div>,
  document.getElementById('root')
);
```
ReactDOM.render 方法也可以写在函数中，例如：

```javascript
let t0 = new Date().getTime();
setInterval(()=>{
  let t = new Date().getTime(),
  delta = t - t0;
  //在虚拟DOM上创建元素
  let el = React.createElement("p",null,delta);
  //渲染到真实DOM
  ReactDOM.render(el,document.getElementById('root'));
},16);
```
## React 组件

定义 React 组件有三种方法，第一种是 JavaScript 函数，第二种是用 ES6 classes 的方式，一个是用 React.createClass

### JavaScript 函数

```javascript
function HelloMessage(props) {
  return <h1>Hello, {props.name}</h1>;
}
ReactDOM.render(
    <HelloMessage name="Leo"/>,
    document.getElementById('root')
);
```
注意这里调用属性的时候没有 this。

### React.Component

```javascript
class HelloMessage extends React.Component {
  render() {
    return <h1>Hello, {this.props.name}</h1>;
  }
}
ReactDOM.render(
  <HelloMessage name="Leo"/>,
  document.getElementById('root')
);
```

### React.createClass

React.createClass(meta) 方法用于生成组件类，参数 meta 是一个实现预定义接口的 JavaScript 对象，用来对 React 组件原型进行扩展。
在 meta 中，至少需要实现一个 render() 方法，而这个方法， 必须而且只能返回一个有效的 React 元素。这意味着，如果你的组件是由多个元素构成的，那么你必须在外边包一个顶层元素，然后返回这个顶层元素。

```javascript
const HelloMessage = React.createClass({
  render: function() {
    return <h1>Hello {this.props.name}!</h1>;
  }
});
ReactDOM.render(
  <HelloMessage name="Leo"/>,
  document.getElementById('root')
);
```

1. 组件名必须以大写字母开头
2. 组件类只能包含一个顶层标签
3. 获取属性的值用的是 this.props.属性名
4. 为元素添加 css 的 class 时，要用 className，for 属性需要写成 htmlFor， 因为 class 和 for 是 ES6 关键字

## 内联 css

```javascript
const HelloMessage = React.createClass({
  render: function() {
    return <div style={{color:"red",fontSize: "44px"}}>
          Hello {this.props.name}!</div>;
  }
});
```
内联 css 的写法与用 JavaScript 直接操作样式相同：

```javascript
document.getElementById('root').style.paddingLeft='104px';
```

### 组件组合

```html
//组合组件
class WebSite extends React.Component {
  render() {
    return (
      <div>
        <Name name={this.props.name} />
        <Link site={this.props.site} />
      </div>
    );
  }
}
//Name组件
class Name extends React.Component {
  render() {
    return (
      <h1>{this.props.name}</h1>
    );
  }
};
//Link组件
class Link extends React.Component {
  render() {
    return (
      <a href={this.props.site}>
        {this.props.site}
      </a>
    );
  }
};

ReactDOM.render(
  <WebSite name="Leo" site="https://lz5z.com" />,
  document.getElementById('root')
);
```

# 最后

ReactJS 入门暂时就到这里，后面会有更加详细的内容。