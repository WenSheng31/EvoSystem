import { reactive } from 'vue'

export const inputDialogState = reactive({
  isOpen: false,
  title: '輸入',
  type: 'text',
  placeholder: '請輸入',
  hint: '',
  resolve: null
})

export function useInputDialog() {
  /**
   * 顯示輸入對話框
   * @param {Object} options - 對話框選項
   * @param {string} options.title - 標題
   * @param {string} options.type - 輸入框類型 (text, password, email, number, tel, url)
   * @param {string} options.placeholder - 輸入框提示
   * @param {string} options.hint - 提示文字
   * @returns {Promise<{confirmed: boolean, value: string|null}>}
   */
  const showInput = (options = {}) => {
    return new Promise((resolve) => {
      inputDialogState.isOpen = true
      inputDialogState.title = options.title || '輸入'
      inputDialogState.type = options.type || 'text'
      inputDialogState.placeholder = options.placeholder || '請輸入'
      inputDialogState.hint = options.hint || ''
      inputDialogState.resolve = resolve
    })
  }

  const handleConfirm = (value) => {
    if (inputDialogState.resolve) {
      inputDialogState.resolve({ confirmed: true, value })
    }
    inputDialogState.isOpen = false
    inputDialogState.resolve = null
  }

  const handleCancel = () => {
    if (inputDialogState.resolve) {
      inputDialogState.resolve({ confirmed: false, value: null })
    }
    inputDialogState.isOpen = false
    inputDialogState.resolve = null
  }

  return {
    showInput,
    inputDialogState,
    handleConfirm,
    handleCancel
  }
}
