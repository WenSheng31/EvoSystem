<template>
  <div>
    <!-- 遮罩 (手機版) -->
    <div
      v-if="isOpen"
      @click="$emit('close')"
      class="fixed inset-0 bg-black/40 z-20 lg:hidden"
    ></div>

    <!-- 側邊欄 -->
    <aside
      class="fixed top-16 left-0 bottom-0 w-64 bg-white border-r border-gray-200 z-30 transition-transform duration-300 lg:translate-x-0"
      :class="isOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <nav class="p-4 h-full overflow-y-auto">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          @click="$emit('close')"
          class="flex items-center gap-3 px-4 py-3 rounded text-sm font-medium mb-1 transition-colors"
          :class="isActive(item.path) ? 'bg-gray-900 text-white' : 'text-gray-700 hover:bg-gray-100'"
        >
          <component :is="item.icon" :size="18" />
          <span>{{ item.name }}</span>
        </router-link>
      </nav>
    </aside>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Home, Settings, Users } from 'lucide-vue-next'
import { ROUTES } from '../config/constants'

export default {
  name: 'AppSidebar',
  props: {
    user: {
      type: Object,
      default: null
    },
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close'],
  setup(props) {
    const route = useRoute()

    const menuItems = computed(() => {
      const items = [
        { path: ROUTES.HOME, name: '首頁', icon: Home },
        { path: ROUTES.ACCOUNT, name: '帳號管理', icon: Settings },
      ]

      if (props.user?.role === 'admin') {
        items.push({ path: ROUTES.ADMIN, name: '用戶管理', icon: Users })
      }

      return items
    })

    const isActive = (path) => {
      return route.path === path
    }

    return {
      menuItems,
      isActive,
      ROUTES
    }
  }
}
</script>
