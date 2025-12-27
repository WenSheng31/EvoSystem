/**
 * 前端常量配置
 */

// 導航延遲時間（毫秒）
export const NAVIGATION_DELAYS = {
  LOGIN_SUCCESS: 500,
  REGISTER_SUCCESS: 2000,
  DEFAULT: 1000
}

// Toast 提示持續時間（毫秒）
export const TOAST_DURATION = {
  DEFAULT: 3000,
  SHORT: 2000,
  LONG: 5000
}

// 路由路徑
export const ROUTES = {
  HOME: '/home',
  LOGIN: '/login',
  REGISTER: '/register',
  ACCOUNT: '/account',
  ADMIN: '/admin',
  TODOS: '/todos'
}

// 文件上傳限制
export const FILE_UPLOAD = {
  MAX_SIZE: 5 * 1024 * 1024, // 5MB
  ALLOWED_IMAGE_TYPES: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
  ALLOWED_EXTENSIONS: ['.jpg', '.jpeg', '.png', '.gif', '.webp']
}

// API 配置
export const API_CONFIG = {
  BASE_URL: '/api',
  TIMEOUT: 30000 // 30 秒
}
