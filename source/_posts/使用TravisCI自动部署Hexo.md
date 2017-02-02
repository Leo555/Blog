---
title: 使用Travis CI自动部署Hexo
tags:
  - Travis
  - 持续集成
  - Hexo
categories: 杂记
date: 2016-11-18 10:00:36
---
# Travis CI

[Travis CI](https://travis-ci.org/) 是一个持续集成的平台，我们可以使用其自动构建部署的功能帮我们简化Hexo博客的部署流程。

## 为什么要用 Travis CI

因为懒。 <img src="/assets/img/what_can_i_say.jpg" alt="what_can_i_say">

Hexo 部署 Blog 到 GitPage 通常需要三部曲：

```shell
$ hexo clean
$ hexo g
$ hexo deploy
```
<!--more-->
很简单吧，但是如果是一个新的环境，你需要安装一大堆工具和依赖，比如要装Node，要装Hexo，还有package.json里面的各种依赖，虽然Npm提供了强大的包管理功能，但是有时候就是不方便。

使用 Travis，你只需要本地有一个 git 就可以了。

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

<img src="/assets/img/Travis.png" alt="我是一只的图片">

这里会显示你GitHub下所有的项目，选中博客仓库，我的博客在GitHub上的仓库名字就叫做 **Blog**。然后点击仓库名进入仓库配置页面。

<img src="/assets/img/Travis_settings.png" alt="我是一只的图片">

选择Settings，配置选择如下：

<img src="/assets/img/Travis_general_settings.png" alt="我是一只的图片">

* Build only if .travis.yml is present：是只有在.travis.yml文件中配置的分支改变了才构建
* Build pushes：当推送完这个分支后开始构建

这个时候，我们已经开启要构建的仓库，但是如何将构建完成后的文件推送到 Github 上呢？

## GitHub Access Token

Github 支持一种特殊的 URL 来执行 push/pull 等等操作，而不需要输入用户名密码。但这需要事先在 Github 上创建一个 token。

首先去GitHub Settings页面选择 [**Personal access tokens**](https://github.com/settings/tokens)，如果你已经登录了，点击链接进去即可。

<img src="/assets/img/Travis_generate_token.png" alt="我是一只的图片">

选择 **Generate new token**，配置如下：

<img src="/assets/img/Travis_token.png" alt="我是一只的图片">

点击绿色确认按钮，copy刚刚生成的token。回到Travis Settings页面，将复制的token加入到环境变量，并命名为 **GitHub_token**。

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
  - git commit -m "Update"
  - git push --force --quiet "https://${GitHub_token}@${GH_REF}" master:master

branches:
  only:
    - master
env:
 global:
   - GH_REF: github.com/Leo555/Leo555.github.io.git
```
将上面的nama和email还有GH_REF修改成你自己的。

这里用 Linux 环境变量的引用方式将 GH_REF 和 GitHub_token 其引入 git push 的 url，因此 push 方法就能通过 GitHub OAuth 授权，完成自动 push 的功能。

此时就万事俱备了。

# 测试

使用 Hexo 创建新的 Blog 文件，然后 push 到 GitHub 上。
```shell
$ hexo new test.md
$ git add .
$ git commit -m "add new post test"
$ git push origin master
```
然后回到 Travis 主页面，发现部署已经开始了

<img src="/assets/img/Travis_deploy.png" alt="我是一只图片">

在下面的log中可以看到部署的详细情况。

包括 **nvm install**，**npm install**，**hexo g** 等命令都在这里执行。


# 总结

有了自动部署的功能，从此以后就可以将关注点集中在博客内容上，换了平台和环境也没有任何影响。
