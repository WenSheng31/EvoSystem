<template>
  <div>
    <h1 class="text-2xl font-semibold text-gray-900 mb-6">首頁</h1>
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
            歡迎使用EvoSystem，{{ user?.username }}
          </h2>
          <p class="text-sm text-gray-600 mt-1">{{ currentDateTime }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from "vue";
import { useUser } from "../composables/useUser";
import { getAvatarUrl } from "../utils/avatar";

export default {
  name: "Home",
  setup() {
    const { user, fetchUserInfo } = useUser();
    const currentDateTime = ref("");
    let intervalId = null;

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
      intervalId = setInterval(updateDateTime, 1000);
    });

    onUnmounted(() => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    });

    return {
      user,
      currentDateTime,
      getAvatarUrl,
    };
  },
};
</script>
