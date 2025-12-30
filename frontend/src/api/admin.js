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
  },

  // 獲取審計日誌（分頁 + 篩選）
  getAuditLogs(page = 1, pageSize = 20, action = null) {
    const params = { page, page_size: pageSize }
    if (action) {
      params.action = action
    }
    return api.get('/admin/audit-logs', { params })
  }
}
