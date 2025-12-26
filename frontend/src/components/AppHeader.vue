<template>
  <header class="fixed top-0 left-0 right-0 h-16 bg-white border-b border-gray-200 z-30">
    <div class="h-full px-4 flex items-center justify-between">
      <!-- 左側：漢堡選單 + 系統名稱 -->
      <div class="flex items-center gap-4">
        <button
          @click="$emit('toggle-sidebar')"
          class="lg:hidden p-2 hover:bg-gray-100 rounded"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
        </button>
        <h1 class="text-lg font-semibold text-gray-900">測試系統</h1>
      </div>

      <!-- 右側：用戶資訊 + 登出 -->
      <div class="flex items-center gap-4">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden">
            <img
              v-if="user?.avatar"
              :src="getAvatarUrl(user.avatar)"
              alt="Avatar"
              class="w-full h-full object-cover"
            />
            <span v-else class="text-gray-600 font-medium text-xs">
              {{ user?.username?.charAt(0).toUpperCase() }}
            </span>
          </div>
          <span class="hidden sm:block text-sm text-gray-700">{{ user?.username }}</span>
        </div>
        <button
          @click="handleLogout"
          class="px-4 py-2 text-sm bg-gray-900 text-white rounded font-medium hover:bg-gray-800 transition-colors"
        >
          登出
        </button>
      </div>
    </div>
  </header>
</template>

<script>
import { getAvatarUrl } from '../utils/avatar'
import { ROUTES } from '../config/constants'

export default {
  name: 'AppHeader',
  props: {
    user: {
      type: Object,
      default: null
    }
  },
  emits: ['toggle-sidebar'],
  setup() {
    const handleLogout = () => {
      localStorage.removeItem('token')
      window.location.href = ROUTES.LOGIN
    }

    return {
      handleLogout,
      getAvatarUrl
    }
  }
}
</script>
