---
title: PostCSS 初识
date: 2017-03-29 18:20:33
categories: JavaScript
tags:
- JavaScript
- CSS
- PostCSS
- webpack
---

## 背景

今天在吃早饭的时候就被同事@，说有一块页面效果在测试服务器的部署效果跟本地不一样：代码在本地运行没有问题，部署后发现有一个分割线的位置明显不对。来到公司后看了同事的演示，觉得可能是 css 代码压缩时出现了问题。
<!-- more -->
通过 chrome 查看相关 css，发现了问题所在，有一段代码是这样写的：

```css
.clz_editor_container {
  display: -moz-box;
  display: -webkit-flex;
  display: -ms-flexbox;
  -webkit-box-orient: vertical;
  -webkit-flex-direction: column;
  -ms-flex-direction: column;
  height: 100%;
}
```
压缩后在 chrome 中代码变成了这样的：

```css
.clz_editor_container[data-v-5fd4dedf]{
  display: -ms-flexbox;
  -ms-flex-direction: column;
  height: 100%;
}  
```
然而实际浏览器中前两句都没有生效。

因为在代码压缩时，相同的代码会默认选择比较靠后的，因此 `display: -ms-flexbox; -ms-flex-direction: column;`，而 `-ms-flexbox` 和 `-ms-flex-direction` 是为了兼容 IE 浏览器而存在的， 所以这两句 css 都没有生效。

而没有压缩的代码在浏览器中运行时，浏览器自动选择了合适的 css 语句所以没有出现问题。

解决方案很简单啦，这应该是同事写代码粗心导致的，直接把 `display: flex; flex-direction: column;`加上就行了。而且 idea 里面自动代码兼容性补全功能，所以用 idea 写出的代码应该不会出现这个问题。

