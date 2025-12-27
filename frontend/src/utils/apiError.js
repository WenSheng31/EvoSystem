/**
 * 統一的 API 錯誤處理工具
 * 避免在每個組件中重複錯誤提取邏輯
 */

/**
 * 從 API 錯誤響應中提取錯誤消息
 *
 * @param {Error} error - Axios 錯誤對象
 * @param {string} defaultMessage - 默認錯誤消息
 * @returns {string} 錯誤消息
 */
export const getErrorMessage = (error, defaultMessage = '操作失敗') => {
  // 檢查是否有響應數據
  if (error?.response?.data?.detail) {
    return error.response.data.detail
  }

  // 檢查是否有錯誤消息
  if (error?.message) {
    return error.message
  }

  // 返回默認消息
  return defaultMessage
}

/**
 * 檢查錯誤類型
 */
export const ErrorType = {
  /**
   * 網絡錯誤（無響應）
   */
  isNetworkError: (error) => {
    return !error?.response
  },

  /**
   * 未授權錯誤（401）
   */
  isUnauthorizedError: (error) => {
    return error?.response?.status === 401
  },

  /**
   * 權限不足錯誤（403）
   */
  isForbiddenError: (error) => {
    return error?.response?.status === 403
  },

  /**
   * 資源不存在錯誤（404）
   */
  isNotFoundError: (error) => {
    return error?.response?.status === 404
  },

  /**
   * 驗證錯誤（422）
   */
  isValidationError: (error) => {
    return error?.response?.status === 422
  },

  /**
   * 服務器錯誤（5xx）
   */
  isServerError: (error) => {
    const status = error?.response?.status
    return status >= 500 && status < 600
  }
}

/**
 * 根據錯誤類型返回友好的錯誤消息
 *
 * @param {Error} error - Axios 錯誤對象
 * @returns {string} 友好的錯誤消息
 */
export const getFriendlyErrorMessage = (error) => {
  if (ErrorType.isNetworkError(error)) {
    return '網絡連接失敗，請檢查網絡設置'
  }

  if (ErrorType.isUnauthorizedError(error)) {
    return '登入已過期，請重新登入'
  }

  if (ErrorType.isForbiddenError(error)) {
    return '沒有權限執行此操作'
  }

  if (ErrorType.isNotFoundError(error)) {
    return '請求的資源不存在'
  }

  if (ErrorType.isServerError(error)) {
    return '服務器錯誤，請稍後再試'
  }

  // 返回服務器提供的詳細消息
  return getErrorMessage(error, '操作失敗')
}
