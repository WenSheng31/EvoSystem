import { API_BASE_URL } from './config'

export const getAvatarUrl = (avatarPath) => {
  if (!avatarPath) return null
  const cleanPath = avatarPath.replace(/\\/g, '/').replace('backend/', '')
  return `${API_BASE_URL}/${cleanPath}`
}
