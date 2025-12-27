import api from './auth'

export const adminAPI = {
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
  },

  // 重置用戶密碼
  resetUserPassword(userId, newPassword) {
    return api.patch(`/admin/users/${userId}/reset-password`, {
      new_password: newPassword
    })
  }
}
