<template>
  <div class="flex justify-center items-center min-h-screen bg-gray-50">
    <div class="bg-white p-8 w-full max-w-sm rounded-lg border border-gray-200">
      <h2 class="text-xl font-semibold mb-6 text-gray-900 text-center">註冊</h2>
      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block mb-1.5 text-gray-700 text-sm font-medium">用戶名</label>
          <input
            v-model="formData.username"
            type="text"
            required
            placeholder="請輸入用戶名"
            class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-gray-900"
          />
        </div>
        <div>
          <label class="block mb-1.5 text-gray-700 text-sm font-medium">電子郵件</label>
          <input
            v-model="formData.email"
            type="email"
            required
            placeholder="請輸入電子郵件"
            class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-gray-900"
          />
        </div>
        <div>
          <label class="block mb-1.5 text-gray-700 text-sm font-medium">密碼</label>
          <input
            v-model="formData.password"
            type="password"
            required
            placeholder="請輸入密碼"
            class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-gray-900"
          />
        </div>
        <div>
          <label class="block mb-1.5 text-gray-700 text-sm font-medium">確認密碼</label>
          <input
            v-model="formData.confirmPassword"
            type="password"
            required
            placeholder="請再次輸入密碼"
            class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-gray-900"
          />
        </div>
        <button type="submit" class="w-full py-2.5 bg-gray-900 text-white rounded-lg text-sm font-medium hover:bg-gray-800">
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
import { NAVIGATION_DELAYS, ROUTES } from '../config/constants'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    const toast = useToast()
    const formData = ref({
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    })

    const handleRegister = async () => {
      // 前端驗證
      if (formData.value.username.length > 20) {
        toast.error('用戶名最多 20 個字符')
        return
      }

      // 驗證兩次密碼是否一致
      if (formData.value.password !== formData.value.confirmPassword) {
        toast.error('兩次輸入的密碼不一致')
        return
      }

      try {
        // 只發送必要的字段到後端
        const { username, email, password } = formData.value
        await authAPI.register({ username, email, password })
        toast.success('註冊成功！即將跳轉到登入頁面...')
        setTimeout(() => {
          router.push(ROUTES.LOGIN)
        }, NAVIGATION_DELAYS.REGISTER_SUCCESS)
      } catch (err) {
        // 只顯示簡潔的錯誤訊息
        const detail = err.response?.data?.detail
        if (detail) {
          toast.error(detail)
        } else {
          toast.error('註冊失敗，請檢查輸入格式')
        }
      }
    }

    return {
      formData,
      handleRegister
    }
  }
}
</script>
