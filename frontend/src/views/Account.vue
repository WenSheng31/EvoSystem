<template>
  <div>
    <h1 class="text-2xl font-semibold text-gray-900 mb-6">帳號管理</h1>

      <!-- 頭像上傳 -->
      <div class="bg-white p-6 rounded mb-6">
        <h2 class="text-base font-medium text-gray-900 mb-4">大頭貼</h2>
        <div class="flex items-center gap-6">
          <AvatarImage
            :avatar="user?.avatar"
            :username="user?.username"
            :size="80"
          />
          <div>
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              class="hidden"
              @change="handleAvatarUpload"
            />
            <button
              @click="$refs.fileInput.click()"
              :disabled="uploadingAvatar"
              class="px-4 py-2 text-sm text-gray-700 border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ uploadingAvatar ? '上傳中...' : '上傳新頭像' }}
            </button>
            <p class="text-xs text-gray-500 mt-2">支援 JPG, PNG, GIF（最大 5MB）</p>
          </div>
        </div>
      </div>

      <!-- 帳號資訊 -->
      <div class="bg-white p-6 rounded">
        <h2 class="text-base font-medium text-gray-900 mb-4">帳號資訊</h2>
        <form @submit.prevent="handleUpdateProfile" class="space-y-4">
          <div>
            <label class="block mb-1.5 text-gray-700 text-sm font-medium">用戶名</label>
            <input
              v-model="formData.username"
              type="text"
              class="w-full px-3 py-2.5 border border-gray-300 rounded text-sm focus:outline-none focus:border-gray-900"
            />
          </div>

          <div>
            <label class="block mb-1.5 text-gray-700 text-sm font-medium">電子郵件</label>
            <input
              v-model="formData.email"
              type="email"
              class="w-full px-3 py-2.5 border border-gray-300 rounded text-sm focus:outline-none focus:border-gray-900"
            />
          </div>

          <div>
            <label class="block mb-1.5 text-gray-700 text-sm font-medium">個人簡介</label>
            <textarea
              v-model="formData.bio"
              rows="3"
              maxlength="200"
              placeholder="介紹一下自己..."
              class="w-full px-3 py-2.5 border border-gray-300 rounded text-sm focus:outline-none focus:border-gray-900 resize-none"
            ></textarea>
            <p class="text-xs text-gray-500 mt-1">{{ formData.bio?.length || 0 }}/200</p>
          </div>

          <div class="mt-6">
            <button
              type="submit"
              :disabled="updatingProfile"
              class="px-4 py-2 bg-gray-900 text-white rounded text-sm font-medium hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ updatingProfile ? '儲存中...' : '儲存變更' }}
            </button>
          </div>
        </form>
      </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { userAPI } from '../api/user'
import { useToast } from '../composables/useToast'
import { useUser } from '../composables/useUser'
import AvatarImage from '../components/AvatarImage.vue'

export default {
  name: 'Account',
  components: {
    AvatarImage
  },
  setup() {
    const toast = useToast()
    const { user, fetchUserInfo, updateUser } = useUser()
    const fileInput = ref(null)
    const uploadingAvatar = ref(false)
    const updatingProfile = ref(false)
    const formData = ref({
      username: '',
      email: '',
      bio: ''
    })

    const loadUserInfo = async () => {
      try {
        const userData = await fetchUserInfo()
        formData.value.username = userData.username
        formData.value.email = userData.email
        formData.value.bio = userData.bio || ''
      } catch (err) {
        // response interceptor 會自動處理 401 錯誤並跳轉
      }
    }

    const handleAvatarUpload = async (event) => {
      const file = event.target.files[0]
      if (!file) return

      uploadingAvatar.value = true
      try {
        const response = await userAPI.uploadAvatar(file)
        updateUser(response.data)
        toast.success('頭像更新成功')
      } catch (error) {
        toast.error(error.response?.data?.detail || '上傳失敗')
      } finally {
        uploadingAvatar.value = false
        event.target.value = '' // 清空文件選擇，允許重新上傳同一文件
      }
    }

    const handleUpdateProfile = async () => {
      // 前端驗證
      if (formData.value.username.length > 20) {
        toast.error('用戶名最多 20 個字符')
        return
      }

      updatingProfile.value = true
      try {
        const updateData = {
          username: formData.value.username,
          email: formData.value.email,
          bio: formData.value.bio
        }

        const response = await userAPI.updateProfile(updateData)
        updateUser(response.data)
        toast.success('資料更新成功')
      } catch (error) {
        toast.error(error.response?.data?.detail || '更新失敗')
      } finally {
        updatingProfile.value = false
      }
    }

    onMounted(() => {
      loadUserInfo()
    })

    return {
      user,
      fileInput,
      formData,
      uploadingAvatar,
      updatingProfile,
      handleAvatarUpload,
      handleUpdateProfile
    }
  }
}
</script>
