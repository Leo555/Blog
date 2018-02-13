---
title: webpack打包加速实战
date: 2018-01-13 09:05:31
categories: JavaScript
tags:
- webpack3
- dll
---

## webpack 打包优化

最近项目不算忙，抽时间重构了一下项目的打包，先说一下成就。

在我的开发电脑上：

OS: macOS High Sierra 
CPU: 2.6 GHz Intel Core i5 
内存: 8G 1600 DDR3
硬盘: 1 TB SATA磁盘

代码全量编译时间从 4 分 51 秒优化到 2 分 08 - 20 秒左右。

在项目编译电脑上：

OS: Ubuntu 16.04.3 LTS
CPU: Intel(R) Core(TM) i5-7500 CPU @ 3.40GHz
内存: 64G 2133 DDR4
硬盘: 1 TB SSD 

代码全量编译时间从 4 分 08 秒优化到 1 分 10 - 20 秒左右。

<!--more-->

## 用了哪些手段

### 升级电脑

升级 SSD 可能是提升效果最明显的吧，从上面两组数据中就可以看出。相同的优化在 SSD 中表现要明显很多。

### 升级 webpack3

[webpack 3: Official Release!!](https://medium.com/webpack/webpack-3-official-release-15fd2dd8f07b)

如果你的项目还在用 webpack2 的话，强烈建议你升级到 webpack3。webpack3 向下兼容，只不过有一些插件需要同时升级，注意看控制台给出的日志，把需要升级的一起升级了就好了。

#### Scope Hoisting-作用域提升

webpack 打包的时候，每个模块都被一个闭包函数包裹，过多的闭包函数降低了浏览器中 JS 执行效率，Scope Hoisting 的作用是减少闭包函数的数量，将有关联的模块放到同一个闭包函数中。

启用方法

```javascript
module.exports = {
  plugins: [
  new webpack.optimize.ModuleConcatenationPlugin()
  ]
}
```

Scope Hoisting 是基于 ECMAScript Module syntax ，对于 Commonjs 和 AMD 的模块不适用。

上面升级的算是副本，下面才是正文。

## 正文开始

现在开发的项目算是比较大的项目，严格来说，是多个 SPA 组成的多项目。这样做的好处是能减少架构师的工作，同一份架构给多个项目使用，能保证项目稳定性。坏处也比较明显，就是会额外引入无用的依赖，比如共用的 helper 模块，很多项目都引用了，但是并不是每个项目都使用里面的每个函数。这点 tree-shaking 可以给出解决方案，但是实际开发过程中，由于同事们代码质量参差不齐，有些没用到的函数和模块也都引用了，所以导致 tree-shaking 的效果并不是很好。比如在大项目中，同事把几个 helper 里面函数全部封装到 vue-filter 中，当然里面的内容主要项目大多数都引用到了，但是后面同事在初始化一个小项目的同时，无论是否需要也都用了相同的代码（copy and paste）。

```javascript
import * as helpers from 'helpers'
import * as helpers2 from 'helpers/string'
import * as helpers3 from 'helpers/...'
import * as helpers4 from 'helpers/...'

// register global utility filters.
let _filters = Object.assign(helpers, helpers2, helpers3, helpers4)
Object.keys(_filters).forEach(key => Vue.filter(key, _filters[key]))
```

于是 helper 中每个 function 都挂载在 Vue-filter 中，所以完美的避开了 tree-shaking。

另外 tree-shaking 虽然能够一定程度的减少打包后代码的体积，但是开发和编译的速度还是会受到一定的影响。

下面是代码打包速度优化的一些思路，多数来源于网上的资料。

### commonChunkPlugin 抽取公共代码

抽取公共代码有两个好处，一个是能减少编译代码的数量，一个是能够充分利用浏览器缓存，比如遇到项目切换的情况，使用 service-worker 中缓存共用的 common 代码能够减少请求的数量。

以下是 vue-cli 中给出的解决方案

```javascript
// split vendor js into its own file
new webpack.optimize.CommonsChunkPlugin({
  name: 'vendor',
  minChunks(module) {
    // any required modules inside node_modules are extracted to vendor
    return (
      module.resource &&
      /\.js$/.test(module.resource) &&
      module.resource.indexOf(
        path.join(__dirname, '../node_modules')
      ) === 0
    )
  }
}),
// extract webpack runtime and module manifest to its own file in order to
// prevent vendor hash from being updated whenever app bundle is updated
new webpack.optimize.CommonsChunkPlugin({
  name: 'manifest',
  minChunks: Infinity
}),
// This instance extracts shared chunks from code splitted chunks and bundles them
// in a separate chunk, similar to the vendor chunk
// see: https://webpack.js.org/plugins/commons-chunk-plugin/#extra-async-commons-chunk
new webpack.optimize.CommonsChunkPlugin({
  name: 'app',
  async: 'vendor-async',
  children: true,
  minChunks: 3
}),

```


### DLL 预编译

DLL 预编译的作用是将项目中稳定的依赖单独打包编译生成动态链接库，在业务代码中引用。这点在开发过程中优势比较明显，每次更新代码重新编译的时候都能够省去 DLL 库的编译，有不小的速度提升。

DLL 需要有一个额外的打包过程，新建一个 webpck.dll.conf.js 用来打包 DLL，并且在 package.json 中添加打包过程。

package.json

```javascript
{
  "scripts": {
    ...
    "build": "rimraf dist && npm run dll && npm run build:server && npm run build:client"
    ...
    "dll": "cross-env NODE_ENV=dll node build",
    ...
  }
}
```


webpack.dll.conf.js

```javascript
const webpack = require('webpack')
const path = require('path')
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
const os = require('os')

const vendors = [
  'babel-polyfill',
  'es6-promise',
  'vue/dist/vue.esm.js',
  'vue-router',
  'vuex',
  'vuex-router-sync',
  'axios',
  'cookie'
]

module.exports = {
  output: {
    path: path.resolve(__dirname, '../dist'),
    filename: '[name].dll.js',
    library: '[name]_[hash]'
  },
  entry: {
    'vendor': vendors,
  },
  plugins: [
    new UglifyJsPlugin({
      ... // 压缩参数略
    }),
    new webpack.DllPlugin({
      context: __dirname,
      path: path.join(__dirname, '../dist', '[name]-manifest.json'),
      name: '[name]_[hash]',
    })
  ]
}
```

通过运行 `npm run dll` 在 dist 目录下生成了两个文件 vendor.dll.js 和 vendor.manifest.json。其中 vendor.dll.js 中是打包压缩后的 vendor 代码，vendor.manifest.json 是 vendor 文件的 node_modle 路径和 webpack 打包 id 的映射。

然后通过 DllReferencePlugin 将 vendor 引入业务代码。

```javascript
// 这里将生成的 vendor.dll.js 文件 copy 到 你需要的目录 
new CopyWebpackPlugin([{
  from: 'dist/vendor.dll.js',
  to: config.build.assetsSubDirectory,
  flatten: true
}]),
new webpack.DllReferencePlugin({
  context: __dirname,
  manifest: require('../dist/vendor-manifest.json')
}),
```

最后还需要在 html 中引入生成的 DLL，网上有一些教程是直接把 script 标签写入 html 中的，但是由于我们多个项目同时依赖同一份 html 模板，其中某一些项目并不需要引入 DLL，比如一些静态页面。于是使用 html-webpack-include-assets-plugin 实现按需加载。

```javascript
...pkgs.reduce((pre, current) => {
  let res = [new HtmlWebpackPlugin(current.plugin)]
  let {assets, filename} = current.plugin || {}
  if (pre) res = [...pre, ...res]
  if (assets) {
    return [...res, new HtmlWebpackIncludeAssetsPlugin({
    files: [filename],
    assets: assets.map(item => `${assetsSubDirectory}/${item}`),
    append: false,
    publicPath: assetsPublicPath
    })]
  }
  return res
}, null),
```

在 pkgs 中控制 HtmlWebpackPlugin 的参数，和是否需要引入 vendor.dll.js。

pkg 模板如下：

```javascript
const extChunks = IS_PROD ? ['manifest'] : []
const chunksSortMode = IS_PROD ? 'dependency' : 'auto'
const template = 'static/templates/index.pug'
const minfiy = {}

exports pkg = {
  'index': {
    buddle: 'server-index-bundle.js',
    entry: path.resolve(__dirname, '...省略路径../entry.js'),
    plugin: {
      filename: 'app/index.html',
      chunks: ['app', 'vendor', 'common', ...extChunks],
      inject: true,
      assets: ['vendor.dll.js'],
      chunksSortMode,
      template,
      minify
    }
  },
  // 如果没有额外的依赖 assets 不用传
 '404': {
    plugin: {
      filename: '404.html',
      chunks: ['exception'],
      inject: true,
      chunksSortMode,
      template: 'static/404.pug',
      minify
    }
  }
}
```

打包后可以明显看到 app.js 和 vendor.js 体积缩小，但是项目总体积略有增大。因为通过 DLL 的方式，额外存储了外部依赖的路径和 ID。

### alias 减少搜索路径

这点想必大家都知道

```javascript
module.exports = {
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
      'static': path.resolve(__dirname, '../static')
  	},
  	// 可以用引用 node_modules 里面的方法引用 src 下面的模块
  	modules: [path.resolve(__dirname, '../src'), "node_modules"]
  }
}
```

### 多线程加速 

（1） uglifyjs-webpack-plugin 多线程提示 JS 压缩效率

使用 [uglifyjs-webpack-plugin](https://github.com/webpack-contrib/uglifyjs-webpack-plugin) 不仅可以加速 webpack 压缩 js 代码的速度，还能与 [webpack tree-shaking](https://doc.webpack-china.org/guides/tree-shaking/) 配合，减少代码体积。webpack 本身并不会执行 tree-shaking。它需要依赖于像 UglifyJS 这样的第三方工具来执行实际的未引用代码(dead code)删除工作。

```javascript
new UglifyJsParallelPlugin({
  uglifyOptions: {
    ecma: 8,
    mangle: true,
    output: {
      beautify: false
    },
    compress: {
      drop_console: true
    }
  },
  sourceMap: false,
  cache: true,
  parallel: os.cpus().length * 2,
  exclude: /\.min\.js$/
}),
```

记得开启缓存，能有效提升打包效率。

（2） happypack 多线程提升 loader 执行效率。

使用 happypack 之前，你可以先去 [Loader Compatibility List](https://github.com/amireh/happypack/wiki/Loader-Compatibility-List) 看一下 happypack 的兼容性列表。

```javascript
const os = require('os')
const HappyPack = require('happypack')
const happyThreadPool = HappyPack.ThreadPool({ size: os.cpus().length })

module.exports = {
  module: {
    rules: [
      test: /\.js$/,
      use: [
        {
          loader: 'cache-loader', // 使用 cache-loader 缓存
          options: {
          	cacheDirectory: resolve('node_modules/.cache')
          }
        },
        'happypack/loader?id=babel' // 将 babel loader替换为 happypack
      ],
      exclude: /node_modules/,
        include: [
          resolve('src'), resolve('test')
       ]
    ]
  },
  plugins: [
  	// 使用 happypack 插件
    new HappyPack({ 
	  id: 'babel',
	  threadPool: happyThreadPool,
	  verbose: false,
      loaders: [{
        loader: `babel-loader`
      }]
    })
  ]
}
```

使用 happypack 后，性能比较差的 mac mini 速度反而降低了一些，但是性能比较强的编译机速度有不少的提升，所以 happypack 可以酌情使用，测试后发现速度有提升再加入，没有提升就果断弃用。

### 缓存 HardSourceWebpackPlugin

[hard-source-webpack-plugin](https://github.com/mzgoddard/hard-source-webpack-plugin) 也是利用缓存效果提升打包速度。

> HardSourceWebpackPlugin is a plugin for webpack to provide an intermediate caching step for modules.

用法很简单

```javascript
const HardSourceWebpackPlugin = require('hard-source-webpack-plugin')
module.exports = {
  plugins: [
    new HardSourceWebpackPlugin()
  ]
}
```

## dev 优化

开发的时候，使用 koa-webpack-middleware 的 devMiddleware, hotMiddleware 两个中间件是提供 dev 服务和代码热新服务，devMiddleware 本质上是对 webpack-dev-middleware 的一层封装，而 hotMiddleware 是对 webpack-hot-middleware 的一层封装。

开发过程中，所有的代码均被载入两个 webpack 服务中，因此有一丁点的代码改动都需要重新编译所有的 buddle，这对开发过程是极其不好的体验，因此划分代码依赖，通过 npm 参数编译不同的项目，来达到加速开发的效果。

比如使用 `npm run dev project1` 来开发项目 project1，而其它代码并不加载到 webpack 中。

拿到 project1 参数可以通过 node.js 的 process 对象

```javascript
let projects = process.argv.slice(2)
if (!!projects && projects.length) {
  // filter your entry
}
```

## 总结

以上打包优化都是参考网上的一些东西， 在实际使用过程中，发现有些文章内容是写了，但是并没有亲身实践，有些错误或者不完善的地方甚至都是一模一样的，所以自己结合实际项目走了一遍流程后，还是决定把东西写出来，希望对看到的人有帮助。