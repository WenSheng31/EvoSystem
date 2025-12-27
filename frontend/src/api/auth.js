import axios from 'axios'
import router from '../router'
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
      localStorage.removeItem('userRole') // 也清除角色資訊

      // 只在不是登入/註冊頁面時才跳轉
      const currentPath = router.currentRoute.value.path
      if (currentPath !== ROUTES.LOGIN && currentPath !== ROUTES.REGISTER) {
        router.push(ROUTES.LOGIN)
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
  }
}

export default api
