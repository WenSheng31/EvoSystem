<template>
  <div>
    <h1 class="text-2xl font-semibold text-gray-900 mb-6">待辦事項</h1>

    <!-- 新增待辦事項表單 -->
    <form @submit.prevent="handleCreateTodo" class="flex flex-col sm:flex-row gap-3 mb-6">
      <input
        v-model="newTodoTitle"
        type="text"
        placeholder="輸入新的待辦事項..."
        maxlength="200"
        class="flex-1 px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-gray-900"
        :disabled="isCreating"
      />
      <button
        type="submit"
        :disabled="!newTodoTitle.trim() || isCreating"
        class="px-6 py-2 bg-gray-900 text-white rounded-lg text-sm font-medium hover:bg-gray-800 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors whitespace-nowrap"
      >
        {{ isCreating ? '新增中...' : '新增' }}
      </button>
    </form>

    <!-- 待辦事項列表 -->
    <div class="bg-white rounded-lg border border-gray-200 overflow-hidden">
      <!-- 載入中狀態 -->
      <div v-if="isLoading" class="p-8 text-center text-gray-500">
        載入中...
      </div>

      <!-- 空狀態 -->
      <div v-else-if="todos.length === 0" class="p-8 text-center text-gray-500">
        <p>還沒有待辦事項</p>
        <p class="text-sm mt-2">開始新增你的第一個待辦事項吧！</p>
      </div>

      <!-- 待辦事項清單 -->
      <ul v-else class="divide-y divide-gray-200">
        <li
          v-for="todo in todos"
          :key="todo.id"
          class="px-6 py-4 hover:bg-gray-50 transition-colors"
        >
          <!-- 編輯模式 -->
          <div v-if="editingTodo?.id === todo.id" class="flex items-center gap-3">
            <input
              type="checkbox"
              :checked="todo.is_completed"
              disabled
              class="w-5 h-5 rounded border-gray-300 text-gray-900 opacity-50 cursor-not-allowed"
            />
            <input
              v-model="editingTitle"
              type="text"
              maxlength="200"
              class="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-gray-900"
              @keyup.enter="handleSaveEdit(todo)"
              @keyup.esc="cancelEdit"
              autofocus
            />
            <button
              @click="handleSaveEdit(todo)"
              class="px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-medium hover:bg-gray-800"
            >
              保存
            </button>
            <button
              @click="cancelEdit"
              class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200"
            >
              取消
            </button>
          </div>

          <!-- 顯示模式 -->
          <div v-else>
            <div class="flex items-center gap-4">
              <!-- 完成狀態勾選框 -->
              <input
                type="checkbox"
                :checked="todo.is_completed"
                @change="handleToggleComplete(todo)"
                class="w-5 h-5 rounded border-gray-300 text-gray-900 focus:ring-gray-900 cursor-pointer flex-shrink-0"
              />

              <!-- 待辦事項內容 -->
              <div class="flex-1 min-w-0">
                <div
                  :class="[
                    'text-sm font-medium',
                    todo.is_completed ? 'line-through text-gray-400' : 'text-gray-900'
                  ]"
                >
                  {{ todo.title }}
                </div>
                <div class="text-xs text-gray-500 mt-1">
                  {{ formatDate(todo.created_at) }}
                </div>
              </div>

              <!-- 操作按鈕 -->
              <div class="flex items-center gap-2 flex-shrink-0">
                <button
                  @click="startEdit(todo)"
                  class="text-blue-600 hover:text-blue-800 p-1"
                  title="編輯"
                >
                  <Edit2 :size="18" />
                </button>
                <button
                  @click="handleDeleteTodo(todo)"
                  class="text-red-600 hover:text-red-800 p-1"
                  title="刪除"
                >
                  <Trash2 :size="18" />
                </button>
              </div>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { Edit2, Trash2 } from 'lucide-vue-next'
import { todosAPI } from '../api/todos'
import { useToast } from '../composables/useToast'
import { useConfirmDialog } from '../composables/useConfirmDialog'

export default {
  name: 'Todos',
  components: {
    Edit2,
    Trash2
  },
  setup() {
    const toast = useToast()
    const { confirm } = useConfirmDialog()

    // 資料狀態
    const todos = ref([])
    const isLoading = ref(false)
    const isCreating = ref(false)
    const newTodoTitle = ref('')

    // 編輯狀態
    const editingTodo = ref(null)
    const editingTitle = ref('')

    // 載入待辦事項
    const loadTodos = async () => {
      isLoading.value = true
      try {
        const response = await todosAPI.getTodos()
        todos.value = response.data
      } catch (error) {
        toast.error(error.response?.data?.detail || '載入待辦事項失敗')
      } finally {
        isLoading.value = false
      }
    }

    // 建立待辦事項
    const handleCreateTodo = async () => {
      if (!newTodoTitle.value.trim()) return

      isCreating.value = true
      try {
        const response = await todosAPI.createTodo({
          title: newTodoTitle.value.trim()
        })
        todos.value.unshift(response.data)  // 添加到列表開頭
        newTodoTitle.value = ''
        toast.success('待辦事項已新增')
      } catch (error) {
        toast.error(error.response?.data?.detail || '新增待辦事項失敗')
      } finally {
        isCreating.value = false
      }
    }

    // 切換完成狀態
    const handleToggleComplete = async (todo) => {
      const newStatus = !todo.is_completed
      try {
        await todosAPI.toggleComplete(todo.id, newStatus)
        todo.is_completed = newStatus
        toast.success(newStatus ? '已標記為完成' : '已標記為未完成')
      } catch (error) {
        toast.error(error.response?.data?.detail || '更新狀態失敗')
      }
    }

    // 開始編輯
    const startEdit = (todo) => {
      editingTodo.value = todo
      editingTitle.value = todo.title
    }

    // 取消編輯
    const cancelEdit = () => {
      editingTodo.value = null
      editingTitle.value = ''
    }

    // 保存編輯
    const handleSaveEdit = async (todo) => {
      if (!editingTitle.value.trim()) {
        toast.error('待辦事項標題不能為空')
        return
      }

      try {
        await todosAPI.updateTodo(todo.id, {
          title: editingTitle.value.trim()
        })
        todo.title = editingTitle.value.trim()
        toast.success('待辦事項已更新')
        cancelEdit()
      } catch (error) {
        toast.error(error.response?.data?.detail || '更新待辦事項失敗')
      }
    }

    // 刪除待辦事項
    const handleDeleteTodo = async (todo) => {
      const confirmed = await confirm({
        title: '刪除待辦事項',
        message: `確定要刪除「${todo.title}」嗎？此操作無法復原。`,
        type: 'danger'
      })

      if (!confirmed) return

      try {
        await todosAPI.deleteTodo(todo.id)
        todos.value = todos.value.filter(t => t.id !== todo.id)
        toast.success('待辦事項已刪除')
      } catch (error) {
        toast.error(error.response?.data?.detail || '刪除待辦事項失敗')
      }
    }

    // 格式化日期
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleString('zh-TW', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    // 組件掛載時載入資料
    onMounted(() => {
      loadTodos()
    })

    return {
      todos,
      isLoading,
      isCreating,
      newTodoTitle,
      editingTodo,
      editingTitle,
      handleCreateTodo,
      handleToggleComplete,
      startEdit,
      cancelEdit,
      handleSaveEdit,
      handleDeleteTodo,
      formatDate
    }
  }
}
</script>
