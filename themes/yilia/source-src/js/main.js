// 样式
import '../css/main.scss'
// 分享
import Share from './share'

import {addLoadEvent} from './util'

addLoadEvent(function() {
	Share.init()
})
