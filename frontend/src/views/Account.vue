<template>
  <div>
    <h1 class="text-2xl font-semibold text-gray-900 mb-6">帳號管理</h1>

    <div class="bg-white p-6 rounded-lg border border-gray-200 mb-6">
      <h2 class="text-base font-medium text-gray-900 mb-4">大頭貼</h2>
      <div class="flex items-center gap-6">
        <AvatarImage :avatar="user?.avatar" :username="user?.username" :size="80" />
        <div>
          <input
            ref="fileInput"
            type="file"
            accept="image/jpeg,image/png,image/gif,image/webp"
            class="hidden"
            @change="uploadAvatar"
          />
          <button
            @click="$refs.fileInput.click()"
            :disabled="uploading"
            class="px-4 py-2 text-sm text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
          >
            {{ uploading ? '上傳中...' : '上傳新頭像' }}
          </button>
          <p class="text-xs text-gray-500 mt-2">支援 JPG, PNG, GIF, WebP（最大 5MB）</p>
        </div>
      </div>
    </div>

    <div class="bg-white p-6 rounded-lg border border-gray-200">
      <h2 class="text-base font-medium text-gray-900 mb-4">帳號資訊</h2>
      <form @submit.prevent="updateProfile" class="space-y-4">
        <div>
          <label class="block mb-1.5 text-gray-700 text-sm font-medium">用戶名</label>
          <input
            v-model="form.username"
            type="text"
            class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-gray-900"
          />
        </div>

        <div>
          <label class="block mb-1.5 text-gray-700 text-sm font-medium">電子郵件</label>
          <input
            v-model="form.email"
            type="email"
            class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-gray-900"
          />
        </div>

        <div>
          <label class="block mb-1.5 text-gray-700 text-sm font-medium">個人簡介</label>
          <textarea
            v-model="form.bio"
            rows="3"
            maxlength="200"
            placeholder="介紹一下自己..."
            class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-gray-900 resize-none"
          ></textarea>
          <p class="text-xs text-gray-500 mt-1">{{ form.bio?.length || 0 }}/200</p>
        </div>

        <div>
          <button
            type="submit"
            :disabled="updating"
            class="px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-medium hover:bg-gray-800 disabled:opacity-50"
          >
            {{ updating ? '儲存中...' : '儲存變更' }}
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
import { getErrorMessage } from '../utils/apiError'
import AvatarImage from '../components/AvatarImage.vue'

export default {
  name: 'Account',
  components: { AvatarImage },
  setup() {
    const toast = useToast()
    const { user, fetchUserInfo, updateUser } = useUser()
    const fileInput = ref(null)
    const uploading = ref(false)
    const updating = ref(false)
    const form = ref({
      username: '',
      email: '',
      bio: ''
    })

    const loadUserInfo = async () => {
      const data = await fetchUserInfo()
      form.value = {
        username: data.username,
        email: data.email,
        bio: data.bio || ''
      }
    }

    const uploadAvatar = async (event) => {
      const file = event.target.files[0]
      if (!file) return

      if (file.size > 5 * 1024 * 1024) {
        toast.error('檔案大小不能超過 5MB')
        return
      }

      uploading.value = true
      try {
        const response = await userAPI.uploadAvatar(file)
        updateUser(response.data)
        toast.success('頭像更新成功')
      } catch (error) {
        toast.error(getErrorMessage(error, '上傳失敗'))
      } finally {
        uploading.value = false
        event.target.value = ''
      }
    }

    const updateProfile = async () => {
      if (form.value.username.length > 20) {
        toast.error('用戶名最多 20 個字符')
        return
      }

      updating.value = true
      try {
        const response = await userAPI.updateProfile(form.value)
        updateUser(response.data)
        toast.success('資料更新成功')
      } catch (error) {
        toast.error(getErrorMessage(error, '更新失敗'))
      } finally {
        updating.value = false
      }
    }

    onMounted(loadUserInfo)

    return {
      user,
      fileInput,
      form,
      uploading,
      updating,
      uploadAvatar,
      updateProfile
    }
  }
}
</script>
