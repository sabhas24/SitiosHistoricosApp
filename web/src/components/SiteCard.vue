<template>
  <div class="site-card" @click="navigateToSite">
    <div class="card-image">
      <img 
        :src="minioImg(site.image, 'placeholder-image.jpg')" 
        :alt="site.name"
        loading="lazy"
        @error="handleImageError"
      />
    </div>
    <div class="card-content">
      <h3 class="site-name">{{ site.name }}</h3>
      <p class="site-location">{{ formatLocation(site) }}</p>
      <div v-if="site.rating" class="rating">
        <div class="stars">
          <span v-for="n in 5" :key="n" class="star" :class="{ filled: n <= site.rating }">
            ⭐
          </span>
        </div>
        <span class="rating-value">{{ site.rating.toFixed(1) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { minioImg } from '../utils/minioImages.js'

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

<style scoped>
.site-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.site-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.card-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-content {
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.site-name {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
  color: #2c3e50;
  line-height: 1.4;
}

.site-location {
  color: #6b7280;
  font-size: 0.9rem;
  margin: 0;
}

.rating {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: auto;
}

.stars {
  display: flex;
  gap: 2px;
}

.star {
  font-size: 0.8rem;
  filter: grayscale(1);
  opacity: 0.3;
}

.star.filled {
  filter: none;
  opacity: 1;
}

.rating-value {
  font-size: 0.9rem;
  font-weight: 500;
  color: #374151;
}

@media (max-width: 640px) {
  .card-image {
    height: 160px;
  }
  
  .card-content {
    padding: 12px;
  }
  
  .site-name {
    font-size: 1rem;
  }
}
</style>
