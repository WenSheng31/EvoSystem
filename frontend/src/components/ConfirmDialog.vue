<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="isOpen"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        @click.self="handleCancel"
      >
        <!-- 遮罩 -->
        <div class="absolute inset-0 bg-black/40"></div>

        <!-- 對話框 -->
        <div
          class="relative bg-white rounded-lg shadow-xl max-w-md w-full p-6"
          @click.stop
        >
          <!-- 標題 -->
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            {{ title }}
          </h3>

          <!-- 內容 -->
          <div class="mb-6">
            <p class="text-sm text-gray-600">
              {{ message }}
            </p>
          </div>

          <!-- 按鈕 -->
          <div class="flex gap-3 justify-end">
            <button
              @click="handleCancel"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50 transition-colors"
            >
              取消
            </button>
            <button
              @click="handleConfirm"
              :class="confirmButtonClass"
              class="px-4 py-2 text-sm font-medium text-white rounded transition-colors"
            >
              確認
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script>
export default {
  name: "ConfirmDialog",
  props: {
    isOpen: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: "確認操作",
    },
    message: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      default: "danger", // danger, primary, warning
      validator: (value) => ["danger", "primary", "warning"].includes(value),
    },
  },
  emits: ["confirm", "cancel"],
  computed: {
    confirmButtonClass() {
      const classes = {
        danger: "bg-red-600 hover:bg-red-700",
        primary: "bg-gray-900 hover:bg-gray-800",
        warning: "bg-orange-600 hover:bg-orange-700",
      };
      return classes[this.type];
    },
  },
  setup(props, { emit }) {
    const handleConfirm = () => {
      emit("confirm");
    };

    const handleCancel = () => {
      emit("cancel");
    };

    return {
      handleConfirm,
      handleCancel,
    };
  },
};
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .bg-white,
.modal-leave-active .bg-white {
  transition: transform 0.2s ease;
}

.modal-enter-from .bg-white,
.modal-leave-to .bg-white {
  transform: scale(0.95);
}
</style>
