import { reactive } from 'vue'

export const dialogState = reactive({
  isOpen: false,
  title: '確認操作',
  message: '',
  confirmText: '確認',
  cancelText: '取消',
  type: 'danger',
  resolve: null
})

export function useConfirmDialog() {
  const confirm = (options) => {
    return new Promise((resolve) => {
      dialogState.isOpen = true
      dialogState.title = options.title || '確認操作'
      dialogState.message = options.message
      dialogState.confirmText = options.confirmText || '確認'
      dialogState.cancelText = options.cancelText || '取消'
      dialogState.type = options.type || 'danger'
      dialogState.resolve = resolve
    })
  }

  const handleConfirm = () => {
    if (dialogState.resolve) {
      dialogState.resolve(true)
    }
    dialogState.isOpen = false
    dialogState.resolve = null
  }

  const handleCancel = () => {
    if (dialogState.resolve) {
      dialogState.resolve(false)
    }
    dialogState.isOpen = false
    dialogState.resolve = null
  }

  return {
    confirm,
    dialogState,
    handleConfirm,
    handleCancel
  }
}
