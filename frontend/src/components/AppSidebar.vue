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
      class="fixed top-16 lg:top-0 left-0 bottom-0 w-64 bg-white border-r border-gray-200 z-30 transition-transform duration-300 lg:translate-x-0 flex flex-col"
      :class="isOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <!-- Logo 區域 -->
      <div class="hidden lg:flex items-center gap-3 p-6">
        <img src="/logo/main_nobk_b.png" alt="Logo" class="h-8 w-auto" />
        <h1 class="text-xl font-bold text-gray-900">EvoSystem</h1>
      </div>

      <!-- 導航選單 -->
      <nav class="flex-1 px-4 pt-4 lg:pt-0 overflow-y-auto">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          @click="$emit('close')"
          class="flex items-center gap-3 px-4 py-3 rounded text-sm font-medium mb-1 transition-colors"
          :class="
            isActive(item.path)
              ? 'bg-gray-900 text-white'
              : 'text-gray-700 hover:bg-gray-100'
          "
        >
          <component :is="item.icon" :size="18" />
          <span>{{ item.name }}</span>
        </router-link>
      </nav>

      <!-- 底部用戶區域 -->
      <div class="p-4">
        <!-- 用戶資訊 -->
        <div class="flex items-center gap-3 mb-3">
          <div
            class="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden flex-shrink-0"
          >
            <img
              v-if="user?.avatar"
              :src="getAvatarUrl(user.avatar)"
              alt="Avatar"
              class="w-full h-full object-cover"
            />
            <span v-else class="text-gray-600 font-medium text-sm">
              {{ user?.username?.charAt(0).toUpperCase() }}
            </span>
          </div>
          <div class="flex-1 min-w-0">
            <div class="text-sm font-medium text-gray-900 truncate">
              {{ user?.username }}
            </div>
            <div class="text-xs text-gray-500 truncate">{{ user?.email }}</div>
          </div>
        </div>

        <!-- 登出按鈕 -->
        <button
          @click="handleLogout"
          class="w-full px-4 py-2 text-sm bg-gray-900 text-white rounded font-medium hover:bg-gray-800 transition-colors"
        >
          登出
        </button>
      </div>
    </aside>
  </div>
</template>

<script>
import { computed } from "vue";
import { useRoute } from "vue-router";
import { Home, Settings, Users } from "lucide-vue-next";
import { ROUTES } from "../config/constants";
import { getAvatarUrl } from "../utils/avatar";

export default {
  name: "AppSidebar",
  props: {
    user: {
      type: Object,
      default: null,
    },
    isOpen: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["close"],
  setup(props) {
    const route = useRoute();

    const menuItems = computed(() => {
      const items = [
        { path: ROUTES.HOME, name: "首頁", icon: Home },
        { path: ROUTES.ACCOUNT, name: "帳號管理", icon: Settings },
      ];

      if (props.user?.role === "admin") {
        items.push({ path: ROUTES.ADMIN, name: "用戶管理", icon: Users });
      }

      return items;
    });

    const isActive = (path) => {
      return route.path === path;
    };

    const handleLogout = () => {
      localStorage.removeItem("token");
      localStorage.removeItem("userRole");
      window.location.href = ROUTES.LOGIN;
    };

    return {
      menuItems,
      isActive,
      getAvatarUrl,
      handleLogout,
      ROUTES,
    };
  },
};
</script>
