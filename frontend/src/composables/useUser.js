/**
 * 用戶狀態管理 Composable
 *
 * HttpOnly Cookie 模式下的用戶狀態管理：
 * - 不使用 localStorage 存儲 Token（由 HttpOnly Cookie 處理）
 * - 使用單例模式，所有組件共享同一個用戶狀態
 * - 通過 API 調用獲取和更新用戶信息
 */
import { ref } from 'vue'
import { userAPI } from '../api/user'

// 全局共享狀態（單例模式）
const user = ref(null)
const loading = ref(false)
const error = ref(null)

export function useUser() {
  /**
   * 獲取當前用戶資訊
   */
  const fetchUserInfo = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await userAPI.getCurrentUser()
      user.value = response.data
      return response.data
    } catch (err) {
      error.value = err
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * 更新用戶資訊（本地）
   */
  const updateUser = (userData) => {
    user.value = { ...user.value, ...userData }
  }

  /**
   * 清除用戶資訊
   */
  const clearUser = () => {
    user.value = null
    error.value = null
  }

  return {
    user,
    loading,
    error,
    fetchUserInfo,
    updateUser,
    clearUser
  }
}
