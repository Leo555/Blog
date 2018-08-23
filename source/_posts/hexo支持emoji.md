---
title: hexo 支持 emoji
date: 2017-07-05 16:24:06
categories: Blog
tags:
- Hexo
- emoji
---

### 添加方法

很简单，换一个 markdown 引擎，然后再增加 emoji 插件即可。:blush:

```shell
$ npm un hexo-renderer-marked --save
$ npm i hexo-renderer-markdown-it --save 
$ npm install markdown-it-emoji --save
```
据说 [hexo-renderer-markdown-it](https://github.com/hexojs/hexo-renderer-markdown-it) 的速度要比 Hexo 原装插件要快，而且功能更多：

<!--more-->

> Main Features
>- Support for [Markdown], [GFM] and [CommonMark]
>- Extensive configuration
>- Faster than the default renderer | `hexo-renderer-marked`
>- Safe ID for headings
>- Anchors for headings with ID
>- Footnotes
>- `<sub>` H<sub>2</sub>O
>- `<sup>` x<sup>2</sup>
>- `<ins>` <ins>Inserted</ins>


然后编辑 `_config.yml`：

```
markdown:
  plugins:
    - markdown-it-footnote
    - markdown-it-sup
    - markdown-it-sub
    - markdown-it-abbr
    - markdown-it-emoji
```

### 使用方法

1. 在 [Emoji](https://emoji.codes/) 中找到你想要的表情，然后点击即可复制。
2. 比如你想发一个笑脸 :smile: 直接输入笑脸对应的 emoji 编码 `:smile:` 就可以。


[CommonMark]: http://commonmark.org/
[Markdown]: http://daringfireball.net/projects/markdown/
[GFM]: https://help.github.com/articles/github-flavored-markdown/
[Markdown-it]: https://github.com/markdown-it/markdown-it
[Hexo]: http://hexo.io/