import { reactive } from 'vue'

export const dialogState = reactive({
  isOpen: false,
  title: '',
  message: '',
  type: 'danger',
  resolve: null
})

export function useConfirmDialog() {
  const confirm = (options) => {
    return new Promise((resolve) => {
      dialogState.isOpen = true
      dialogState.title = options.title || '確認操作'
      dialogState.message = options.message
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
