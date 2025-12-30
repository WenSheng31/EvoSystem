<template>
  <div class="flex justify-center items-center min-h-screen bg-gray-50">
    <div class="bg-white p-8 w-full max-w-sm rounded-lg border border-gray-200">
      <div class="flex flex-col items-center mb-6">
        <img src="/logo/main_nobk_b.png" alt="EvoSystem Logo" class="h-16 mb-4" />
        <h2 class="text-xl font-semibold text-gray-900">登入 EvoSystem</h2>
      </div>
      <form @submit.prevent="handleLogin" class="space-y-4">
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
        <button
          type="submit"
          :disabled="isSubmitting"
          class="w-full py-2.5 bg-gray-900 text-white rounded-lg text-sm font-medium hover:bg-gray-800 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {{ isSubmitting ? '登入中...' : '登入' }}
        </button>
      </form>
      <div class="mt-6 text-center text-sm text-gray-600">
        還沒有帳號？ <router-link to="/register" class="text-gray-900 font-medium hover:underline">註冊</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../api/auth'
import { useToast } from '../composables/useToast'
import { getErrorMessage } from '../utils/apiError'
import { NAVIGATION_DELAYS, ROUTES } from '../config/constants'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const toast = useToast()
    const formData = ref({
      email: '',
      password: ''
    })
    const isSubmitting = ref(false)

    const handleLogin = async () => {
      if (isSubmitting.value) return // 防止重複提交

      isSubmitting.value = true
      try {
        // 登入請求 - 後端會自動設置 HttpOnly Cookie
        await authAPI.login(formData.value)

        toast.success('登入成功')
        setTimeout(() => router.push(ROUTES.HOME), NAVIGATION_DELAYS.LOGIN_SUCCESS)
      } catch (err) {
        toast.error(getErrorMessage(err, '登入失敗'))
      } finally {
        isSubmitting.value = false
      }
    }

    return {
      formData,
      isSubmitting,
      handleLogin
    }
  }
}
</script>
