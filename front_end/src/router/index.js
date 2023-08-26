import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/home.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: {
      title: '首页',
      isMenu: true
    }
  },
  {
    path: '/me',
    name: 'Me',
    component: () => import('../views/me.vue'),
    meta: {
      title: '我的',
      isMenu: true
    }
  },
  {
    path: '/',
    name: 'LogIn',
    component: () => import('../views/log_in.vue'),
    meta: {
      title: '登录',
      isMenu: false
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
