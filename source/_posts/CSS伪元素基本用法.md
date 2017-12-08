---
title: CSS 伪元素基本用法
date: 2017-12-08 18:06:19
categories: CSS
tags:
- CSS
- 伪元素
- before
- after
---

# 伪元素

CSS 中可以利用伪元素给 DOM 元素添加特殊的样式。比如说，我们可以通过 `:before` 在一个元素前增加一些文本，并为这些文本添加样式。虽然用户可以看到这些文本，但是这些文本实际上不在文档树中。

CSS3 规范中要求使用双冒号(::)添加伪元素，用以区分伪元素和伪类，比如 `::before` 是伪元素，`:hover` 是伪类。但是大部分伪元素依然支持单冒号的形式，`::before` 写成 `:before` 也可以，为了向后兼容，一般推荐使用单冒号的形式。

支持单双冒号的伪元素有： `:before/::before`，`:after/::after`，`:first-letter/::first-letter`，`:first-line/::first-line`。

仅支持双冒号的伪元素有： `::selection`，`::placeholder`，`::backdrop`。

<!-- more -->

## `:before` & `:after`

`:before` 和 `:after` 可以在元素前面或者后面插入内容，用 content 属性表示要插入的内容，这个虚拟元素默认是行内元素，可以配合其它样式使用。

html:

```html
<p> </p>
```

css:

```css
p:before {
  content: 'Hello';
  color: red;
}
p:after {
  content: 'World';
  color: black;
}
```

p 元素会显示 **Hello World**，但是被插入的内容实际上不在文档树中。


## `:first-letter`

`:first-letter` 用来获取元素中文本的首字母，被修饰的首字母不在文档树中。注意没有 `:last-letter`。

首行只在 block-container box 内部才有意义, 因此 `:first-letter` 伪元素 只在 display 属性值为 block, inline-block, table-cell, list-item 或者 table-caption 的元素上才起作用。 其他情况下 `:first-letter` 毫无意义。

`:first-letter` 的优先级低于 `:before`，也就是如果元素用 `:before` 先插入文本，会获取 before 伪元素中的内容。

html:

```html
<p>World</p>
```

css:

```css
p:before {
  content: 'Hello ';
}
p:first-letter {
  font-size: 40px;
  color: red;
}
```

这时，`:first-letter` 实际获取的元素是 `：before` 中的 **H**。

注意： 在一个使用了 `:first-letter` 伪元素的选择器中，只有很小的一部分 css 属性能被使用 [::first-letter](https://developer.mozilla.org/zh-CN/docs/Web/CSS/::first-letter)


## `:first-line`

`:first-line` 用来获取 **块状元素** 中的第一行文本，不能用于内联元素。

html:

```html
<h1>Hello</br>World</h1>
```

css:

```css
h1:first-line {
  background: orange;
}
```

在一个使用了 ::first-line 伪元素的选择器中，只有很小的一部分css属性能被使用 [::first-line](https://developer.mozilla.org/zh-CN/docs/Web/CSS/::first-line)

## `::selection`

`::selection` 伪元素应用于文档中被用户高亮的部分（比如使用鼠标或其他选择设备选中的部分），该伪元素只支持双冒号的形式。

只有 Gecko 引擎需要加前缀（-moz）

```css
::-moz-selection {
  background: orange;
}
 
::selection  {
  background: orange;
}
```


注意： 只有一小部分 CSS 属性可以用于 `::selection` 选择器： color, background-color, cursor, outline, text-decoration, text-emphasis-color 和 text-shadow。要特别注意的是，background-image 会如同其他属性一样被忽略。

## `::placeholder` (试验性质)

`:placeholder` 匹配占位符的文本，只有元素设置了 placeholder 属性时，该伪元素才能生效。在一些浏览器中（IE10 和 Firefox18 及其以下版本）会使用单冒号的形式。

```css
input::-moz-placeholder {
  color: #666;
}
 
input::-webkit-input-placeholder {
  color: #666;
}
 
/* IE 10 only */
input:-ms-input-placeholder {
  color: #666;
}
 
/* Firefox 18 and below */
input:-moz-input-placeholder {
  color: #666;
}
```

## `::backdrop` (试验性质)

用于改变全屏模式下背景色，全屏模式默认背景色为黑色。

```css
h1:fullscreen::backdrop {
  background: orange;
}
```

# 参考文章

- [MDN - Pseudo-elements](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Pseudo-elements)
- [summary-of-pseudo-classes-and-pseudo-elements/](http://www.alloyteam.com/2016/05/summary-of-pseudo-classes-and-pseudo-elements/)