/**
 * 路由配置
 *
 * HttpOnly Cookie 認證模式下的路由策略：
 * - 前端無法訪問 Cookie，因此無法在路由層檢查認證狀態
 * - 所有路由都允許訪問，依賴後端 API 的 401 錯誤來處理未認證情況
 * - 當受保護的頁面加載時，會調用 API 獲取數據
 * - 如果 Cookie 無效，後端返回 401，前端攔截器會自動跳轉到登入頁
 */
import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../layouts/MainLayout.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import Account from '../views/Account.vue'
import Admin from '../views/Admin.vue'
import AuditLogs from '../views/AuditLogs.vue'

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
        meta: { requiresAuth: true }  // 標記需要認證（僅用於文檔說明）
      },
      {
        path: 'account',
        name: 'Account',
        component: Account,
        meta: { requiresAuth: true }
      },
      {
        path: 'admin',
        name: 'Admin',
        component: Admin,
        meta: { requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'audit-logs',
        name: 'AuditLogs',
        component: AuditLogs,
        meta: { requiresAuth: true, requiresAdmin: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守衛（簡化版）
// 使用 HttpOnly Cookie 後，前端無法直接檢查認證狀態
// 認證檢查完全依賴後端 API，如果 Cookie 無效會收到 401 錯誤
// response interceptor 會自動處理 401 並跳轉到登入頁
router.beforeEach((to, from, next) => {
  // 允許所有路由導航
  // 受保護的頁面會在組件加載時調用 API
  // 如果未認證，後端會返回 401，前端攔截器會自動跳轉
  next()
})

export default router