然后有同事说应该有一些工具能够自动补全的，于是 google 了一下，发现这种问题早就有非常好的解决方案，那就是 PostCSS 的插件 [autoprefixer](https://github.com/postcss/autoprefixer)。

## 解决方案

首先安装 webpack 插件 postcss-loader 和 autoprefixer

```bash
$ npm i autoprefixer postcss-loader --save-dev
```
然后修改 webpack 配置文件，在插件系统中更改 LoaderOptionsPlugin，在 options 中增加 postcss 

```javascript
new webpack.LoaderOptionsPlugin({
    minimize: process.env.NODE_ENV === 'production',
    options: {
        postcss:[autoprefixer()]
    }
})
```

然后在所有 css 相关的 loader 中增加 postcss-loader

```javascript
{
    test: /\.vue$/,
    loader: 'vue-loader',
    options: {
        loaders: {
            js: '...',
            css: ExtractTextPlugin.extract({
                use: 'css-loader!postcss-loader',
                fallback: 'vue-style-loader'
            }),
            less: ExtractTextPlugin.extract({
                fallback: 'vue-style-loader',
                use: 'css-loader!postcss-loader!less-loader'
            })
        }
    }
},
{
    test: /\.css$/,
    loader: ExtractTextPlugin.extract({
        fallback: 'style-loader',
        use: 'css-loader!postcss-loader'
    })
},
{
    test: /\.less$/,
    loader: ExtractTextPlugin.extract({
        fallback: 'style-loader',
        use: 'css-loader!postcss-loader!less-loader'
    })
}
```

注意 postcss-loader 应该放在 less-loader 和 css-loader 之间，处理顺序为:
less-loader -> postcss-loader -> css-loader -> style-loader

修改前面出问题的 css 为原生

```css
.clz_editor_container {
    display: flex;
    flex-direction: column;
    height: 100%;
}
```

重新打包压缩后的 css 如下

<img src="/assets/img/postcss-css.png" alt="css文件">

重新打开查看效果，问题解决。

注意如果你在 css 中使用 `@import` 引入其它 css 文件，而被引入的文件在 webpack 打包后又没有加入浏览器前缀的话，建议在 css-loader 中加入 `importLoaders=1` 参数

```javascript
{
    test: /\.css$/,
    loader: ExtractTextPlugin.extract({
        fallback: 'style-loader',
        use: 'css-loader?importLoaders=1!postcss-loader'
    })
}
```


## [PostCSS](http://postcss.org/)

PostCSS 是什么？官方给出的定义是： PostCSS 是一个用 JavaScript 转化 CSS 的工具。准确的说，PostCSS 是一个平台，通过一些插件，能做很多事情：

（1） 增加代码可读性
比如刚才我们用的 [autoprefixer](https://github.com/postcss/autoprefixer)，通过给 css 添加供应商前缀，让我们的 css 代码更加优雅。

（2） 使用未来 CSS 的语法特性
通过使用 [cssnext](http://cssnext.io/) 插件，可以允许我们使用最新的 css 语法，而不用等待浏览器支持。

（3）global css 终结者
PostCSS 通过 [CSS Modules](https://github.com/css-modules/css-modules) 对 css 命名做模块化处理，一般为添加前缀和后缀，让我们写 css 的时候不必担心命名太通用，只要觉得有意义即可。

（4）避免 css errors
通过使用 [stylelint](https://stylelint.io/) 来避免 css errors。

（4）更强大的栅格系统
[LostGrid](http://lostgrid.org) 通过 calc() 轻松创建强大的栅格系统。

（5）[更多插件](http://postcss.parts/) 更多功能

## PostCSS webpack

在 webpack 中使用 PostCSS 的一般方式

1. 安装相关依赖

```bash
$ npm install postcss-loader --save-dev
```

2. 创建 postcss.config.js

```javascript
module.exports = {
  plugins: [
    require('postcss-smart-import')({ /* ...options */ }),
    require('precss')({ /* ...options */ }),
    require('autoprefixer')({ /* ...options */ })
  ]
}
```

可以通过在不同路径下创建不同的 config 来实现配置覆盖的功能，在根目录下创建的 postcss.config.js 会被子目录中的配置文件覆盖。

3. 添加 PostCSS Loader 到 webpack.config.js 中，记得要把它放在 css-loader 和 style-loader 后面，如果有其它 loader，如 sass-loader 或者 less-loader， 要放在它们前面。

```javascript
module.exports = {
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1
            }
          },
          'postcss-loader'
        ]
      }
    ]
  }
}
```

4. 如果不想使用 postcss.config.js 的话，也可以把插件直接写入到 webpack.config.js 中

```javascript
module.exports = {
module.exports = {
  module: {
    rules: [{
      test: /\.css/,
      use: […{
        loader: 'postcss-loader',
        options: {
          plugins: function() {
            return [
              require('precss'),
              require('autoprefixer')
            ];
          }
        }
      }]
    }]
  }
}
```

## demo

假如有 style.css 如下

```css
:root {
 --base-color: gray;
}

div {
  display: flex;
    border-radius: 10px;
    transition: all 0.8s;
    width: 100px;
    height: 50px;
    background: var(--base-color);
}

```

webpack 配置文件下

```javascript
var cssnext = require('cssnext');
var autoprefixer = require('autoprefixer');
var px2rem = require('postcss-px2rem');
var Ex = require('extract-text-webpack-plugin');
var webpack = require('webpack')

module.exports = {
  entry: './src/style.css',
  output: {
    filename: "./dist/[name].css"
  },
  module: {
    loaders: [{
      test: /\.css$/,
      loader: Ex.extract({
        fallback: 'style-loader',
        use: 'css-loader!postcss-loader'
      })
    }]
  },
  plugins: [
    new Ex({
      filename: './dist/style.css'
    }),
    new webpack.LoaderOptionsPlugin({
      options: {
        postcss: [autoprefixer({browsers: ['last 2 versions']}), 
          cssnext(), px2rem({remUnit: 100})]
      }
    })
  ]
}
```

运行 webpack 命令后，dist 文件夹下面的 style.css 如下

```css
div {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  border-radius: 0.1rem;
  -webkit-transition: all 0.8s;
  transition: all 0.8s;
  width: 1rem;
  height: 0.5rem;
  background: gray;
}
```

这里一共使用了三个插件，cssnext 解析 css 自定义属性和 val() 函数，autoprefixer 添加浏览器前缀，postcss-px2rem 完成 px 到 rem 单位的转化。

## 参考资料

1. 参考 [PostCSS](http://postcss.org/) 官方网站，了解 PostCSS 的更多内容。
2. [autoprefixer](https://github.com/postcss/autoprefixer)
3. [cssnext](http://cssnext.io/)
