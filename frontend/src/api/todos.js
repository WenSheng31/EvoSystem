import api from './auth'

export const todosAPI = {
  // 獲取所有待辦事項
  getTodos() {
    return api.get('/todos')
  },

  // 建立待辦事項
  createTodo(todoData) {
    return api.post('/todos', todoData)
  },

  // 更新待辦事項
  updateTodo(todoId, todoData) {
    return api.patch(`/todos/${todoId}`, todoData)
  },

  // 刪除待辦事項
  deleteTodo(todoId) {
    return api.delete(`/todos/${todoId}`)
  },

  // 切換完成狀態（便捷方法）
  toggleComplete(todoId, isCompleted) {
    return api.patch(`/todos/${todoId}`, { is_completed: isCompleted })
  }
}
