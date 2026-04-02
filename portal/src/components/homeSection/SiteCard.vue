<template>
  <article class="site-card" @click="navigateToSite">
    <div class="card-image-wrapper">
      <img 
        :src="minioImg(site.imagen_principal || site.image, 'placeholder-image.jpg')" 
        :alt="site.nombre || site.name"
        loading="lazy"
        @error="handleImageError"
      />
    </div>
    <div class="card-content">
      <h3 class="site-name">{{ site.nombre || site.name }}</h3>
      <p class="site-location">{{ formatLocation(site) }}</p>
      <p v-if="site.descripcion_breve" class="site-description">
        {{ site.descripcion_breve }}
      </p>
      <div v-if="site.calificacion_promedio || site.rating" class="rating">
        <div class="stars" aria-hidden="true">
          <span v-for="n in 5" :key="n" class="star" :class="{ filled: n <= Math.round(site.calificacion_promedio || site.rating || 0) }">
            ★
          </span>
        </div>
        <span class="rating-value">{{ ((site.calificacion_promedio || site.rating || 0)).toFixed(1) }}</span>
        <span class="sr-only">Calificación: {{ ((site.calificacion_promedio || site.rating || 0)).toFixed(1) }} de 5</span>
      </div>
    </div>
  </article>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { minioImg } from '../../utils/minioImages'

const router = useRouter()

const props = defineProps({
  site: {
    type: Object,
    required: true
  }
})

const navigateToSite = () => {
  
  router.push(`/sitio/${props.site.id}`)
}

const handleImageError = (event) => {
  event.target.src = minioImg('placeholder-image.jpg')
}

const formatLocation = (site) => {
  const parts = []
  if (site.ciudad || site.city) parts.push(site.ciudad || site.city)
  if (site.provincia || site.province) parts.push(site.provincia || site.province)
  
  let location = parts.join(', ')
  
  if (site.visitas !== undefined && site.visitas !== null) {
    const visitsText = site.visitas === 1 ? '1 visita' : `${site.visitas} visitas`
    location += ` • ${visitsText}`
  }
  
  return location
}
</script>

<style scoped>
.site-card {
  background: white;
  border: 1px solid #e5e7eb;  
  border-radius: 8px; 
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.site-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: #d1d5db;
  scale: 1.04;
}

.card-image-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 4/3; /* Consistent aspect ratio */
  overflow: hidden;
  background: #f3f4f6;
  border-bottom: 1px solid #f3f4f6;
}

.card-image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

 .card-image-wrapper img {
  transform: scale(1.05);
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
  color: #111827;
  line-height: 1.3;
}

.site-location {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}

.site-description {
  font-size: 0.875rem;
  color: #4b5563;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.5;
}

.rating {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: auto;
  padding-top: 8px;
}

.stars {
  display: flex;
  gap: 1px;
}

.star {
  font-size: 1rem;
  color: #d1d5db;
  line-height: 1;
}

.star.filled {
  color: #fbbf24; 
}

.rating-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

/* Responsive styles */
@media (max-width: 768px) {
  .site-card {
    max-width: 100%;
  }
  
  .site-name {
    font-size: 1rem;
  }
  
  .site-location,
  .site-description,
  .rating-value {
    font-size: 0.8rem;
  }
  
  .card-content {
    padding: 12px;
  }
}

@media (max-width: 480px) {
  .site-card:hover {
    transform: none; 
  }
  
  .site-card:hover .card-image-wrapper img {
    transform: none;
  }
  
  .card-content {
    padding: 10px;
  }
  
  .site-name {
    font-size: 0.95rem;
  }
  
  .rating {
    gap: 4px;
  }
  
  .star {
    font-size: 0.9rem;
  }
}
</style>
