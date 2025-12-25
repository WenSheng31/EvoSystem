<template>
  <header class="bg-white border-b border-gray-200">
    <div class="max-w-5xl mx-auto px-6 h-16 flex items-center justify-between">
      <button @click="$router.push('/home')" class="text-base font-semibold text-gray-900 hover:text-gray-700">
        測試系統
      </button>

      <div v-if="user" class="flex items-center gap-6">
        <div class="flex items-center gap-2.5">
          <button
            @click="$router.push('/account')"
            class="w-8 h-8 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center overflow-hidden transition-colors"
            title="帳號管理"
          >
            <img
              v-if="user.avatar"
              :src="getAvatarUrl(user.avatar)"
              alt="Avatar"
              class="w-full h-full object-cover"
            />
            <span v-else class="text-gray-600 font-medium text-xs">
              {{ user.username.charAt(0).toUpperCase() }}
            </span>
          </button>
          <span class="text-sm text-gray-700">{{ user.username }}</span>
        </div>

        <button
          @click="handleLogout"
          class="px-3.5 py-1.5 text-sm text-gray-700 hover:text-gray-900 border border-gray-300 rounded hover:bg-gray-50"
        >
          登出
        </button>
      </div>
    </div>
  </header>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'Header',
  props: {
    user: {
      type: Object,
      default: null
    }
  },
  setup() {
    const router = useRouter()

    const handleLogout = () => {
      localStorage.removeItem('token')
      router.push('/login')
    }

    const getAvatarUrl = (avatarPath) => {
      if (!avatarPath) return null
      // 將路徑中的反斜線替換為斜線，並移除 backend/ 前綴
      const cleanPath = avatarPath.replace(/\\/g, '/').replace('backend/', '')
      return `http://localhost:8000/${cleanPath}`
    }

    return {
      handleLogout,
      getAvatarUrl
    }
  }
}
</script>
