---
title: DOM 事件机制
date: 2016-12-25 17:44:44
categories: JavaScript
tags:
- DOM  
- 事件流
- JavaScript
- HTML
- 事件委托/代理
---

DOM 事件流（event  flow）存在三个阶段：事件捕获 --> 事件目标 --> 事件冒泡。

事件捕获：当事件发生时（onclick, onmouseover……），浏览器会从根节点开始由外到内进行事件传播，即点击了子元素，如果父元素通过事件捕获方式注册了对应的事件的话，会先触发父元素绑定的事件。（IE10 及以下浏览器不支持捕获型事件）

事件冒泡：与事件捕获恰恰相反，事件冒泡顺序是由内到外进行事件传播，直到根节点。
<!-- more -->
## 事件

(1) onlick -->事件冒泡，重写 onlick 会覆盖之前属性，没有兼容性问题。DOM0 级事件处理程序，每个元素都有自己的事件处理程序属性，这些属性通常全部小写，将这些属性的值全部设置为一个函数，就可以指定事件处理程序。

```javascript
// 解绑单击事件，将 o0nlick 属性设为 null 即可
el.onclik = null 
```

(2) addEventListener(event, listener, useCapture)  
参数定义：event---（事件名称，如 click，不带 on），listener---事件监听函数，useCapture---是否采用事件捕获进行事件捕捉，默认为 false，即采用事件冒泡方式。 IE8  及以下不支持，属于 DOM2 级的方法，**可添加多个方法不被覆盖**。

```javascript
// 事件类型没有 on，false 表示在事件第三阶段（冒泡）触发，true表示在事件第一阶段（捕获）触发。 如果handle是同一个方法，只执行一次。
ele.addEventListener('click', function(){ }, false) 
// 解绑事件，参数和绑定一样
ele.removeEventListener(event.type, handle, boolean)
```

(3) attachEvent(event.type, handle) IE 特有，兼容 IE8 及以下，可添加多个事件处理程序，与 DOM 方法不同的是，多个事件的执行顺序与添加顺序相反，attachEvent 只支持冒泡阶段。

```javascript
// 如果 handle 是同一个方法，绑定几次执行几次，这点和 addEventListener 不同,事件类型要加 on, 例如 onclick 而不是 click
ele.attachEvent('onclick', function(){ })
// 解绑事件，参数和绑定一样
ele.detachEvent('onclick', function(){ })
```

使用 attachEvent() 添加的事件可以通过 detachEvent() 来移除，条件是必须提供相同的参数，与 DOM 方法一样，这也意味着添加的匿名函数不能被移除。

(4) 默认事件行为：href=''，submit表单提交等

* return false 阻止独享属性（通过on这种方式）绑定的事件的默认事件

```javascript
ele.onclick = function() {
  ……             // 你的代码
  return false   // 通过返回false值阻止默认事件行为
}
```

* event.preventDefault() 阻止通过 addEventListener() 添加的事件的默认事件

```javascript
element.addEventListener('click', function(e) {
  let event = e || window.event
  ……
  event.preventDefault()    // 阻止默认事件
},false)
```

* event.returnValue = false 阻止通过 attachEvent() 添加的事件的默认事件

```javascript
element.attachEvent("onclick", function(e) {
  let event = e || window.event
  ……
  event.returnValue = false     // 阻止默认事件
})
```

## DOM 中的事件对象 

| 属性/方法 | 类型 | 读写 | 说明 |
| :-| :-| :-| :-|
| Event.bubbles | Boolean | 只读 | 表示该事件是否在 DOM 中冒泡 |
| Event.cancelable | Boolean | 只读 | 表示这个事件是否可以取消 |
| Event.currentTarget | Element | 只读 | 当前注册事件的对象的引用，当前事件需要传递到的对象 |
| Event.defaultPrevented | Boolean | 只读 | 表示了是否已经执行过了 event.preventDefault() |
| Event.eventPhase  | Integer | 只读 | 指示事件流正在处理哪个阶段: 1.捕获 2.目标 3. 冒泡 |
| Event.target  | Element | 只读 | 对事件起源目标的引用 |
| Event.timeStamp  | Number | 只读 | 事件创建时的时间戳，毫秒级别 |
| Event.type  | String | 只读 | 事件的类型（'click'） |
| event.preventDefault  | Function | 只读 | 取消事件的默认行为，如果 cancelable 是 true，则可以使用这个方法 |
| event.stopImmediatePropagation  | Function | 只读 | 取消事件的进一步捕获或者冒泡，同时阻止任何事件处理程序被调用（DOM3） |
| event.stopPropagation  | Function | 只读 | 取消事件的默认行为，如果 bubbles 是 true，则可以使用这个方法 |

