<template>
  <div class="min-h-screen bg-gray-50">
    <Header :user="user" />
    <main class="max-w-2xl mx-auto px-6 py-8">
      <h1 class="text-2xl font-semibold text-gray-900 mb-6">帳號管理</h1>

      <!-- 頭像上傳 -->
      <div class="bg-white p-6 rounded mb-6">
        <h2 class="text-base font-medium text-gray-900 mb-4">大頭貼</h2>
        <div class="flex items-center gap-6">
          <div class="w-20 h-20 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden">
            <img
              v-if="user?.avatar"
              :src="getAvatarUrl(user.avatar)"
              alt="Avatar"
              class="w-full h-full object-cover"
            />
            <span v-else class="text-gray-600 font-medium text-xl">
              {{ user?.username.charAt(0).toUpperCase() }}
            </span>
          </div>
          <div>
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              class="hidden"
              @change="handleAvatarUpload"
            />
            <button
              @click="$refs.fileInput.click()"
              class="px-4 py-2 text-sm text-gray-700 border border-gray-300 rounded hover:bg-gray-50"
            >
              上傳新頭像
            </button>
            <p class="text-xs text-gray-500 mt-2">支援 JPG, PNG, GIF（最大 5MB）</p>
          </div>
        </div>
      </div>

      <!-- 帳號資訊 -->
      <div class="bg-white p-6 rounded">
        <h2 class="text-base font-medium text-gray-900 mb-4">帳號資訊</h2>
        <form @submit.prevent="handleUpdateProfile" class="space-y-4">
          <div>
            <label class="block mb-1.5 text-gray-700 text-sm font-medium">用戶名</label>
            <input
              v-model="formData.username"
              type="text"
              class="w-full px-3 py-2.5 border border-gray-300 rounded text-sm focus:outline-none focus:border-gray-900"
            />
          </div>

          <div>
            <label class="block mb-1.5 text-gray-700 text-sm font-medium">電子郵件</label>
            <input
              v-model="formData.email"
              type="email"
              class="w-full px-3 py-2.5 border border-gray-300 rounded text-sm focus:outline-none focus:border-gray-900"
            />
          </div>

          <div class="mt-6">
            <button
              type="submit"
              class="px-4 py-2 bg-gray-900 text-white rounded text-sm font-medium hover:bg-gray-800"
            >
              儲存變更
            </button>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../api/auth'
import { useToast } from '../composables/useToast'
import axios from 'axios'
import Header from '../components/Header.vue'
import { getAvatarUrl } from '../utils/avatar'
import { API_BASE_URL } from '../utils/config'

export default {
  name: 'Account',
  components: {
    Header
  },
  setup() {
    const router = useRouter()
    const toast = useToast()
    const user = ref(null)
    const fileInput = ref(null)
    const formData = ref({
      username: '',
      email: ''
    })

    const fetchUserInfo = async () => {
      try {
        const response = await authAPI.getCurrentUser()
        user.value = response.data
        formData.value.username = response.data.username
        formData.value.email = response.data.email
      } catch (err) {
        console.error('獲取用戶資訊失敗:', err)
        router.push('/login')
      }
    }

    const handleAvatarUpload = async (event) => {
      const file = event.target.files[0]
      if (!file) return

      const formData = new FormData()
      formData.append('file', file)

      try {
        const token = localStorage.getItem('token')
        const response = await axios.post(`${API_BASE_URL}/api/avatar`, formData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        })
        user.value = response.data
        toast.success('頭像更新成功')
      } catch (error) {
        console.error('上傳頭像失敗:', error)
        toast.error(error.response?.data?.detail || '上傳失敗')
      }
    }

    const handleUpdateProfile = async () => {
      try {
        const updateData = {
          username: formData.value.username,
          email: formData.value.email
        }

        const token = localStorage.getItem('token')
        const response = await axios.patch(`${API_BASE_URL}/api/me`, updateData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        user.value = response.data
        toast.success('資料更新成功')
      } catch (error) {
        console.error('更新失敗:', error)
        toast.error(error.response?.data?.detail || '更新失敗')
      }
    }

    onMounted(() => {
      fetchUserInfo()
    })

    return {
      user,
      fileInput,
      formData,
      getAvatarUrl,
      handleAvatarUpload,
      handleUpdateProfile
    }
  }
}
</script>
