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
            <p v-if="message" class="text-sm text-gray-600 mb-4">
              {{ message }}
            </p>

            <label v-if="inputLabel" class="block text-sm font-medium text-gray-700 mb-2">
              {{ inputLabel }}
            </label>
            <input
              v-model="inputValue"
              :type="inputType"
              :placeholder="inputPlaceholder"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              @keyup.enter="handleConfirm"
            />
            <p v-if="hint" class="mt-2 text-xs text-gray-500">
              {{ hint }}
            </p>
          </div>

          <!-- 按鈕 -->
          <div class="flex gap-3 justify-end">
            <button
              @click="handleCancel"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50 transition-colors"
            >
              {{ cancelText }}
            </button>
            <button
              @click="handleConfirm"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded transition-colors"
            >
              {{ confirmText }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script>
import { ref, watch } from 'vue'

export default {
  name: "InputDialog",
  props: {
    isOpen: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: "輸入",
    },
    message: {
      type: String,
      default: "",
    },
    inputLabel: {
      type: String,
      default: "",
    },
    inputPlaceholder: {
      type: String,
      default: "請輸入",
    },
    inputType: {
      type: String,
      default: "text",
      validator: (value) => ["text", "password", "email", "number", "tel", "url"].includes(value),
    },
    hint: {
      type: String,
      default: "",
    },
    confirmText: {
      type: String,
      default: "確認",
    },
    cancelText: {
      type: String,
      default: "取消",
    },
  },
  emits: ["confirm", "cancel"],
  setup(props, { emit }) {
    const inputValue = ref('')

    // 當對話框關閉時清空輸入
    watch(() => props.isOpen, (newVal) => {
      if (!newVal) {
        inputValue.value = ''
      }
    })

    const handleConfirm = () => {
      if (!props.loading) {
        emit("confirm", inputValue.value);
      }
    };

    const handleCancel = () => {
      if (!props.loading) {
        emit("cancel");
      }
    };

    return {
      inputValue,
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
