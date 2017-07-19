---
title: CSS Modules学习
date: 2017-06-21 10:39:32
categories: CSS
tags:
- CSS Modules
- webpack
- vue
---

CSS Modules 的用法很简单，不过现阶段还需要 webpack 的支持。CSS Modules 的功能非常少，它一共就干了两件事：局部作用域和模块依赖。


## CSS Modules 示例

[代码地址](https://github.com/Leo555/css_modules_study)

项目路径

```
├── README.md
├── index.html
├── node_modules
│   └── ...
├── package.json
├── src
│   ├── animation.css
│   ├── colors.css
│   ├── index.js
│   └── style.css
└── webpack.config.js
```

<!--more-->

把文件 clone 下来后，安装依赖，然后就可以运行了

```shell
$ git clone https://github.com/Leo555/css_modules_study.git
$ cd css_modules_study
$ npm install
$ npm run start
```
浏览器会自动打开静态文件，方便查看效果。


## CSS Modules 用法

### webpack

首先配置 webpack 环境(本文使用webpack2)，给 css-loader 增加一个 modules 查询参数，表示打开 CSS Modules 功能。

简单的示例如下：

``` javascript
module: {
  rules: [{
    test: /\.css$/,
    loader: "style-loader!css-loader?modules"
  }]
},
```

如果需要给 CSS Modules 传递一些参数，可以用对象的方式：

```javascript
module: {
  rules: [{
    test: /\.css$/,
    use: ["style-loader", 
    {
      loader: "css-loader",
      options: {
        modules: true,
        localIdentName: '[path][name]__[local]--[hash:base64:5]',
        importLoaders: 1,
        camelCase: true
      }
    }]
  }]
}
```

### 作用域

开启 CSS Modules 后，所有的 CSS 选择器都是局部作用域，除非声明它为全局的。

```css
/*Scoped Selectors*/
.className {
  color: green;
  margin: 10px 0;
}

/*Global Selectors*/
:global(.text) {
  font-size: 22px;
}
```
以上两个 CSS class 通过如下方法被 JS 引用

```javascript
import styles from "./style.css";
// import { className } from "./style.css";

let app = document.getElementById('app')
app.innerHTML = 
`
<div class="${styles.className}">Hello CSS Modules</div>
<div class="text">Global Selectors</div>
`
```
后面的引用方式都相同，因此略去，具体可查看 [index.js](https://github.com/Leo555/css_modules_study/blob/master/src/index.js)。

查看构建后的 CSS，发现局部变量的名字被编译成 hash (`localIdentName: '[path][name]__[local]--[hash:base64:5]'`)，而全局变量的名字不变。

<img src="/assets/img/css-modules.png" alt="css-modules">

原来 CSS Modules 就做了这么一点微小的工作。

### class 继承和重写

CSS Modules 通过组合的方式进行集成，以达成代码复用的效果。

```css
/*Class Composes*/
.otherClassName {
  composes: className;
  width: 220px;
  height: 60px;
  line-height: 60px;
  border-width: 2px;
  border-style: solid;
}

/*Composes Overrides*/
.background {
  border-radius: 20px;
  background: #efefef;
  composes: otherClassName;
  border-style: dotted;
}  
```
otherClassName 继承 className，因为拥有了 color 和 margin 属性，而 background 继承 otherClassName，却重写了 border-style。

### 局部动画

在 animation.css 中，定义了动画 tada：

```css
@keyframes tada {
  from {
  transform: scale3d(1, 1, 1);
  }
  10%, 20% {
  transform: scale3d(.9, .9, .9) rotate3d(0, 0, 1, -3deg);
  }
  30%, 50%, 70%, 90% {
  transform: scale3d(1.1, 1.1, 1.1) rotate3d(0, 0, 1, 3deg);
  }
  40%, 60%, 80% {
  transform: scale3d(1.1, 1.1, 1.1) rotate3d(0, 0, 1, -3deg);
  }
  to {
  transform: scale3d(1, 1, 1);
  }
}

.tada {
  animation: tada 2s infinite;
}
```

在 style 中的引用方式如下：

```css
/*Scoped Animations*/
.backgroundAnimation {
  composes: background;
  composes: tada from './animation.css';
}
```

上面第二个 composes 也展示了如何从其它 CSS 模块中引用选择器。


### 定义变量

通过 @value 定义变量和引用变量


colors.css

```css
@value color: black;
@value fontSize: 22px;
```

引用方式

```css
/*Define variables*/
@value colors: "./colors.css";
@value color, fontSize from colors;

.color {
  composes: otherClassName;
  color: color;
  font-size: fontSize;
}
```

## Vue 结合 CSS Modules

vue-loader 中集成了 CSS Modules，可以作为模拟 CSS 作用域的替代方案。

### 使用

在 `<style>` 上添加 module 属性即可开启 CSS Modules 模式：

```html
<style module>
.red {
  color: red;
}
.bold {
  font-weight: bold;
}
</style>
```

css-loader 会自动将生成的 CSS 对象注入到 $style 中，只需要在 `<template>` 中使用动态 class 绑定：

```html
<template>
  <p :class="$style.red">
    This should be red
  </p>
</template>
```

由于它是一个计算属性，它也适用于 `:class` 的 object/array 语法：

```html
<template>
  <div>
    <p :class="{ [$style.red]: isRed }">
      Am I red?
    </p>
    <p :class="[$style.red, $style.bold]">
      Red and bold
    </p>
  </div>
</template>
```

在 JavaScript 访问它：

```html
<script>
export default {
  created () {
    console.log(this.$style.red)
  }
}
</script>
```

### 自定义注入名称

在 .vue 中可以定义不止一个 `<style>`，为了避免被覆盖，你可以通过设置 module 属性来为它们定义注入后计算属性的名称。

```html
<style module="a">
  /* identifiers injected as a */
</style>
```

## 总结

在前端模块化的道路上，CSS 显然落后 JS 非常多。ES2015/ES2016 的快速普及和 Babel/webpack 等工具的发展，让 JS 在大型项目工程化中越发强大，[最终成为一流语言](http://www.infoq.com/cn/news/2017/05/JavaScript-become-language) 。


CSS Modules 解决了哪些问题呢？

1. 消除了全局命名的问题，再也不用担心不同文件之间的命名冲突了，也不用写一层又一层的选择器了。
2. 通过 JS 去管理 CSS 之间的依赖，在引入组件的时候，可以只引入次组件需要的 CSS，组件更加独立。
3. CSS 变量 可以在 CSS 和 JS 中共享，对于复杂组件的使用会有奇效。
4. 对代码压缩也有一定帮助。

>CSS 模块化的解决方案有很多，但主要有两类。一类是彻底抛弃 CSS，使用 JS 或 JSON 来写样式。Radium，jsxstyle，react-style 属于这一类。优点是能给 CSS 提供 JS 同样强大的模块化能力；缺点是不能利用成熟的 CSS 预处理器（或后处理器） Sass/Less/PostCSS，:hover 和 :active 伪类处理起来复杂。另一类是依旧使用 CSS，但使用 JS 来管理样式依赖，代表是 CSS Modules。CSS Modules 能最大化地结合现有 CSS 生态和 JS 模块化能力，API 简洁到几乎零学习成本。发布时依旧编译出单独的 JS 和 CSS。它并不依赖于 React，只要你使用 Webpack，可以在 Vue/Angular/jQuery 中使用。是我认为目前最好的 CSS 模块化解决方案。

引自 [CSS Modules 详解及 React 中实践](https://github.com/camsong/blog/issues/5)

## 参考资料

- [CSS Modules 详解及 React 中实践](https://github.com/camsong/blog/issues/5)
- [css-modules](https://github.com/css-modules/css-modules)
- [CSS Modules 用法教程](http://www.ruanyifeng.com/blog/2016/06/css_modules.html)