### target vs currnetTarget

在事件处理程序的内部，对象的 this 始终等于 currentTarget 的值，而 target 则只包含事件的实际目标。如果直接将事件处理程序指定给了目标元素，则 this， currentTarget 和 target 包含相同的值。

```javascript
var btn = document.getElementById('myBtn')
btn.onclick = function (e) {
  e.currentTarget === this // true
  e.target === this // true
}
```
由于 click 事件的目标是按钮，因此这三个值是相等的，但如果事件处理程序存在于按钮的父节点中，结果就不一样了。

```javascript
document.body.onclick = function (e) {
  e.target === document.getElementById('myBtn') // true
  e.currentTarget === document.body // true
  this === document.body // true
}
```
单击这个按钮时，this 和 currentTarget 都等于 document.body，因为事件处理程序是注册到这个元素上的。然而 target 元素却等于按钮元素，因为它是 click 事件的真正目标。


## IE 事件对象

访问 IE 中的 event 对象时，如果使用 DOM0 级方法添加事件处理程序，event 对象作为 window 对象的一个属性存在。使用 attachEvent() 添加事件处理程序时，event 会作为参数传入，也可以从 window 对象中访问 event 对象，就像 DOM0 级方法一样。

```javascript
// onclick
var btn = document.getElementById('myBtn')
btn.onclick = function () {
  var event = window.event
  alert(event.type) // 'click'
}
// attachEvent
var btn = document.getElementById('myBtn')
btn.attachEvent('onclick', function (event) {
  alert(event.type) // 'click'
})
```

| 属性/方法 | 类型 | 读写 | 说明 |
| :-| :-| :-| :-|
| Event.cancelable | Boolean | 读/写 | 默认为 false，但将其设置为 true 就可以取消事件冒泡（与 DOM0 级的 stopPropagation()方法的作用相同） |
| Event.returnValue | Boolean | 读/写 | 默认为 false，但将其设置为 true 就可以取消事件的默认行为（与 DOM 中的 preventDefault()方法的作用相同） |
| Event.srcElement | Element | 只读 | 事件的目标（DOM 中的 target） |
| Event.type | String | 只读 | 事件的类型 |

事件处理程序的作用域是根据指定它的方式来确定的，所以其 this 也会有所不同，比较好的办法是用 event.srcElement。

```javascript
var btn = document.getElementById('myBtn')
btn.onclick = function () {
  window.event.srcElement === this // true
}
btn.attachEvent('onclick', function(event) {
  event.srcElement === this // false
})
```

IE 事件中的 returnValue 相当于 DOM 中的 preventDefault() 方法，它们的作用都是取消事件的默认行为，不过这里不能确定事件的默认行为是否已经被取消。

cancelBubble 属性与 DOM 中的 stopPropagation() 方法作用相同，用来阻止事件冒泡，由于 IE 不支持事件捕获，因此只能阻止事件冒泡，而 stopPropagation() 同时可以取消事件冒泡和捕获。

```javascript
var btn = document.getElementById('myBtn')
btn.onclick = function () {
  window.event.returnValue = false // 阻止默认事件
  window.event.cancelBubble = true // 阻止事件冒泡
}
```


## 事件封装

JavaScript 中实现事件绑定主要使用两个方法： [addEventListener](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener)、[attachEvent](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/attachEvent)。

为了兼容浏览器，按照网上通用的方案对事件进行封装

```javascript
// 事件绑定
function addEvent(element, eType, handle, bol) {
 if (element.addEventListener) {       // 如果支持addEventListener
   element.addEventListener(eType, handle, bol)
 } else if (element.attachEvent) {      // 如果支持attachEvent
   element.attachEvent('on' + eType, handle)
 } else {                  // 否则使用兼容的onclick绑定
   element['on' + eType] = handle
 }
}
```

```javascript
// 事件解绑
function removeEvent(element, eType, handle, bol) {
 if (element.addEventListener) {
   element.removeEventListener(eType, handle, bol)
 } else if (element.attachEvent) {
   element.detachEvent('on' + eType, handle)
 } else {
   element['on' + eType] = null
 }
}
```

## 阻止事件冒泡、事件捕获

```javascript
// 阻止默认事件
function preventDefault (event) {
  if (event.preventDefault) {
    event.preventDefault()
  } else {
    event.returnValue = false
  }
}
// 阻止事件进一步传播
function stopPropagation (event) {
  if (event.stopPropagation) {
    event.stopPropagation() // 阻止事件的进一步传播，包括（冒泡，捕获），无参数
  } else {
    event.cancelBubble = true // true 为阻止冒泡
  }
} 
// 获取事件目标
function getTarget (event) {
  return event.target || event.srcElement
}
```

