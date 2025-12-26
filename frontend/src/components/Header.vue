<template>
  <header class="bg-white border-b border-gray-200">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
      <button @click="$router.push('/home')" class="text-base font-semibold text-gray-900 hover:text-gray-700">
        測試系統
      </button>

      <div v-if="user" class="flex items-center gap-3 sm:gap-6">
        <!-- 管理員入口 -->
        <button
          v-if="user.role === 'admin'"
          @click="$router.push(ROUTES.ADMIN)"
          class="px-3.5 py-1.5 text-sm text-purple-700 hover:text-purple-900 border border-purple-300 rounded hover:bg-purple-50 font-medium"
        >
          用戶管理
        </button>

        <div class="flex items-center gap-2.5">
          <button
            @click="$router.push(ROUTES.ACCOUNT)"
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
          <span class="hidden sm:inline text-sm text-gray-700">{{ user.username }}</span>
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
import { getAvatarUrl } from '../utils/avatar'
import { ROUTES } from '../config/constants'

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
      // 使用 window.location.href 確保完全重新載入頁面
      window.location.href = ROUTES.LOGIN
    }

    return {
      handleLogout,
      getAvatarUrl,
      ROUTES
    }
  }
}
</script>
