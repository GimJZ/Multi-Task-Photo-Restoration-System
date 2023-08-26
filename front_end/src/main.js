import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import utils from './utils'
import 'amfe-flexible'
//初始化样式
import './common/stylus/index.styl'
Vue.config.productionTip = false


import { Button } from 'vant';
import { Tab, Tabs } from 'vant';
import { Popup } from 'vant';
import { Cell, CellGroup } from 'vant';
import { Empty } from 'vant';
import { Loading } from 'vant';
import { Overlay } from 'vant';
import { Field } from 'vant';

Vue.use(Field);
Vue.use(utils)
Vue.use(Overlay);
Vue.use(Loading);
Vue.use(Empty);
Vue.use(Cell);
Vue.use(CellGroup);
Vue.use(Popup);
Vue.use(Tab);
Vue.use(Tabs);
Vue.use(Button)
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
