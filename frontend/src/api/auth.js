import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// 請求攔截器
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

export const authAPI = {
  register(userData) {
    return api.post('/register', userData)
  },

  login(credentials) {
    return api.post('/login', credentials)
  },

  getCurrentUser() {
    return api.get('/me')
  }
}

export default api
