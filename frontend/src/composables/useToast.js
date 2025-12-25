import { reactive } from 'vue'

export const toastState = reactive({
  toasts: []
})

let toastId = 0

export function useToast() {
  const showToast = (message, type = 'info', duration = 3000) => {
    const id = toastId++
    toastState.toasts.push({ id, message, type })

    if (duration > 0) {
      setTimeout(() => {
        const index = toastState.toasts.findIndex(t => t.id === id)
        if (index > -1) {
          toastState.toasts.splice(index, 1)
        }
      }, duration)
    }
  }

  const success = (message, duration) => {
    showToast(message, 'success', duration)
  }

  const error = (message, duration) => {
    showToast(message, 'error', duration)
  }

  const info = (message, duration) => {
    showToast(message, 'info', duration)
  }

  return {
    showToast,
    success,
    error,
    info
  }
}
