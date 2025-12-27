import { ref } from 'vue'
import { userAPI } from '../api/user'

/**
 * 用戶狀態管理 Composable
 */
export function useUser() {
  const user = ref(null)
  const loading = ref(false)
  const error = ref(null)

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
