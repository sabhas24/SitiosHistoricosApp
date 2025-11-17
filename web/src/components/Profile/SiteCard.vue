<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden transition-all duration-200 hover:shadow-md hover:-translate-y-1 cursor-pointer h-full flex flex-col" @click="navigateToSite">
    <div class="relative w-full h-48 overflow-hidden">
      <img
        :src="minioImg(site.image, 'placeholder-image.jpg')"
        :alt="site.name"
        loading="lazy"
        @error="handleImageError"
        class="w-full h-full object-cover"
      />
    </div>
    <div class="p-4 flex-1 flex flex-col gap-2">
      <h3 class="text-lg font-semibold text-gray-900 line-clamp-1">{{ site.name }}</h3>
      <p class="text-sm text-gray-600">{{ formatLocation(site) }}</p>
      <div v-if="site.rating" class="flex items-center gap-2 mt-auto">
        <div class="flex gap-1">
          <span v-for="n in 5" :key="n" class="text-xs" :class="n <= site.rating ? 'text-yellow-400' : 'text-gray-300'">
            ⭐
          </span>
        </div>
        <span class="text-sm font-medium text-gray-700">{{ site.rating.toFixed(1) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { minioImg } from '../../utils/minioImages.js'

const props = defineProps({
  site: {
    type: Object,
    required: true
  }
})

const navigateToSite = () => {
  // IMPLEMENTAR NAVEGACIONA DETALLE DEL SITIO CUANDO ESTE
  console.log('Ver detalle del sitio:', props.site.name)
}

const handleImageError = (event) => {
  event.target.src = minioImg('placeholder-image.jpg')
}

const formatLocation = (site) => {
  const parts = []
  if (site.city) parts.push(site.city)
  if (site.province) parts.push(site.province)
  return parts.join(', ')
}
</script>
