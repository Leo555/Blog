---
title: JavaScript 常见的内存泄漏
date: 2018-04-23 22:07:24
categories: JavaScript
tags:
- JavaScript
- 内存泄漏
- Memory Leaks
---

## 什么是内存泄漏

JavaScript 是一种垃圾回收语言，垃圾回收语言通过周期性地检查之前被分配的内存是否可以从应用的其它部分访问来帮助开发者管理内存。内存泄露是指当一块内存不再被应用程序使用的时候，由于某种原因，这块内存没有返还给操作系统或者内存池的现象。内存泄漏可能会导致应用程序卡顿或者崩溃。

<!--more-->

### 查看内存泄漏

在 chrome 中可以通过 performance 中的 Memory record 来查看，选中 Memory 后点击左边的 Record，然后模拟用户的操作，一段时间后点击 stop，在面板上查看这段时间的内存占用情况。如果内存基本平稳，则无内存泄漏情况；如果内存占用不断飙升，内可能出现内存泄漏的情况。

在 Node 环境中，可以输入 `process.memoryUsage()` 查看 Node 进程的内存占用情况。

- rss（resident set size）：进程的常驻内存部分。
- heapTotal："堆"占用的内存，包括用到的和没用到的。
- heapUsed：用到的堆的部分。
- external： V8 引擎内部的 C++ 对象占用的内存。

判断内存泄漏，以 heapUsed 字段为准。

## 常见的内存泄漏


