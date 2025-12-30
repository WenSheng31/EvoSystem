<template>
  <div
    class="rounded-full bg-gray-200 flex items-center justify-center overflow-hidden flex-shrink-0"
    :style="{ width: `${size}px`, height: `${size}px` }"
  >
    <img
      v-if="avatarUrl"
      :src="avatarUrl"
      :alt="alt"
      class="w-full h-full object-cover"
      @error="handleError"
    />
    <span
      v-else
      class="text-gray-600 font-medium"
      :style="{ fontSize: `${size / 2.5}px` }"
    >
      {{ displayLetter }}
    </span>
  </div>
</template>

<script>
import { computed, ref } from 'vue'
import { getAvatarUrl } from '../utils/avatar'

export default {
  name: 'AvatarImage',
  props: {
    avatar: {
      type: String,
      default: null
    },
    username: {
      type: String,
      default: ''
    },
    size: {
      type: Number,
      default: 40
    },
    alt: {
      type: String,
      default: '頭像'
    }
  },
  setup(props) {
    const imageError = ref(false)

    const avatarUrl = computed(() => {
      if (imageError.value || !props.avatar) return null
      return getAvatarUrl(props.avatar)
    })

    const displayLetter = computed(() => {
      return props.username ? props.username.charAt(0).toUpperCase() : '?'
    })

    const handleError = () => {
      imageError.value = true
    }

    return {
      avatarUrl,
      displayLetter,
      handleError
    }
  }
}
</script>
