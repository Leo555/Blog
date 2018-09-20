---
title: webpack4 新特性
date: 2018-09-15 17:13:58
categories: JavaScript
tags:
- webpack
- webpack4
---

wepack4 出来已经有半年了，目前最新的 release 版本为 [4.19.0](https://webpack.docschina.org/concepts/)。由于之前项目打包一直存在性能问题，所以我一直很关注 webpack 和其社区的发展。目前来说 webpack4 已经趋于稳定，很多关键的插件也都更新了对 webpack4 的支持；更为重要的是，webpack4 的官方文档（中英文）已经很完善了，因此现在不学习 webpack4，更待何时。根据 webpack 作者 Tobias Koppers 的说法，他们已经着手开始开发 webpack5 了。

关于 webpack 入门的文章可以参考 [webpack 从入门到放弃](https://lz5z.com/webpack/)。
关于 webpack 性能优化的内容可以参考 [webpack 打包优化](https://lz5z.com/webpack%E6%89%93%E5%8C%85%E5%8A%A0%E9%80%9F%E5%AE%9E%E6%88%98/)。
关于 webpack4 全部新的特性可以查看官方的 [releases](https://github.com/webpack/webpack/releases/tag/v4.0.0)。

<!--more-->

## 学习参考

学习一项新知识最好能站在巨人的肩膀上，其中 angular-cli、create-react-app 和 vue-cli 中对 webpack4 中的使用都是我们学习和模仿的对象。

### 参考 [create-react-app](https://github.com/facebook/create-react-app)

使用 npx 创建 react-demo，创建之后 `npm run eject` 就可以看到它详细的 webpack 配置了。

```bash
$ npx create-react-app react-demo
$ cd react-demo
$ npm run eject / yarn eject
```

不过比较遗憾的是正式版本的 create-react-app 暂时还不支持 webpack4，我们可以使用 `react-scripts@2.0.0-next.3e165448` 来体验 webpack4 的特性。

```bash
$ # Create a new application
$ npx create-react-app@next --scripts-version=2.0.0-next.3e165448 react-demo
$ # Upgrade an existing application
$ yarn upgrade react-scripts@2.0.0-next.3e165448
```

<img src="/assets/img/create-react-app-webpack.png" alt="create-react-app-webpack">

其中 config 目录下的与 webpack 相关的三个文件是非常好的学习和借鉴的对象，可以说适应于绝大多数中小型项目。


### 参考 vue-cli

[Vue CLI3](https://cli.vuejs.org/zh/) 简直可以说是学习和使用 vue 中一个无敌的存在，其中 @vue/cli-service 中集成了 webpack 的默认配置，带来开箱即用的快感；不过 Vue CLI 没有像 angular-cli 和 create-react-app 那样提供 eject 命令，而是通过 vue.config.js 进行包括 webpack 在内的全局配置。其可视化工具 [vue ui](https://cli.vuejs.org/zh/guide/creating-a-project.html#%E4%BD%BF%E7%94%A8%E5%9B%BE%E5%BD%A2%E5%8C%96%E7%95%8C%E9%9D%A2) 中的 inspect 可以查看 webpack 参数，非常强大。

Vue CLI3 内部的 webpack 配置是通过 [webpack-chain](https://github.com/mozilla-neutrino/webpack-chain) 维护的，这个库提供了一个 webpack 原始配置的上层抽象，使其可以定义具名的 loader 规则和具名插件，并有机会在后期进入这些规则并对它们的选项进行修改。

如果你的项目也有链式访问特定的 loader 的需求的话，不妨参考一下 Vue CLI3。

<img src="/assets/img/vue-cli-webpack.png" alt="vue-cli-webpack">

如果不希望使用 webpack-chain 的话，可以参考其它比较成熟的 vue 项目，比如 [vue-element-admin](https://github.com/PanJiaChen/vue-element-admin/tree/master/build) 也非常具有借鉴意义。

## webpack4 升级建议

- webpack4 依赖 node 版本 >= 6.11.5，node4 及其以下版本将不再支持。所以首先需要检查 node 是否需要升级。
- 还需要安装 webpack-cli 到 devDependencies 中。
- 如果是升级一个已有项目的话，可以使用 `npm outdated` 查看与 webpack 相关的 loader 和 plugin 是否需要升级。
- [extract-text-webpack-plugin](https://github.com/webpack-contrib/extract-text-webpack-plugin) 让位于 [mini-css-extract-plugin](https://github.com/webpack-contrib/mini-css-extract-plugin)。
- [html-webpack-plugin](https://github.com/jantimon/html-webpack-plugin) 在使用过程中如果遇到  `thrownewError('Cyclic dependency'+nodeRep)` 的错误的话，可以使用 Alpha 版本 `npm i--save-dev html-webpack-plugin@next`。

> 由于 webpack4 以后对 css 模块支持的逐步完善和 commonChunk 插件的移除，在处理 css 文件提取的计算方式上也做了些调整。所以之前一直使用的 extract-text-webpack-plugin 也完成了它的历史使命，将让位于 mini-css-extract-plugin。

extract-text-webpack-plugin 会将 css 内联在 js 中，这样带来的问题是：css 或者 js 的改动都会影响整个 bundle 的缓存。而 mini-css-extract-plugin 在 code Splitting 的时候会将原先内联写在每一个 js chunk bundle 的 css，单独拆成了一个个 css 文件。然后再通过 [optimize-css-assets-webpack-plugin](https://github.com/NMFR/optimize-css-assets-webpack-plugin) 这个插件对 css 进行压缩和优化。

<span style="opacity:0.7">备注：optimize-css-assets-webpack-plugin 默认使用 cssnano 进行 css 代码优化，但是也会导致一些问题，比如我之前遇到的 z-index 重新计算的问题和 keyframes 重命名的问题：[解决 webpack 打包后 z-index 重新计算的问题](https://lz5z.com/%E8%A7%A3%E5%86%B3webpack%E6%89%93%E5%8C%85%E5%90%8Ez-index%E9%87%8D%E6%96%B0%E8%AE%A1%E7%AE%97%E7%9A%84%E9%97%AE%E9%A2%98/)。 </span>


## webpack4 带来的变化

可能是受到 [parcel](http://www.css88.com/doc/parcel/)（一款号称快速，零配置的 Web 应用程序打包器）的影响，webpack4 也引入了零配置的概念，遵从软件行业更先进的『规约大于配置』的理念。

### 模式（mode）

mode 有三个值：

| 选项 | 描述 |
| :-| :-|
|development|会将 process.env.NODE_ENV 的值设为 development。启用 NamedChunksPlugin 和 NamedModulesPlugin。|
|production|会将 process.env.NODE_ENV 的值设为 production。启用 FlagDependencyUsagePlugin, FlagIncludedChunksPlugin, ModuleConcatenationPlugin, NoEmitOnErrorsPlugin, OccurrenceOrderPlugin, SideEffectsFlagPlugin 和 UglifyJsPlugin。|
|none|不选用任何默认优化选项|

（1）可以在启动命令后加入参数使用：

```javascript
"scripts": {
  "dev": "webpack --mode development",
  "build": "webpack --mode production"
}
```
（2）也可以在配置文件中加入 mode 属性：

- mode: development

```javascript
// webpack.development.config.js
module.exports = {
+ mode: 'development'
- plugins: [
-   new webpack.NamedModulesPlugin(), // 当开启 HMR 的时候使用该插件会显示模块的相对路径
-   new webpack.NamedChunksPlugin(),  // 根据文件名来生成稳定的 chunkid
-   new webpack.DefinePlugin({ "process.env.NODE_ENV": JSON.stringify("development") }) // 向代码注入了 NODE\_ENV 这个环境变量
- ]
}
```

development 模式默认开启了 NamedChunksPlugin 和 NamedModulesPlugin 方便调试，提供了更完整的错误信息，更快的重新编译的速度。

- mode: production

```javascript
// webpack.production.config.js
module.exports = {
+  mode: 'production',
-  plugins: [
-    new UglifyJsPlugin(/* ... */), // JS 代码压缩
-    new webpack.optimize.ModuleConcatenationPlugin(), // 作用域提升(scope hoisting)，提升代码在浏览器中的执行速度
-    new webpack.NoEmitOnErrorsPlugin(), // 在编译出现错误时，跳过输出阶段
-    new webpack.DefinePlugin({ "process.env.NODE_ENV": JSON.stringify("production") })
-  ]
}
```

production 模式提供代码压缩和代码分割，同时 webpack 也会自动进行 Scopehoisting 和 Tree-shaking。

可以看出 mode 本质上是提供了一些默认的配置，以此来简化 webpack 的使用门槛。


## [optimization(优化)](https://webpack.docschina.org/configuration/optimization/)

optimization 是 webpack4 中最大的改进，其中包括代码压缩，分割，优化等功能。

### 使用 optimization.splitChunks 进行分包

webpack4 移除 CommonsChunkPlugin，取而代之的是两个新的配置项（optimization.splitChunks 和 optimization.runtimeChunk）来进行分包。

我们来看下 create-react-app 生成的关于分包的配置：

```javascript
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin'); // 用来压缩以及优化 css
module.exports = {
  mode: 'production',	
  optimization: {
    minimizer: [
      new UglifyJsPlugin({
        uglifyOptions: {/* ... */},
        // Use multi-process parallel running to improve the build speed
        // Default number of concurrent runs: os.cpus().length - 1
        parallel: true,
        // Enable file caching
        cache: true
      }),
      new OptimizeCSSAssetsPlugin({ cssProcessorOptions: { safe: true } }),
    ],
    // Automatically split vendor and commons
    splitChunks: {
      chunks: 'all',
      name: 'vendors'
    },
    // Keep the runtime chunk seperated to enable long term caching
    runtimeChunk: true
  }
}
```

在分包功能上主要使用 [splitChunks](https://webpack.docschina.org/configuration/optimization/#optimization-splitchunks) 和 [runtimeChunk](https://webpack.docschina.org/configuration/optimization/#optimization-runtimechunk) 两个参数。


### optimization.splitChunks

默认情况下 splitChunks 的配置就适用于大多数用户。webpack4 将会按照以下规则自动进行分包：

- 新的 chunk 是否被分享或者是否来自 node_modules。
- 新的 chunk 在压缩和 gzip 前是否大于 30kb。
- 按需加载 chunk 的并发请求数量小于等于 5 个。
- 页面初始化时需要加载的 chunk 并发数量小于等于 3 个。

为了满足后面两个条件，webpack 有可能受限于包的最大数量值，生成的代码体积往上增加。

默认配置对应的参数如下：

```javascript
optimization: {
  splitChunks: {
    chunks: 'async',
    minSize: 30000,
    minChunks: 1,
    maxAsyncRequests: 5,
    maxInitialRequests: 3,
    automaticNameDelimiter: '~', 
    name: true,
    cacheGroups: {
      vendors: {
        test: /[\\/]node_modules[\\/]/,
        priority: -10
      },
      default: {
        minChunks: 2,
        priority: -20,
        reuseExistingChunk: true
      }
    }
  }
}
```

(1) splitChunks.chunks

表示哪些 chunks 会被分割，可以提供字符串或者 function 作为参数。如果传字符串的话，值可以是 “all”、“async”、“initial”。“all” 表示无论 chunk 是 async 还是 non-async 都可以被共享。

(2) splitChunks.cacheGroups

默认模式会将所有来自 node_modules 的模块分配到 一个叫 vendors 的缓存组；所有重复引用至少两次的代码，会被分配到 default 的缓存组。

一个模块可以被分配到多个缓存组，优化策略会将模块分配至跟高优先级别（priority）的缓存组，或者会分配至可以形成更大体积代码块的组里。

默认来说，缓存组会继承 splitChunks 的配置。所有上面列出的选择都是可以用在缓存组里的：chunks, minSize, minChunks, maxAsyncRequests, maxInitialRequests, name。

可以通过 `optimization.splitChunks.cacheGroups.default: false` 禁用 default 缓存组。

可以使用如下的方式提取公共代码：

```javscript
cacheGroups: {
  commons: {
    name: "commons",
    chunks: "initial",
    minChunks: 2
  }
}
```

(3) minSize: 形成一个新代码块最小的体积，默认是 30 kb。
(4) minChunks: 在分割之前，这个代码块最小应该被引用的次数（保证代码块复用性，默认值为 1 ，即不需要多次引用也可以被分割）。
(5) maxInitialRequests: 一个入口最大的并行请求数，默认是 3。
(6) maxAsyncRequests: 按需加载时候最大的并行请求数，默认是 5。
(7) name: 要控制代码块的命名，可以用 name 参数来配置，当不同分割代码块被赋予相同名称时候，他们会被合并在一起。如果赋予一个神奇的值 true，webpack 会基于代码块和缓存组的 key 自动选择一个名称。


### optimization.runtimeChunk 

webpack4 提供了 runtimeChunk 能让我们方便的提取 manifest，以前我们需要这样配置

```javascript
new webpack.optimize.CommonsChunkPlugin({
  name: "manifest",
  minChunks: Infinity
});
```

webpack4 中则只需要

```javascript
runtimeChunk: true,
// OR manifest
runtimeChunk: {
  name: "manifest"
}
```

通过 `optimization.runtimeChunk: true` 选项，webpack 会添加一个只包含运行时(runtime)额外代码块到每一个入口。
这个需要看场景使用，会导致每个入口都加载多一份运行时代码。其实打包生成的 runtime.js 非常的小，gzip 之后一般只有几 kb，但这个文件又经常会改变，导致我们每次都需要重新请求它，它的 http 耗时远大于它的执行时间了，所以建议不要将它单独拆包，而是将它内联到 index.html 之中。

```javascript
const ScriptExtHtmlWebpackPlugin = require('script-ext-html-webpack-plugin') // 支持 prefetch preload
// 注意一定要在 HtmlWebpackPlugin 之后引用
// inline 的 name 和 runtimeChunk 的 name 保持一致

new ScriptExtHtmlWebpackPlugin({
  inline: /runtime..*.js$/
})
```

### webpack 中的 [runtime 和 manifest](https://webpack.docschina.org/concepts/manifest/)

在使用 webpack 构建的应用程序中，主要包含三种类型的代码：

- 我们自己编写的代码
- 源码依赖的第三方 library 或者 “vendor”
- webpack 的 runtime 和 manifest，管理所有模块的交互

runtime 以及伴随的 manifest 数据，主要是指：在浏览器运行时，webpack 用来连接模块化的应用程序的所有代码。

（1）runtime

在模块交互时，连接模块所需的加载和解析逻辑。包括浏览器中的已加载模块的连接，以及懒加载模块的执行逻辑。

（2）manifest

当编译器(compiler)开始执行、解析和映射应用程序时，它会保留所有模块的摘要信息。这个摘要的数据集合称为 "Manifest"，当完成打包并发送到浏览器时，在运行时通过 Manifest 来解析和加载模块。

无论选择哪种模块语法，那些 import 或 require 语句现在都已经转换为 `__webpack_require__` 方法，此方法指向模块标识符(module identifier)。通过使用 manifest 中的数据，runtime 将能够查询模块标识符，检索出背后对应的模块。

可以理解为在应用程序运行时，编译器通过 manifest 中的数据来查找相应的模块，管理模块的加载和执行。


### 优化分包策略

根据业务的复杂程度，一般在我们的代码中存在以下几种类型的代码：

基础组件库：react/vue; redux/vuex/mobx; react-router/vue-router; axios; 
UI 组件库：Ant Design/Element;
必要组件/公共组件：Nav; Footer; Header; 全局配置等
非必要组件/代码：自己封装的组件和函数
低频组件：富文本; Markdown-Editor; Echarts 等
业务代码：业务组件; 业务模块; 业务页面等


- 基础类库 chunk-libs

它是构成我们项目必不可少的一些基础类库，比如 vue 全家桶或者 reat 全家桶，它们的升级频率都不高，但每个页面都需要它们，还有一些全局被共用的，体积不大的第三方库也可以放在其中：比如 nprogress、js-cookie、clipboard 等。

也可以使用 webpack 的 dll 技术将这些代码抽取为动态链接库。

- UI 组件库

可以考虑将 UI 组件库也打包在 libs 中，不过相比于 chunk-libs，它的升级频率更高，并且体积更大，因此单独打包是更好的选择。

- 自定义组件/函数 chunk-commons

自定义组件可以选择单独打包成 bundle，也可以与业务代码打包在一起，还是要结合具体情况来看。

- 低频组件

低频组件和 chunk-commons 最大的区别是，它们只会在一些特定业务场景下使用，比如富文本编辑器、js-xlsx 等。webpack4 会根据这些库的大小（30kb）选择将其打包成独立的 bundle 或者 直接打包到具体的页面 bundle 中。

- 业务代码

一般按照页面来划分打包。


## [webpack4 plugins](https://webpack.docschina.org/api/plugins)

webpack 插件是一个具有 apply 方法的 JavaScript 对象。apply 属性会被 webpack compiler 调用，并且 compiler 对象可在整个编译生命周期访问。

- 定义 apply 方法。
- 指定一个绑定到 webpack 自身的事件钩子。
- 使用 webpack 提供的 plugin API 操作构建结果。

```javascript
const pluginName = 'BasicPlugin'

class BasicPlugin {
  constructor(options) {

  }	
  apply(compiler) {
    compiler.hooks.run.tap(pluginName, compilation => {
      console.log('webpack 构建过程开始！')
    })
  }
}
```

使用这个插件

```javascript
const BasicPlugin = require('./BasicPlugin.js')
module.export = {
  plugins:[
    new BasicPlugin(options),
  ]
}
```

### 插件运作原理
 
webpack 基于插件的运行模式非常强大，也是其能够迅速占领市场，社区活跃的主要原因。如果把 webpack 比作流水线，插件就是流水线上一个个工人。webpack 通过 [Tapable](https://github.com/webpack/tapable) 来组织这条复杂的流水线。

webpack 在运行过程中会广播事件，每个插件只需要监听它所关心的事件，就能加入到这条生产线中，从而改变生产线的运作。webpack 中基于观察者模式的事件流机制保证了其运行的有序性。

插件的核心是两个继承于 Tapable 的对象： Compiler 和 Compilation，它们是连接插件与 webpack 之间的桥梁。在插件代码的编写中，只要拿到了这两个对象，就可以实现广播和监听事件。

- Compiler 对象包含了 webpack 环境所有的的配置信息，包含 options，loaders，plugins 这些信息，这个对象在 webpack 启动时候被实例化，它是全局唯一的，可以简单地把它理解为 webpack 实例。
- Compilation 对象包含了当前的模块资源、编译生成资源、变化的文件等。当 webpack 以开发模式运行时，每当检测到一个文件变化，一次新的 Compilation 将被创建。Compilation 对象也提供了很多事件回调供插件做扩展。通过 Compilation 也能读取到 Compiler 对象。

Compiler 和 Compilation 的区别在于：Compiler 代表了整个 webpack 从启动到关闭的生命周期，而 Compilation 只是代表了一次新的编译。

### 插件事件流变化

webpack4 插件的编写方式与之前发生了变化，主要表现在 Compiler 和 Compilation 中事件监听和广播的表现形式。

webpack3:

```javascript
/**
* 广播出事件
* event-name 为事件名称，注意不要和现有的事件重名
* params 为附带的参数
*/
compiler.apply('event-name', params);

/**
* 监听名称为 event-name 的事件，当 event-name 事件发生时，函数就会被执行。
* 同时函数中的 params 参数为广播事件时附带的参数。
*/
compiler.plugin('event-name', function(params) {

});

// compilation.apply 和 compilation.plugin 使用方法和上面一致。
```

webpack4:

[html-webpack-plugin](https://github.com/jantimon/html-webpack-plugin) 中在 compilation.hooks 上添加了 htmlWebpackPluginBeforeHtmlGeneration 对象：

<img src="/assets/img/webpack-plugin-hooks-2.png" alt="webpack-plugin-hooks">

来看下 [html-webpack-include-assets-plugin](https://github.com/jharris4/html-webpack-include-assets-plugin) 的兼容写法。

<img src="/assets/img/webpack-plugin-hooks.png" alt="webpack-plugin-hooks">


## 参考资料

- [webpack](https://webpack.docschina.org/)
- [手摸手，带你用合理的姿势使用 webpack 4](https://mp.weixin.qq.com/s/bQvRFb3luLkvj0MEOvbsJw)
- [没有了CommonsChunkPlugin，咱拿什么来分包（译）](https://github.com/yesvods/Blog/issues/15)
- [Webpack原理-编写Plugin](https://segmentfault.com/a/1190000012840742)


