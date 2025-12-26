<template>
  <div class="fixed top-6 left-1/2 -translate-x-1/2 z-50 flex flex-col items-center gap-3">
    <transition-group name="fade">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="bg-white px-4 py-3 rounded border border-gray-200 flex items-center gap-3 min-w-[320px] max-w-md"
      >
        <div class="flex-1">
          <p class="text-sm text-gray-900">{{ toast.message }}</p>
        </div>
        <button
          @click="removeToast(toast.id)"
          class="text-gray-400 hover:text-gray-600 flex-shrink-0"
        >
          ✕
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script>
import { toastState } from '../composables/useToast'

export default {
  name: 'Toast',
  setup() {
    const removeToast = (id) => {
      const index = toastState.toasts.findIndex(t => t.id === id)
      if (index > -1) {
        toastState.toasts.splice(index, 1)
      }
    }

    return {
      toasts: toastState.toasts,
      removeToast
    }
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
