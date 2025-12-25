<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <router-view></router-view>
    <Toast />
  </div>
</template>

<script>
import Toast from './components/Toast.vue'

export default {
  name: 'App',
  components: {
    Toast
  }
}
</script>