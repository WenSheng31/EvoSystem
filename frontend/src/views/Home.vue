<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white border-b border-gray-200">
      <div class="max-w-5xl mx-auto px-6 py-4 flex justify-between items-center">
        <h2 class="text-lg font-semibold text-gray-900">會員系統</h2>
        <div class="flex items-center gap-3">
          <span v-if="user" class="text-gray-700 text-sm">{{ user.username }}</span>
          <button @click="handleLogout" class="px-4 py-2 bg-gray-900 text-white rounded text-sm font-medium hover:bg-gray-800">
            登出
          </button>
        </div>
      </div>
    </nav>
    <main class="max-w-5xl mx-auto px-6 py-8">
      <h1 class="text-2xl font-semibold text-gray-900 mb-3">首頁</h1>
      <p class="text-gray-600">登入成功！</p>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../api/auth'

export default {
  name: 'Home',
  setup() {
    const router = useRouter()
    const user = ref(null)

    const fetchUserInfo = async () => {
      try {
        const response = await authAPI.getCurrentUser()
        user.value = response.data
      } catch (err) {
        console.error('獲取用戶資訊失敗:', err)
        handleLogout()
      }
    }

    const handleLogout = () => {
      localStorage.removeItem('token')
      router.push('/login')
    }

    onMounted(() => {
      fetchUserInfo()
    })

    return {
      user,
      handleLogout
    }
  }
}
</script>
