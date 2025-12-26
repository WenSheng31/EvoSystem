<template>
  <header
    class="fixed top-0 left-0 right-0 h-16 bg-white border-b border-gray-200 z-30 lg:hidden"
  >
    <div class="h-full px-4 flex items-center justify-between">
      <button
        @click="$emit('toggle-sidebar')"
        class="p-2 hover:bg-gray-100 rounded"
      >
        <svg
          class="w-6 h-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
      </button>
      <img src="/logo/main_nobk_b.png" alt="EvoSystem" class="h-7 w-auto" />
    </div>
  </header>
</template>

<script>
export default {
  name: "AppHeader",
  emits: ["toggle-sidebar"],
};
</script>
