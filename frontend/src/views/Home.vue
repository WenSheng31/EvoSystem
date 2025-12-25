<template>
  <div class="min-h-screen bg-gray-50">
    <Header :user="user" />
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
import Header from '../components/Header.vue'

export default {
  name: 'Home',
  components: {
    Header
  },
  setup() {
    const router = useRouter()
    const user = ref(null)

    const fetchUserInfo = async () => {
      try {
        const response = await authAPI.getCurrentUser()
        user.value = response.data
      } catch (err) {
        console.error('獲取用戶資訊失敗:', err)
        router.push('/login')
      }
    }

    onMounted(() => {
      fetchUserInfo()
    })

    return {
      user
    }
  }
}
</script>
