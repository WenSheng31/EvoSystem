<template>
  <div class="min-h-screen bg-gray-50">
    <Header :user="user" />
    <main class="max-w-5xl mx-auto px-6 py-8">
      <div class="bg-white rounded p-6">
        <div class="flex items-center gap-4">
          <div
            class="w-16 h-16 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden"
          >
            <img
              v-if="user?.avatar"
              :src="getAvatarUrl(user.avatar)"
              alt="Avatar"
              class="w-full h-full object-cover"
            />
            <span v-else class="text-gray-600 font-medium text-2xl">
              {{ user?.username.charAt(0).toUpperCase() }}
            </span>
          </div>
          <div>
            <h2 class="text-xl font-medium text-gray-900">
              歡迎使用本系統，{{ user?.username }}
            </h2>
            <p class="text-sm text-gray-600 mt-1">{{ currentDateTime }}</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { authAPI } from "../api/auth";
import Header from "../components/Header.vue";

export default {
  name: "Home",
  components: {
    Header,
  },
  setup() {
    const router = useRouter();
    const user = ref(null);
    const currentDateTime = ref("");

    const fetchUserInfo = async () => {
      try {
        const response = await authAPI.getCurrentUser();
        user.value = response.data;
      } catch (err) {
        console.error("獲取用戶資訊失敗:", err);
        router.push("/login");
      }
    };

    const getAvatarUrl = (avatarPath) => {
      if (!avatarPath) return null;
      const cleanPath = avatarPath.replace(/\\/g, "/").replace("backend/", "");
      return `http://localhost:8000/${cleanPath}`;
    };

    const updateDateTime = () => {
      const now = new Date();
      const year = now.getFullYear();
      const month = String(now.getMonth() + 1).padStart(2, "0");
      const day = String(now.getDate()).padStart(2, "0");
      const hours = String(now.getHours()).padStart(2, "0");
      const minutes = String(now.getMinutes()).padStart(2, "0");
      const seconds = String(now.getSeconds()).padStart(2, "0");
      currentDateTime.value = `${year}/${month}/${day} ${hours}:${minutes}:${seconds}`;
    };

    onMounted(() => {
      fetchUserInfo();
      updateDateTime();
      setInterval(updateDateTime, 1000);
    });

    return {
      user,
      currentDateTime,
      getAvatarUrl,
    };
  },
};
</script>
