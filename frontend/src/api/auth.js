import axios from 'axios'
import { API_CONFIG, ROUTES } from '../config/constants'

const api = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 請求攔截器
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 回應攔截器 - 處理 token 過期
api.interceptors.response.use(
  response => {
    return response
  },
  error => {
    // 處理 401 未授權錯誤（token 過期或無效）
    if (error.response && error.response.status === 401) {
      // 清除無效 token
      localStorage.removeItem('token')

      // 只在不是登入/註冊頁面時才跳轉
      const currentPath = window.location.pathname
      if (currentPath !== ROUTES.LOGIN && currentPath !== ROUTES.REGISTER) {
        window.location.href = ROUTES.LOGIN
      }
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  // 用戶註冊
  register(userData) {
    return api.post('/register', userData)
  },

  // 用戶登入
  login(credentials) {
    return api.post('/login', credentials)
  },

  // 獲取當前用戶
  getCurrentUser() {
    return api.get('/me')
  },

  // 更新用戶資料
  updateProfile(data) {
    return api.patch('/me', data)
  },

  // 上傳頭像
  uploadAvatar(file) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // === 管理員 API ===

  // 獲取所有用戶
  getAllUsers() {
    return api.get('/admin/users')
  },

  // 啟用/停用用戶
  toggleUserActive(userId) {
    return api.patch(`/admin/users/${userId}/toggle-active`)
  },

  // 刪除用戶
  deleteUser(userId) {
    return api.delete(`/admin/users/${userId}`)
  }
}

export default api
