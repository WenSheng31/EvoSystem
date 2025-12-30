import { API_CONFIG } from '../config/constants'

export const getAvatarUrl = (avatarPath) => {
  if (!avatarPath) return null

  let path = avatarPath.replace(/\\/g, '/').replace('backend/', '')

  if (path.startsWith('/')) {
    path = path.substring(1)
  }

  return `${API_CONFIG.BASE_URL}/${path}`
}
