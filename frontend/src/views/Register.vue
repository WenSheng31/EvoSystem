<template>
  <div class="flex justify-center items-center min-h-screen bg-gray-50">
    <div class="bg-white p-8 w-full max-w-sm rounded">
      <h2 class="text-xl font-semibold mb-6 text-gray-900">註冊</h2>
      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block mb-1.5 text-gray-700 text-sm font-medium">用戶名</label>
          <input
            v-model="formData.username"
            type="text"
            required
            placeholder="請輸入用戶名"
            class="w-full px-3 py-2.5 border border-gray-300 rounded text-sm focus:outline-none focus:border-gray-900"
          />
        </div>
        <div>
          <label class="block mb-1.5 text-gray-700 text-sm font-medium">電子郵件</label>
          <input
            v-model="formData.email"
            type="email"
            required
            placeholder="請輸入電子郵件"
            class="w-full px-3 py-2.5 border border-gray-300 rounded text-sm focus:outline-none focus:border-gray-900"
          />
        </div>
        <div>
          <label class="block mb-1.5 text-gray-700 text-sm font-medium">密碼</label>
          <input
            v-model="formData.password"
            type="password"
            required
            placeholder="請輸入密碼"
            class="w-full px-3 py-2.5 border border-gray-300 rounded text-sm focus:outline-none focus:border-gray-900"
          />
        </div>
        <button type="submit" class="w-full py-2.5 bg-gray-900 text-white rounded text-sm font-medium hover:bg-gray-800">
          註冊
        </button>
      </form>
      <div class="mt-6 text-center text-sm text-gray-600">
        已有帳號？ <router-link to="/login" class="text-gray-900 font-medium hover:underline">登入</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../api/auth'
import { useToast } from '../composables/useToast'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    const toast = useToast()
    const formData = ref({
      username: '',
      email: '',
      password: ''
    })

    const handleRegister = async () => {
      try {
        await authAPI.register(formData.value)
        toast.success('註冊成功！即將跳轉到登入頁面...')
        setTimeout(() => {
          router.push('/login')
        }, 2000)
      } catch (err) {
        toast.error(err.response?.data?.detail || '註冊失敗')
      }
    }

    return {
      formData,
      handleRegister
    }
  }
}
</script>
