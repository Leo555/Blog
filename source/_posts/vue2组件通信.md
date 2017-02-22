---
title: vue2.0 组件通信
date: 2017-02-17 10:46:29
categories: Vue
tags: 
- JavaScript
- Vue
- Vuex
---

Vue 采用基于组件的开发方式，那么组件之间的通信必不可少：比如父组件要给子组件传递数据，子组件将它内部发生的事情告知给父组件，因此定义一个良好的接口尽可能将组件解耦显得尤为重要，这保证不同的组件可以在相对独立的环境中开发测试，而且更方便阅读理解以及组件复用。

Vue 父子组件之间通信主要采取两种方式，通常可以总结为 **props down**、**events up**，父组件通过 props 向下传递数据给子组件，子组件通过 events 给父组件发送消息，这点跟 React 一模一样。

Vue2.0 废除了 `events`、`$dispatch`、`$broadcast` 几个事件，官方推荐使用 [全局事件驱动 或者 vuex](https://github.com/vuejs/vue/issues/2873)代替，目前只剩下 `vm.$on`、`vm.$once`、`vm.$off`、`vm.$emit` 几个事件。
<!-- more -->

## props down

Vue 组件之间的作用域是相互隔离的，父组件向子组件传值只能通过 props 的方式，子组件不能直接调用父组件的数据。在子组件中，如果需要调用父组件传来的参数，必须显式的声明 props。

```javascript
Vue.component('child', {
  props: ['message'],
  template: '<span>{{ message }}</span>'sssss	
})
```
父组件向子组件传值

```html
<child message="hello!"></child>
```
### 单向数据流

props 传递值只能父组件向子组件传递，不能反回来，每当父组件更新时，子组件中的 props 会自动更新。如果在子组件中更改 props，Vue 控制台会给出 warning。因此如果需要在子组件中更改 props 通常会把其作为初始值赋值给某个变量，然后变量的值，或者在计算属性中定义一个基于 props 的值。

## events up

如果子组件需要把信息传达给父组件，可以使用 `v-on` 绑定自定义事件

```html
<div id="counter-event-example">
  <p>{{ total }}</p>
  <button-counter v-on:increment="incrementTotal"></button-counter>
  <button-counter v-on:increment="incrementTotal"></button-counter>
</div>
```
我们给 button-counter 绑定了一个自定义事件 `increment`，v-on 绑定事件还可以简写为 `@increment=""`。

```javascript
Vue.component('button-counter', {
  template: '<button v-on:click="increment">{{ counter }}</button>',
  data: function () {
    return {
      counter: 0
    }
  },
  methods: {
    increment() {
      this.counter += 1
      this.$emit('increment')
    }
  },
})
new Vue({
  el: '#counter-event-example',
  data: {
    total: 0
  },
  methods: {
    incrementTotal() {
      this.total += 1
    }
  }
})
```
button-counter 组件的模板中包含一个 button，其 click 事件会触发($emit)自定义事件 `increment`，因此每次在子组件中点击一次 button，父组件中都会调用 incrementTotal() 方法。

## 非父子组件通信

上面讲的两种方法都父子组件之间的通信，有时候非父子关系的组件也需要通信。在 Vue1.0 时代，可以通过 $dispatch 和 $broadcast 来解决，首先 dispatch 到根组件，然后再 broadcast 到子组件。Vue2.0 中官方推荐用 event bus 或者 vuex 解决，event bus 的本质是一个发布者订阅者模式。

（1）使用一个空的 Vue 实例作为中央事件总线
	`var bus = new Vue()`
（2）触发组件 A 中的事件(发布消息)
	`bus.$emit('id-selected', 1)`
（3）在组件 B 创建的钩子中监听事件（订阅消息）
	`bus.$on('id-selected', function (id) {})`
 
 下面是 [stackoverflow](http://stackoverflow.com/questions/38064054/vue-js-global-event-bus) 上面的一个例子

```html
<div id="example">
    <Display></Display>
    <Increment></Increment>
</div>
```

```javascript
var bus = new Vue()

Vue.component('Increment', {
  template: `<button @click="increment">+</button>`,
  data: function() {
   return {count: 1}
  },
  methods: {
    increment: function(){
      var increment = this.count++
      bus.$emit('inc', increment)
  }
 }
})

Vue.component('Display', {
  template: `<h3>Clicked: {{count}} times</h3>`,
  data: function(){
  return {count: 0}
  },
 created: function(){
   bus.$on('inc', function(num){
     this.count = num
   }.bind(this))
 }
})

new Vue({
 el: "#example",
})
```

## 全局状态管理 [Vuex](https://vuex.vuejs.org)

Vuex 是 Vue 组件的一个状态管理器，相当于一个只为 Vue 服务的 [Redux](http://redux.js.org/)。下面一个图能很好的反映出 Vuex 是如何让组件之间通信的。

<img src="/assets/img/vuex.png" alt="vuex" width="50%">

下面是 Vuex 官网上给出的一个 [计数器的例子](https://jsfiddle.net/n9jmu5v7/341/)

```html
<div id="app">
  <p>{{ count }}</p>
  <p>
    <button @click="increment">+</button>
    <button @click="decrement">-</button>
  </p>
</div>
```

```javascript
const store = new Vuex.Store({
  state: {
    count: 0
  },
  mutations: {
    increment: state => state.count++,
    decrement: state => state.count--
  }
})

const app = new Vue({
  el: '#app',
  computed: {
    count() {
      return store.state.count
    }
  },
  methods: {
    increment() {
      store.commit('increment')
    },
    decrement() {
      store.commit('decrement')
    }
  }
})
```

点击查看效果
{% raw %}
<!DOCTYPE html>
<html lang="en">
<body>
<div id="app">
  <p>{{ count }}</p>
  <p>
    <button @click="increment">+</button>
    <button @click="decrement">-</button>
  </p>
</div>
</body>
<script src="https://unpkg.com/vue/dist/vue.js"></script>
<script src="https://unpkg.com/vuex@2.0.0"></script>
<script type="text/javascript">
const store = new Vuex.Store({
  state: {
    count: 0
  },
  mutations: {
    increment: state => state.count++,
    decrement: state => state.count--
  }
})

const app = new Vue({
  el: '#app',
  computed: {
    count() {
      return store.state.count
    }
  },
  methods: {
    increment() {
      store.commit('increment')
    },
    decrement() {
      store.commit('decrement')
    }
  }
})
</script>
</html>
{% endraw %}

在 Vuex 中，store 是组件状态的一个容器，上面的 store 中定义了一个初始的 state 对象，和两个 mutations 函数。我们可以通过 store.state 来获取状态对象，以及通过 store.commit 方法触发状态变更。要注意的是，我们不能直接更改 store 中的状态，改变 store 中的状态的唯一途径就是显式地提交(commit) mutations。

## 总结

1. 父组件向子组件传递信息使用 props down
2. 子组件向父组件传递信息使用 event up
3. 其它关系类型组件通信使用 global event bus
4. 大型 SPA 组件之间通信使用 Vuex 管理组件状态