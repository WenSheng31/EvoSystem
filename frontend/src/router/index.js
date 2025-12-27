import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../layouts/MainLayout.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import Account from '../views/Account.vue'
import Admin from '../views/Admin.vue'
import Test from '../views/Test.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: 'home',
        name: 'Home',
        component: Home,
        meta: { requiresAuth: true }
      },
      {
        path: 'account',
        name: 'Account',
        component: Account,
        meta: { requiresAuth: true }
      },
      {
        path: 'test',
        name: 'Test',
        component: Test,
        meta: { requiresAuth: true }
      },
      {
        path: 'admin',
        name: 'Admin',
        component: Admin,
        meta: { requiresAuth: true, requiresAdmin: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守衛
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const userRole = localStorage.getItem('userRole')

  // 檢查是否需要登入
  if (to.meta.requiresAuth && !token) {
    next('/login')
    return
  }

  // 檢查是否需要管理員權限
  if (to.meta.requiresAdmin && userRole !== 'admin') {
    next('/home')
    return
  }

  // 已登入用戶訪問登入/註冊頁
  if ((to.path === '/login' || to.path === '/register') && token) {
    next('/home')
    return
  }

  next()
})

export default router