## 事件流

### 事件冒泡

HTML内容：

```html
<body>
  <div id="parent">
    父元素
    <div id="child">
      子元素
    </div>
  </div>
</body>
```

css

```css
#parent{
  width: 200px;
  height:200px;
  text-align: center;
  line-height: 3;
  background: green;
}
#child{
  width: 100px;
  height: 100px;
  margin: 0 auto;
  background: orange;
}
```

JavaScript

```javascript
let parent = document.getElementById('parent')
let child = document.getElementById('child')

document.body.addEventListener('click', function(e) {
  console.log('click-body')
}, false)

parent.addEventListener('click', function(e) {
  console.log('click-parent')
}, false)

child.addEventListener('click', function(e) {
  console.log('click-child')
}, false)
```

通过 'addEventListener' 方法，采用事件冒泡方式给 DOM 元素注册 click 事件，点击“子元素”，控制台依次输出 “click-child” --> “click-parent” --> “click-body”。

事件触发顺序是由内到外的，这就是事件冒泡，虽然只点击子元素，但是它的父元素也会触发相应的事件。

{% raw %}
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>DOM 事件</title>
  <style>
    #parent{
      width: 200px;
      height:200px;
      text-align: center;
      line-height: 3;
      background: green;
    }
    #child{
      width: 100px;
      height: 100px;
      margin: 0 auto;
      background: orange;
    }
  </style>
</head>
<body>
  <div id="parent">
    父元素
    <div id="child">
      子元素
    </div>
  </div>
  <script type="text/javascript">
    let parent = document.getElementById('parent')
    let child = document.getElementById('child')
  
    document.body.addEventListener('click', function(e) {
      console.log('click-body')
    }, false)
    
    parent.addEventListener('click', function(e) {
      console.log('click-parent')
    }, false)

    child.addEventListener('click', function(e) {
      console.log('click-child')
    }, false)
  </script>
</body>
</html>
{% endraw %}（F12 打开控制台，点击查看效果）

如果点击子元素不想触发父元素的事件怎么办？
那就是停止事件传播---event.stopPropagation()

```javascript
child.addEventListener('click', function(e){
  console.log('click-child')
  　e.stopPropagation()
}, false)
```

{% raw %}
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>DOM 事件</title>
  <style>
    #parent2{
      width: 200px;
      height:200px;
      text-align: center;
      line-height: 3;
      background: green;
    }
    #child2{
      width: 100px;
      height: 100px;
      margin: 0 auto;
      background: orange;
    }
  </style>
</head>
<body>
  <div id="parent2">
    父元素
    <div id="child2">
      子元素
    </div>
  </div>
  <script type="text/javascript">
    let parent2 = document.getElementById('parent2')
    let child2 = document.getElementById('child2')
    
    parent2.addEventListener('click', function(e) {
      console.log('click-parent')
    }, false)

    child2.addEventListener('click', function(e) {
      console.log('click-child')
      e.stopPropagation()
    }, false)
  </script>
</body>
</html>
{% endraw %}（F12 打开控制台，点击查看效果）

### 事件捕获

修改上面事件冒泡的例子

```javascript
let parent = document.getElementById('parent')
let child = document.getElementById('child')

parent.addEventListener('click', function(e) {
  console.log('click-parent---事件传播')
}, false)
// 新增事件捕获
parent.addEventListener('click', function(e) {
  console.log('click-parent--事件捕获')
}, true)

child.addEventListener('click', function(e) {
  console.log('click-child')
}, false)
```

{% raw %}
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>DOM 事件</title>
  <style>
    #parent3{
      width: 200px;
      height:200px;
      text-align: center;
      line-height: 3;
      background: green;
    }
    #child3{
      width: 100px;
      height: 100px;
      margin: 0 auto;
      background: orange;
    }
  </style>
</head>
<body>
  <div id="parent3">
    父元素
    <div id="child3">
      子元素
    </div>
  </div>
  <script type="text/javascript">
    let parent3 = document.getElementById('parent3')
    let child3 = document.getElementById('child3')

    parent3.addEventListener('click', function(e) {
      console.log('click-parent---事件传播')
    }, false)        
    // 新增事件捕获
    parent3.addEventListener('click', function(e) {
      console.log('click-parent--事件捕获')
    }, true)

    child3.addEventListener('click', function(e) {
      console.log('click-child')
    }, false)
  </script>
