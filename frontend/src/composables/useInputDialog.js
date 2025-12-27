import { reactive } from 'vue'

export const inputDialogState = reactive({
  isOpen: false,
  title: '輸入',
  message: '',
  inputLabel: '',
  inputPlaceholder: '請輸入',
  inputType: 'text',
  hint: '',
  confirmText: '確認',
  cancelText: '取消',
  resolve: null
})

export function useInputDialog() {
  /**
   * 顯示輸入對話框
   * @param {Object} options - 對話框選項
   * @param {string} options.title - 標題
   * @param {string} options.message - 說明文字
   * @param {string} options.inputLabel - 輸入框標籤
   * @param {string} options.inputPlaceholder - 輸入框提示
   * @param {string} options.inputType - 輸入框類型 (text, password, email, number, tel, url)
   * @param {string} options.hint - 提示文字
   * @param {string} options.confirmText - 確認按鈕文字
   * @param {string} options.cancelText - 取消按鈕文字
   * @returns {Promise<{confirmed: boolean, value: string|null}>}
   */
  const showInput = (options = {}) => {
    return new Promise((resolve) => {
      inputDialogState.isOpen = true
      inputDialogState.title = options.title || '輸入'
      inputDialogState.message = options.message || ''
      inputDialogState.inputLabel = options.inputLabel || ''
      inputDialogState.inputPlaceholder = options.inputPlaceholder || '請輸入'
      inputDialogState.inputType = options.inputType || 'text'
      inputDialogState.hint = options.hint || ''
      inputDialogState.confirmText = options.confirmText || '確認'
      inputDialogState.cancelText = options.cancelText || '取消'
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
