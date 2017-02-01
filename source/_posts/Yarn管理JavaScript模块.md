---
title: Yarn管理JavaScript模块
date: 2017-02-01 19:42:03
categories: JavaScript
tags:
- Yarn
- JavaScript
- Node
---

# [Yarn](https://yarnpkg.com/) 简介

Yarn 是 Facebook 开发的一款新的 JavaScript 包管理工具， 作为 NPM 的替代产品，主要是为了解决下面两个问题：

- 安装的时候无法保证速度/一致性
- 安全问题，因为 NPM 安装时允许运行代码

<!-- more -->

# Yarn vs NPM

## 速度快

相比于 NPM，Yarn 的速度更快，Yarn 会把使用过的模块在本地缓存一份，如果下次还要用到相同版本的模块，那么将会直接使用本地的而不是访问网络重新获取一份。而 NPM 使用的时候，如果不全局安装那么每个项目都要重新下载一次包，浪费时间和资源。

## 安全性

Yarn 在安装模块之前会验证文件完整性。

## 并行安装

每当 NPM 或 Yarn 需要安装一个包时，它会进行一系列的任务。在 NPM 中这些任务是按包的顺序一个个执行，这意味着必须等待上一个包被完整安装才会进入下一个；Yarn 则并行的执行这些任务，提高了性能。

## 输出清晰

NPM 安装包的时候输出惨不忍睹，而 Yarn 的输出就清晰多了。
<img src="/assets/img/yarn.png" alt="yarn">

# 使用

## 常用命令对照表

|作用|NPM 命令|Yarn 命令|
| :-| :-|:-|
|初始化| npm init| yarn init|
|安装 package.json 中的包|npm install|yarn|
|安装某个包|npm install xxx --save|yarn add xxx|
|删除某个包|	npm uninstall xxx --save|yarn remove xxx|
|开发模式下安装某个包|npm install xxx --save-dev|	yarn add xxx -dev|
|更新|npm update --save|	yarn upgrade|
|全局安装|npm install xxx –global|yarn global add xxx|
|清除缓存|npm cache clean|yarn cache clean|
|查看模块信息|npm info xxx|yarn info xxx|
|运行script|npm run|yarn run|
|测试|npm test|yarn test|

## [yarn.lock](https://yarnpkg.com/docs/configuration/#toc-use-yarn-lock-to-pin-your-dependencies) 文件

在使用 NPM 管理 JavaScript 模块的时候，可以用比较宽松的方式定义某个模块的版本信息，如

```javascript
*: 任意版本
~1.1.0: >=1.1.0 && < 1.2.0
^1.1.0: >=1.1.0 && < 2.0.0
>= 1.0.0: >= 1.0.0
3.x: 任意 3 版本
```
理想状态下使用[语义化](http://deadhorse.me/nodejs/2014/04/27/semver-in-nodejs.html)版本发布补丁不会包含大的变化，但不幸的很多时候并非如此。NPM 的这种策略可能导致两台拥有相同 package.json 文件的电脑安装了不同版本的包，这可能导致一些错误。很多模块的安装错误和环境问题都是由于这个原因导致。

为了避免包版本的错误匹配，一个确定的安装版本被固定在一个锁文件中。每次模块被添加时，Yarn 就会创建（或更新） yarn.lock 文件，这样你就可以保证其它电脑也安装相同版本的包，同时包含了 package.json 中定义的一系列允许的版本。

在 npm 中同样可以使用 [npm shrinkwrap](https://docs.npmjs.com/cli/shrinkwrap) 命令来生成一个锁文件，这样在使用 npm install 时会在读取 package.json 前先读取这个文件，就像 Yarn 会先读取 yarn.lock 一样。这里的区别是 Yarn 总会自动更新 yarn.lock，而 npm 需要你重新操作。

## [yarn install](https://yarnpkg.com/en/docs/cli/install)

npm install 命令会根据 package.json 安装依赖以及允许你添加新的模块； yarn install 仅会按照 yarn.lock 或 package.json 里面的依赖顺序来安装模块。

## [yarn add [–dev]](https://yarnpkg.com/en/docs/cli/add)

与 npm install 类似，yarn add 允许你添加与安装模块，添加依赖的同时也会将依赖写入 package.json，类似 npm 的 --save 参数；Yarn 的 --dev 参数则是添加开发依赖，类似 npm 的 --save-dev 参数。

## [yarn global](https://yarnpkg.com/en/docs/cli/global)

不像 npm 添加 -g 或 --global 可以进行全局安装，Yarn 使用的是 global 前缀（yarn global add xxx）。global 前缀只能用于 yarn add, yarn bin, yarn ls 和 yarn remove。

## [yarn why](https://yarnpkg.com/en/docs/cli/why)

该命令会查找依赖关系并找出为什么会将某些包安装在你的项目中。也许你知道为什么添加，也许它只是你安装包中的一个依赖，yarn why 可以帮你找出。
<img src="/assets/img/yarn_why.png" alt="yarn_why">

# 总结

相比 NPM，Yarn 可以方便生成锁文件，安装模块时非常迅速并且会将依赖自动添加进 package.json，模块可以并行安装。不过个人认为，Yarn 的优势不是绝对的，毕竟 NPM 久经考验，或许不久的将来，NPM 也会拥有这些特性。