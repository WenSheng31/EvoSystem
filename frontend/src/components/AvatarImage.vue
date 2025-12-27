<template>
  <div
    class="rounded-full bg-gray-200 flex items-center justify-center overflow-hidden flex-shrink-0"
    :style="{ width: `${size}px`, height: `${size}px` }"
  >
    <img
      v-if="avatar"
      :src="getAvatarUrl(avatar)"
      :alt="alt"
      class="w-full h-full object-cover"
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
import { computed } from 'vue'
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
      default: 'Avatar'
    }
  },
  setup(props) {
    const displayLetter = computed(() => {
      return props.username ? props.username.charAt(0).toUpperCase() : '?'
    })

    return {
      displayLetter,
      getAvatarUrl
    }
  }
}
</script>
