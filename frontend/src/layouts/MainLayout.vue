<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <AppHeader
      :user="user"
      @toggle-sidebar="sidebarOpen = !sidebarOpen"
    />

    <!-- Sidebar -->
    <AppSidebar
      :user="user"
      :isOpen="sidebarOpen"
      @close="sidebarOpen = false"
    />

    <!-- Main Content -->
    <main class="pt-16 lg:pt-0 lg:pl-64 min-h-screen">
      <div class="p-6 lg:p-8">
        <router-view v-slot="{ Component }">
          <Transition name="fade" mode="out-in">
            <component :is="Component" />
          </Transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useUser } from '../composables/useUser'
import AppHeader from '../components/AppHeader.vue'
import AppSidebar from '../components/AppSidebar.vue'

export default {
  name: 'MainLayout',
  components: {
    AppHeader,
    AppSidebar
  },
  setup() {
    const { user, fetchUserInfo } = useUser()
    const sidebarOpen = ref(false)

    onMounted(() => {
      fetchUserInfo()
    })

    return {
      user,
      sidebarOpen
    }
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
