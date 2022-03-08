import Vue from 'vue'
import VueRouter from 'vue-router'
Vue.use(VueRouter)
import Home from '../views/Home/Home.vue'
import Show from '../views/Show/Show.vue'


const routes = [
  {
    path:'/',
    redirect: '/Home',		
    component: Home
  },
  {
    path:'/Home',
    component: Home
  },
  {
    path: '/Show',
    component: Show,
    
  }
]

const router = new VueRouter({
  routes,
  mode: 'history'
})

export default router
