import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI)

import App from './App.vue'
import router from './router/index.js'
import store from './store/index.js'
Vue.config.productionTip = false

import "./assets/css/global.less"

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
