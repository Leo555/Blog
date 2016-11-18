---
title: 使用Travis CI自动部署Hexo
tags:
  - Travis
  - 持续集成
  - Hexo
categories: Hexo
date: 2016-11-18 10:00:36
---


# [Travis CI](https://travis-ci.org/)

Travis CI 是一个持续集成的平台，我们可以使用其自动构建部署的功能帮我们简化Hexo博客的部署流程。

## 为什么要用 Travis CI

因为懒。

<!--more-->
虽然Hexo部署Blog到GitPage只需要几个命令，但是如果是一个新的环境，你需要安装一大堆依赖，比如要装Node，要装Hexo，还有package.json里面的各种依赖，虽然Npm提供了强大的包管理功能，但是有时候就是不方便。

使用Travis，你只需要本地有一个git就可以了。

每当你 Push 一个 commit 到 Github 时，Travis CI 会检测到你的提交，并根据配置文件自动运行一些命令，通常这些命令用于测试，构建等等。

那么在我们的需求下，就可以用它运行一些 hexo deploy -g 之类的命令用来自动生成、部署我们的网站。

# 使用方法

使用Travis构建Hexo只需要三步：

1. 登录Travis，配置仓库
2. 在Travis CI配置GitHub的Access Token
3. Blog根目录下配置.travis.yml

## 配置Travis仓库

首先使用GitHub账号登录[Travis SI](https://travis-ci.org/)，登录后会进入如下页面

<img src="/assets/img/Travis_main_page.png" alt="我是一只的图片">

点击「My Repositories」后面的 **+**，添加要自动构建的仓库

<img src="/assets/img/Travis1.png" alt="我是一只的图片">

这里会显示你GitHub下所有的项目，选中博客仓库，我的博客在GitHub上的仓库名字就叫做 **Blog**。然后点击仓库名进入仓库配置页面。

<img src="/assets/img/Travis_settings.png" alt="我是一只的图片">

选择Settings，配置选择如下：

<img src="/assets/img/Travis_general_settings.png" alt="我是一只的图片">

* Build only if .travis.yml is present：是只有在.travis.yml文件中配置的分支改变了才构建
* Build pushes：当推送完这个分支后开始构建

这个时候，我们已经开启要构建的仓库，但是如何将构建完成后的文件推送到github上呢？于是我们需要GitHub的Access Token了。

## GitHub Access Token

首先去GitHub Settings页面选择 [**Personal access tokens**](https://github.com/settings/tokens)，如果你已经登录了，点击链接进去即可。

<img src="/assets/img/Travis_generate_token.png" alt="我是一只的图片">

选择 **Generate new token**，配置如下：

<img src="/assets/img/Travis_token.png" alt="我是一只的图片">

点击绿色确认按钮，copy刚刚生成的token。回到Travis Settings页面，将复制的token加入到环境变量。

<img src="/assets/img/Travis_add_token.png" alt="我是一只的图片">

## .travis.yml

上述步骤完成后，只需要在你Blog源代码的根目录下增加一个 **.travis.yml** 文件，
我的文件内容如下：
```yml
language: node_js
node_js: stable

install:
  - npm install

script:
  - hexo clean
  - hexo g

after_script:
  - cd ./public
  - git init
  - git config user.name "YOUR GITHUB USER NAME"
  - git config user.email "YOUR GITHUB EMAIL"
  - git add .
  - git commit -m "Update docs"
  - git push --force --quiet "https://${GH_TOKEN}@${GH_REF}" master:master

branches:
  only:
    - master
env:
 global:
   - GH_REF: github.com/Leo555/Leo555.github.io.git
```
记得将上面的nama和email还有GH_REF修改成你自己的。

此时就万事俱备了。

# 测试

