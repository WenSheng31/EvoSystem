/**
 * 日期格式化工具函數
 */

/**
 * 格式化日期為本地化字符串
 * @param {string} dateString - ISO 格式的日期字符串
 * @param {Intl.DateTimeFormatOptions} options - 自定義格式化選項
 * @returns {string} 格式化後的日期字符串
 */
export const formatDate = (dateString, options = {}) => {
  const date = new Date(dateString)

  const defaultOptions = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }

  return date.toLocaleString('zh-TW', { ...defaultOptions, ...options })
}

/**
 * 格式化為簡短日期（僅年月日）
 * @param {string} dateString - ISO 格式的日期字符串
 * @returns {string} 格式化後的日期字符串
 */
export const formatShortDate = (dateString) => {
  return formatDate(dateString, {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}
