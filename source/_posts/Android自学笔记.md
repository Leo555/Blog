---
title: Android自学笔记
date: 2016-09-28 22:01:00
tags: 
- Android
- 入门
categories: Android
---

<img src="/assets/img/android.png" alt="android">

# Android简介

Android是一种基于Linux的自由及开放源代码的操作系统，主要使用于移动设备，如智能手机和平板电脑，由Google公司和开放手机联盟领导及开发。

<!-- more -->
## Android的独特之处

1. 基于Linux的免费开源平台：手机制造商对其钟爱有加，因为他们可以对这个平台进行定制，而无需支付版权费。开发人员也喜欢它，因为他们知道这个平台不受制于任何可能破产或被收购的厂商。
2. 基于组件的架构：能够以不同于开发人员最初设想的方式使用应用的组成部分，甚至可以将内置组件替换为改进版本。
3. 大量现成的服务：GPS、蓝牙、数据库、浏览器、地图。
4. 自动管理应用的生命周期：多重安全保障能够将程序彼此隔离，从而提高了系统的稳定性。最终用户不必关心哪些应用处于活动状态，也无需关闭一些程序以便运行其他程序。Android针对电量和内存有限的设备进行了优化。
5. 高品质图形和声音。
6. 可移植性：所有程序都使用Java编写，并由Android的ART预先编译器或Dalvik虚拟机执行，因此代码可移植到ARM、x86和其他体系结构。支持各种输入方法，如键盘、游戏手柄、触摸、电视遥控、鼠标和跟踪球。可针对任何屏幕分辨率和朝向定制用户界面。

# Android四大组件

## Activity

Activity通常就是一个单独的屏幕，它上面可以显示一些控件也可以监听并处理用户的事件做出响应。Activity之间通过Intent进行通信。

## Service

Service 是一段长生命周期的，没有用户界面的程序，例如网络监视器或更新检查应用程序。

## Content Provider

可以将Content Provider看作数据库服务器，它的任务是管理对持久数据的访问，例如 SQLite 数据库。Content Provider使一个应用程序的指定数据集提供给其他应用程序。

## BroadcastReceive
Android应用程序可以过滤感兴趣的外部事件（电话呼入、网络可用等）并做出响应。BroadcastReceive没有用户界面。然而，它们可以启动一个activity或serice 来响应它们收到的信息，或者用NotificationManager来通知用户。

---

Android 应用程序是连同一个 AndroidManifest.xml 文件一起部署到设备的。AndroidManifest.xml 包含必要的配置信息，以便将它适当地安装到设备。它包括必需的类名和应用程序能够处理的事件类型，以及运行应用程序所需的许可。例如，如果应用程序需要访问网络 — 例如为了下载一个文件 — 那么 manifest 文件中必须显式地列出该许可。很多应用程序可能启用了这个特定的许可。这种声明式安全性有助于减少恶意应用程序损害设备的可能性。

# Android开发环境

## 所需软件

1. [JDK](http://www.oracle.com/index.html)
2. [Android Studio](http://developer.android.com/index.html)
3. [Genymotion](https://www.genymotion.com/download/)

安装过程：next到底。

天朝可以看这个网站[http://www.android-studio.org/](http://www.android-studio.org/)

Genymotion需要注册才能下载，如果本地没有VM VirtualBox，
请选择 **“With VirtualBox”**的下载。

### Genymotion和Android Studio关联

1. 给Android Studio安装Genymotion插件：

**“File -- Settings -- Plugins -- Browse Repositories -- Genymotion Download and install”**

![](http://p1.bpimg.com/567571/8ce31e7a3ab1d2e7.png) 

重启Android Studio后，选择菜单栏“View--Toolbar”，让工具栏显示出来，可以看到工具栏多了个Genymotion Device Manager的图标：

![](http://p1.bqimg.com/567571/a8438291d5e060b6.png)

点击这个图标，加载之前安装好的Genymotion文件夹，启动Genymotion模拟器。

![](http://p1.bpimg.com/567571/4394d82bf3ebba68.png)

启动后选择你所需要的Android版本和手机型号就可以了。
当然了，如果要在模拟器上运行程序，还要确保模拟器加载了Android SDK：

![](http://p1.bpimg.com/567571/b25279917e251377.png)

## Hello World
终于到了鸡冻人心的Hello World环节

**“File -- New -- New Projct”**创建新的工程文件

![](http://p1.bpimg.com/567571/0b2a119095c7ce10.png)

输入应用程序的名字和 Company Domain

![](http://i1.piimg.com/567571/2b7d1569addca78d.png)

选择Empty Activity

![](http://i1.piimg.com/567571/56bc6911b473cf37.png)

创建后的效果如下：

![](http://i1.piimg.com/567571/885a7eb2b34c0342.png)

## 目录文件解析

![](http://i1.piimg.com/567571/9cb0b222c24e6400.png)

1. app/manifests AndroidManifest.xml配置文件目录
2. app/java 源码目录
3. app/res 资源文件目录
4. Gradle Scripts gradle编译相关的脚本

# Activity

Activity是一个应用程序组件，提供用户与程序交互的界面

### Activity创建

1. 继承Android的Activity类
2. 重写方法
3. 设置显示布局
4. 在AndroidManifest文件中，注册Activity

### Activity生命周期

[官方](https://developer.android.com/reference/android/app/Activity.html)文档给出的图如下：

![](http://p1.bpimg.com/567571/75a197c753928d46.png)

1. onCreate();创建 
2. onStart();运行 
3. onResume();获取焦点 
4. onPause(); 失去焦点
5. onStop();暂停 
6. onDestroy();销毁 
7. onRestart(); 重启

## Activity四种状态
1. Active/Running Activity处于界面顶端，获取焦点。
2. Paused Activity失去焦点，但是对用户可见。
3. Stopped Activity完全被遮挡，但保留所有的状态和成员信息。
4. Killed Activity被销毁

![](http://p1.bqimg.com/567571/2924ef5e1b85bbf1.png)