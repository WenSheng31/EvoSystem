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

    <!-- 全局確認對話框 -->
    <ConfirmDialog
      :isOpen="dialogState.isOpen"
      :title="dialogState.title"
      :message="dialogState.message"
      :confirmText="dialogState.confirmText"
      :cancelText="dialogState.cancelText"
      :type="dialogState.type"
      @confirm="handleConfirm"
      @cancel="handleCancel"
    />

    <!-- 全局輸入對話框 -->
    <InputDialog
      :isOpen="inputDialogState.isOpen"
      :title="inputDialogState.title"
      :message="inputDialogState.message"
      :inputLabel="inputDialogState.inputLabel"
      :inputPlaceholder="inputDialogState.inputPlaceholder"
      :inputType="inputDialogState.inputType"
      :hint="inputDialogState.hint"
      :confirmText="inputDialogState.confirmText"
      :cancelText="inputDialogState.cancelText"
      @confirm="handleInputConfirm"
      @cancel="handleInputCancel"
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useUser } from '../composables/useUser'
import { useConfirmDialog } from '../composables/useConfirmDialog'
import { useInputDialog } from '../composables/useInputDialog'
import AppHeader from '../components/AppHeader.vue'
import AppSidebar from '../components/AppSidebar.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import InputDialog from '../components/InputDialog.vue'

export default {
  name: 'MainLayout',
  components: {
    AppHeader,
    AppSidebar,
    ConfirmDialog,
    InputDialog
  },
  setup() {
    const { user, fetchUserInfo } = useUser()
    const { dialogState, handleConfirm, handleCancel } = useConfirmDialog()
    const { inputDialogState, handleConfirm: handleInputConfirm, handleCancel: handleInputCancel } = useInputDialog()
    const sidebarOpen = ref(false)

    onMounted(() => {
      fetchUserInfo()
    })

    return {
      user,
      sidebarOpen,
      dialogState,
      handleConfirm,
      handleCancel,
      inputDialogState,
      handleInputConfirm,
      handleInputCancel
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
