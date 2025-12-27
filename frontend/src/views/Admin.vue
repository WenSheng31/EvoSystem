<template>
  <div>
    <h1 class="text-2xl font-semibold text-gray-900 mb-6">用戶管理</h1>

    <div class="bg-white rounded border border-gray-200">
      <div class="overflow-x-auto">
        <table class="w-full min-w-[1000px]">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
              >
                用戶名
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
              >
                郵箱
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
              >
                角色
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
              >
                狀態
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
              >
                註冊時間
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase"
              >
                操作
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="u in users" :key="u.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 text-sm font-medium text-gray-900">
                <div class="flex items-center gap-3">
                  <AvatarImage
                    :avatar="u.avatar"
                    :username="u.username"
                    :size="32"
                  />
                  <span>{{ u.username }}</span>
                </div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ u.email }}</td>
              <td class="px-6 py-4 text-sm">
                <span
                  :class="
                    u.role === 'admin'
                      ? 'bg-purple-100 text-purple-700'
                      : 'bg-gray-100 text-gray-700'
                  "
                  class="px-2 py-1 rounded text-xs font-medium"
                >
                  {{ u.role === "admin" ? "管理員" : "普通用戶" }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm">
                <span
                  :class="
                    u.is_active
                      ? 'bg-green-100 text-green-700'
                      : 'bg-red-100 text-red-700'
                  "
                  class="px-2 py-1 rounded text-xs font-medium"
                >
                  {{ u.is_active ? "啟用" : "停用" }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm text-gray-600">
                {{ formatDate(u.created_at) }}
              </td>
              <td class="px-6 py-4 text-sm text-right space-x-2">
                <button
                  v-if="u.id !== user?.id"
                  @click="toggleActive(u)"
                  :class="
                    u.is_active
                      ? 'text-orange-600 hover:text-orange-800'
                      : 'text-green-600 hover:text-green-800'
                  "
                  class="font-medium"
                >
                  {{ u.is_active ? "停用" : "啟用" }}
                </button>
                <button
                  v-if="u.id !== user?.id"
                  @click="handleResetPassword(u)"
                  class="text-blue-600 hover:text-blue-800 font-medium"
                >
                  重置密碼
                </button>
                <button
                  v-if="u.id !== user?.id"
                  @click="confirmDelete(u)"
                  class="text-red-600 hover:text-red-800 font-medium"
                >
                  刪除
                </button>
                <span v-if="u.id === user?.id" class="text-gray-400 text-xs"
                  >（當前帳號）</span
                >
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { authAPI } from "../api/auth";
import { useUser } from "../composables/useUser";
import { useToast } from "../composables/useToast";
import { useConfirmDialog } from "../composables/useConfirmDialog";
import { useInputDialog } from "../composables/useInputDialog";
import { ROUTES } from "../config/constants";
import AvatarImage from "../components/AvatarImage.vue";

export default {
  name: "Admin",
  components: {
    AvatarImage,
  },
  setup() {
    const router = useRouter();
    const { user, fetchUserInfo } = useUser();
    const toast = useToast();
    const { confirm } = useConfirmDialog();
    const { showInput } = useInputDialog();
    const users = ref([]);

    const loadData = async () => {
      try {
        // 獲取當前用戶資訊
        await fetchUserInfo();

        // 檢查是否為管理員
        if (user.value?.role !== "admin") {
          toast.error("需要管理員權限");
          router.push(ROUTES.HOME);
          return;
        }

        // 獲取所有用戶
        const response = await authAPI.getAllUsers();
        users.value = response.data;
      } catch (error) {
        console.error("載入失敗:", error);
        toast.error("載入用戶列表失敗");
      }
    };

    const toggleActive = async (targetUser) => {
      try {
        const response = await authAPI.toggleUserActive(targetUser.id);
        // 更新本地數據
        const index = users.value.findIndex((u) => u.id === targetUser.id);
        if (index !== -1) {
          users.value[index] = response.data;
        }
        toast.success(response.data.is_active ? "已啟用用戶" : "已停用用戶");
      } catch (error) {
        console.error("操作失敗:", error);
        toast.error(error.response?.data?.detail || "操作失敗");
      }
    };

    const confirmDelete = async (targetUser) => {
      const result = await confirm({
        title: "確認刪除",
        message: `確定要刪除用戶 ${targetUser.username} 嗎？此操作無法撤銷！`,
        type: "danger",
      });

      if (result) {
        try {
          await authAPI.deleteUser(targetUser.id);
          users.value = users.value.filter((u) => u.id !== targetUser.id);
          toast.success("用戶已刪除");
        } catch (error) {
          console.error("刪除失敗:", error);
          toast.error(error.response?.data?.detail || "刪除失敗");
        }
      }
    };

    const formatDate = (dateString) => {
      const date = new Date(dateString);
      return date.toLocaleString("zh-TW", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
      });
    };

    const handleResetPassword = async (targetUser) => {
      let isValid = false;
      let password = "";

      // 循環提示直到密碼符合要求或用戶取消
      while (!isValid) {
        const result = await showInput({
          title: "重置用戶密碼",
          type: "password",
          placeholder: "請輸入新密碼",
          hint: "密碼要求：8-50 個字符，需包含字母和數字",
        });

        // 用戶取消
        if (!result.confirmed) return;

        password = result.value;

        // 驗證密碼格式
        if (
          password.length < 8 ||
          password.length > 50 ||
          !/[A-Za-z]/.test(password) ||
          !/\d/.test(password)
        ) {
          toast.error("密碼不符合要求");
          continue;
        }

        // 密碼格式正確
        isValid = true;
      }

      // 調用 API
      try {
        await authAPI.resetUserPassword(targetUser.id, password);
        toast.success("密碼重置成功");
      } catch (error) {
        console.error("重置密碼失敗:", error);
        toast.error(error.response?.data?.detail || "重置密碼失敗");
      }
    };

    onMounted(() => {
      loadData();
    });

    return {
      user,
      users,
      toggleActive,
      confirmDelete,
      formatDate,
      handleResetPassword,
    };
  },
};
</script>
