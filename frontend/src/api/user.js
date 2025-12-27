import api from './auth'

export const userAPI = {
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
  }
}