</body>
</html>
{% endraw %}（F12 打开控制台，点击查看效果）

父元素通过事件捕获的方式注册了 click 事件，所以在事件捕获阶段就会触发，然后到了目标阶段，即事件源，之后进行事件传播，parent 同时也用冒泡方式注册了 click 事件，所以这里会触发冒泡事件，最后到根节点。这就是整个事件流程。

### 事件委托

事件委托(事件代理)：利用事件冒泡的特性，将里层的事件委托给外层事件，根据 event 对象的属性进行事件委托，改善性能。
使用事件委托能够避免对特定的每个节点添加事件监听器；事件监听器是被添加到它们的父元素上。事件监听器会分析从子元素冒泡上来的事件，找到是哪个子元素的事件。

委托在 JQuery 中已经得到了实现，即通过 **$(selector).on(event,childSelector,data,function,map)** 实现委托，一般用于动态生成的元素，当然 JQuery 也是通过原生的 js 去实现的，下面举一个简单的栗子，如果要单独点击 table 里面的 td，普通做法是 for 循环给每个 td 绑定事件，td 少的话性能什么差别，td 如果多了，就不行了，我们使用事件委托:

HTML

```html
<table id="outside" border="1" style="cursor: pointer;">
<tr>
  <td>table01</td>
  <td>table02</td>
  <td>table03</td>
  <td>table04</td>
  <td>table05</td>
  <td>table06</td>
  <td>table07</td>
  <td>table08</td>
  <td>table09</td>
  <td>table10</td>
</tr>
</table>
```

JavaScript

```javascript
let out = document.getElementById('outside')
if (out.addEventListener) {
  out.addEventListener('click', function(e) {
    e = e || window.event
    // IE没有e.target，有e.srcElement
    let target = e.target || e.srcElement
    // 判断事件目标是否是td，是的话target即为目标节点td
    if (target.tagName.toLowerCase() == 'td') {
      changeStyle(target)
      console.log(target.innerHTML)
    }
  }, false)
} else {
  out.attachEvent('onclick', function(e) {
    e = e || window.event
    // IE没有e.target，有e.srcElement
    let target = e.target || e.srcElement
    // 判断事件目标是否是td，是的话target即为目标节点td
    if (target.tagName.toLowerCase() == 'td') {
      changeStyle(target)
      console.log(target.innerHTML)
    }
  })
}

function changeStyle(ele) {
  ele.innerHTML = '已点击'
  ele.style.background = '#900'
  ele.style.color = '#fff'
}
```

{% raw %}
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>DOM 事件</title>
</head>
<body>
  <table id="outside" border="1" style="cursor: pointer;">
  <tr>
    <td>table01</td>
    <td>table02</td>
    <td>table03</td>
    <td>table04</td>
    <td>table05</td>
    <td>table06</td>
    <td>table07</td>
    <td>table08</td>
    <td>table09</td>
    <td>table10</td>
  </tr>
  </table>
  <script type="text/javascript">
    let out = document.getElementById('outside')
    if (out.addEventListener) {
      out.addEventListener('click', function(e) {
        e = e || window.event
          // IE 没有 e.target，有 e.srcElement
        let target = e.target || e.srcElement
          // 判断事件目标是否是td，是的话 target 即为目标节点 td
        if (target.tagName.toLowerCase() == 'td') {
          changeStyle(target)
          console.log(target.innerHTML)
        }
      }, false)
    } else {
      out.attachEvent('onclick', function(e) {
        e = e || window.event
          // IE 没有 e.target，有 e.srcElement
        let target = e.target || e.srcElement
          // 判断事件目标是否是 td，是的话 target 即为目标节点 td
        if (target.tagName.toLowerCase() == 'td') {
          changeStyle(target)
          console.log(target.innerHTML)
        }
      })
    }

    function changeStyle(ele) {
      ele.innerHTML = '已点击'
      ele.style.background = '#900'
      ele.style.color = '#fff'
    }
  </script>
</body>
</html>
{% endraw %}（点击查看效果）


## 总结

事件的三个阶段分别为：捕获，目标和冒泡，低版本 IE 不支持捕获。绑定事件的方法为 **addEventListener** 和 **attachEvent**。addEventListener 方法的第三个 boolean 型参数表示添加的事件为捕获或者冒泡，true 代表捕获，false 代表冒泡。

事件冒泡的优点为： 
1. 可以大量节省内存占用，减少事件注册，比如在 table 上代理所有 td 的 click 事件。
2. 可以实现为动态增加的 DOM 绑定事件的功能。