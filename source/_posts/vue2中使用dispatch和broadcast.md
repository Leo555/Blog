---
title: vue2 中使用 dispatch 和 broadcast
date: 2017-09-01 09:37:44
categories: Vue
tags: 
- Vue
- dispatch
- broadcast
---

最近在使用 Element 过程中发现组件通信大量使用 dispatch 和 broadcast 两个方法，之前在 [vue2 组件通信](https://lz5z.com/vue2%E7%BB%84%E4%BB%B6%E9%80%9A%E4%BF%A1/)也提到过 vue2 中取消了 $dispatch、$broadcast 两个重要的事件，而 Element 重新实现了这两个函数。

代码地址放在 [`element-ui/lib/mixins/emitter`](https://github.com/ElemeFE/element/blob/dev/src/mixins/emitter.js)

<!--more-->

**emitter.js**

```javascript
"use strict";

exports.__esModule = true;
function _broadcast(componentName, eventName, params) {
  this.$children.forEach(function (child) {
    var name = child.$options.componentName;

    if (name === componentName) {
      child.$emit.apply(child, [eventName].concat(params));
    } else {
      _broadcast.apply(child, [componentName, eventName].concat([params]));
    }
  });
}
exports.default = {
  methods: {
    dispatch: function dispatch(componentName, eventName, params) {
      var parent = this.$parent || this.$root;
      var name = parent.$options.componentName;

      while (parent && (!name || name !== componentName)) {
        parent = parent.$parent;

        if (parent) {
          name = parent.$options.componentName;
        }
      }
      if (parent) {
        parent.$emit.apply(parent, [eventName].concat(params));
      }
    },
    broadcast: function broadcast(componentName, eventName, params) {
      _broadcast.call(this, componentName, eventName, params);
    }
  }
};
```
### 解析

`dispatch` 和 `broadcast` 方法都需要 3 个参数，`componentName` 组件名称， `eventName` 事件名称， `params` 传递的参数。

`dispatch` 方法会寻找所有的父组件，直到找到名称为 `componentName` 的组件，调用其 `$emit()` 事件。`broadcast` 方法则是遍历当前组件的所有子组件，找到名称为 `componentName` 的子组件，然后调用其 `$emit()` 事件。

这里也看出了 Element 中的 `dispatch` 与 `broadcast` 的不同，vue1 中的 `$dispatch` 和 `$broadcast` 会将事件通知给所有的 父/子 组件，只要其监听了相关事件，都能够（能够，不是一定）触发；而 Element 则更像是定向爆破，指哪打哪，其实更符合我们日常的需求。

### 使用方式

兄弟组件之间的通信可以很好的诠释上述两个事件。假设父组件 App.vue 中引入了两个子组件 Hello.vue 和 Fuck.vue。

如果你的项目中巧合使用了 Element，那可以按照下面的方式将其引入进来，如果没有用 Element 也不用担心，复制上面的 `emitter.js`，通过 mixins 的方式引入即可。

在 **App.vue** 中监听 `message` 事件，收到事件后，通过 `broadcast` 传播给相关组件。

```html
<template>
  <div id="app">
    <hello></hello>
    <fuck></fuck>
  </div>
</template>

<script>
  import Hello from 'components/Hello'
  import Fuck from 'components/Fuck'
  import Emitter from 'element-ui/lib/mixins/emitter'

  export default {
    name: 'app',
    componentName: 'ROOT',
    mixins: [Emitter],
    components: {
      Hello,
      Fuck
    },
    created () {
      this.$on('message', params => {
        this.broadcast(params.componentName, params.eventName, params.text)
      })
    }
  }
</script>
```

**Fuck.vue** 与 **Hello.vue** 的内容基本相同，下面只列出 **Fuck.vue**

```javascript
import Emitter from 'element-ui/lib/mixins/emitter'
import event from 'mixins/event'

export default {
  componentName: 'Fuck',
  mixins: [Emitter, event],
  data () {
    return {
      name: 'Fuck',
      textarea: '',
      tableData: []
    }
  },
  methods: {
    submit () {
      this.communicate('message', {
        componentName: 'Hello',
        text: this.textarea
      })
      this.textarea = ''
    }
  },
  created () {
    this.$on('message', text => {
      this.tableData.push(this.getMessage(text))
    })
  }
}
```

**mixins/event.js**

```javascript
import Emitter from 'element-ui/lib/mixins/emitter'

export default {
  mixins: [Emitter],
  methods: {
    communicate (event, params = {}) {
      this.dispatch('ROOT', event, Object.assign({
        eventName: event
      }, params))
    }
  }
}
```

[完整代码地址](https://github.com/Leo555/vue_communication)

