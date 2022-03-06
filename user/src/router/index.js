import Vue from 'vue'
import VueRouter from 'vue-router'
Vue.use(VueRouter)
import Home from '../views/Home/Home.vue'

const routes = [
  {
    path:'/',
    redirect: '/Home',		
    component: Home
  },
]

const router = new VueRouter({
  routes,
  mode: 'history'
})

export default router
