/**
 * API 配置和認證相關 API
 *
 * 使用 HttpOnly Cookie 認證模式：
 * - withCredentials: true 讓瀏覽器自動發送 Cookie
 * - 前端無需手動管理 Token（由瀏覽器自動處理）
 * - 後端通過 Cookie 驗證身份
 */
import axios from 'axios'
import router from '../router'
import { API_CONFIG, ROUTES } from '../config/constants'
import { useToast } from '../composables/useToast'

// 創建 axios 實例
const api = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  withCredentials: true,  // 重要：允許跨域請求攜帶 Cookie
  headers: {
    'Content-Type': 'application/json'
  }
})

// 回應攔截器 - 處理 Token 過期和錯誤
api.interceptors.response.use(
  response => {
    return response
  },
  error => {
    // 處理 401 未授權錯誤（Token 過期或無效）
    if (error.response && error.response.status === 401) {
      // 只在不是登入/註冊頁面時才跳轉
      const currentPath = router.currentRoute.value.path
      if (currentPath !== ROUTES.LOGIN && currentPath !== ROUTES.REGISTER) {
        // 顯示提示訊息（使用 useToast 確保自動消失）
        const toast = useToast()
        toast.error('登入已過期，請重新登入')

        // 跳轉到登入頁
        router.push(ROUTES.LOGIN)
      }
    }

    return Promise.reject(error)
  }
)

// 認證相關 API
export const authAPI = {
  /**
   * 用戶註冊
   * @param {Object} userData - 用戶資料 { username, email, password }
   * @returns {Promise} 註冊結果
   */
  register(userData) {
    return api.post('/register', userData)
  },

  /**
   * 用戶登入
   * 後端會自動設置 HttpOnly Cookie
   * @param {Object} credentials - 登入憑證 { email, password }
   * @returns {Promise} 登入結果（返回用戶資料）
   */
  login(credentials) {
    return api.post('/login', credentials)
  },

  /**
   * 用戶登出
   * 後端會清除 HttpOnly Cookie
   * @returns {Promise} 登出結果
   */
  logout() {
    return api.post('/logout')
  }
}

// 導出 axios 實例供其他 API 模組使用
export default api
