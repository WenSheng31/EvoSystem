<template>
  <div>
    <h1 class="text-2xl font-semibold text-gray-900 mb-6">審計日誌</h1>

    <!-- 篩選區 -->
    <div class="mb-4 flex items-center gap-4">
      <label class="text-sm font-medium text-gray-700">操作類型：</label>
      <select
        v-model="selectedAction"
        @change="handleFilterChange"
        class="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option :value="null">全部</option>
        <option value="register">註冊</option>
        <option value="login_success">登入成功</option>
        <option value="login_failed">登入失敗</option>
        <option value="logout">登出</option>
      </select>

      <div class="ml-auto text-sm text-gray-600">
        共 {{ total }} 筆記錄
      </div>
    </div>

    <!-- 表格 -->
    <div class="bg-white rounded-lg border border-gray-200 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full min-w-[900px]">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase w-[160px]">
                時間
              </th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase w-[120px]">
                用戶
              </th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase w-[100px]">
                操作
              </th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase w-[130px]">
                IP 地址
              </th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                詳情
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-if="logs.length === 0">
              <td colspan="5" class="px-4 py-8 text-center text-gray-500">
                暫無記錄
              </td>
            </tr>
            <tr v-for="log in logs" :key="log.id" class="hover:bg-gray-50">
              <td class="px-4 py-3 text-sm text-gray-600">
                {{ formatDate(log.created_at) }}
              </td>
              <td class="px-4 py-3 text-sm text-gray-900">
                <span v-if="log.username">{{ log.username }}</span>
                <span v-else class="text-gray-400">（已刪除）</span>
              </td>
              <td class="px-4 py-3 text-sm">
                <span
                  :class="getActionBadgeClass(log.action)"
                  class="px-2 py-1 rounded-lg text-xs font-medium"
                >
                  {{ formatActionText(log.action) }}
                </span>
              </td>
              <td class="px-4 py-3 text-sm text-gray-600">
                {{ log.ip_address || '-' }}
              </td>
              <td class="px-4 py-3 text-sm text-gray-600">
                {{ log.details || '-' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 分頁控制 -->
    <div v-if="totalPages > 1" class="mt-4 flex items-center justify-center gap-4">
      <button
        @click="prevPage"
        :disabled="currentPage === 1"
        :class="currentPage === 1 ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-100'"
        class="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium"
      >
        上一頁
      </button>

      <span class="text-sm text-gray-600">
        第 {{ currentPage }} / {{ totalPages }} 頁
      </span>

      <button
        @click="nextPage"
        :disabled="currentPage === totalPages"
        :class="currentPage === totalPages ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-100'"
        class="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium"
      >
        下一頁
      </button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { adminAPI } from '../api/admin'
import { useUser } from '../composables/useUser'
import { useToast } from '../composables/useToast'
import { ROUTES } from '../config/constants'
import { formatDate } from '../utils/dateFormatter'
import { getErrorMessage } from '../utils/apiError'

export default {
  name: 'AuditLogs',
  setup() {
    const router = useRouter()
    const { user, fetchUserInfo } = useUser()
    const toast = useToast()

    const logs = ref([])
    const currentPage = ref(1)
    const pageSize = ref(20)
    const total = ref(0)
    const totalPages = ref(0)
    const selectedAction = ref(null)

    const loadLogs = async () => {
      try {
        const response = await adminAPI.getAuditLogs(
          currentPage.value,
          pageSize.value,
          selectedAction.value
        )
        logs.value = response.data.logs
        total.value = response.data.total
        totalPages.value = response.data.total_pages
      } catch (error) {
        toast.error(getErrorMessage(error, '載入審計日誌失敗'))
      }
    }

    const loadData = async () => {
      try {
        // 獲取當前用戶資訊
        await fetchUserInfo()

        // 檢查是否為管理員
        if (user.value?.role !== 'admin') {
          toast.error('需要管理員權限')
          router.push(ROUTES.HOME)
          return
        }

        // 載入日誌
        await loadLogs()
      } catch (error) {
        toast.error('載入失敗')
      }
    }

    const handleFilterChange = () => {
      currentPage.value = 1
      loadLogs()
    }

    const prevPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--
        loadLogs()
      }
    }

    const nextPage = () => {
      if (currentPage.value < totalPages.value) {
        currentPage.value++
        loadLogs()
      }
    }

    const formatActionText = (action) => {
      const actionMap = {
        register: '註冊',
        login_success: '登入成功',
        login_failed: '登入失敗',
        logout: '登出'
      }
      return actionMap[action] || action
    }

    const getActionBadgeClass = (action) => {
      const classMap = {
        register: 'bg-blue-100 text-blue-700',
        login_success: 'bg-green-100 text-green-700',
        login_failed: 'bg-red-100 text-red-700',
        logout: 'bg-gray-100 text-gray-700'
      }
      return classMap[action] || 'bg-gray-100 text-gray-700'
    }

    onMounted(() => {
      loadData()
    })

    return {
      logs,
      currentPage,
      total,
      totalPages,
      selectedAction,
      handleFilterChange,
      prevPage,
      nextPage,
      formatDate,
      formatActionText,
      getActionBadgeClass
    }
  }
}
</script>
