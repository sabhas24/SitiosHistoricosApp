<template>
  <div class="favorites-section">
    <div v-if="loadingFavorites" class="loading-state">
      <div class="spinner"></div>
      <p>Cargando sitios favoritos...</p>
    </div>

    <EmptyState
      v-else-if="favorites.length === 0"
      title="Aún no marcaste ningún sitio como favorito"
      message="Explora sitios históricos y marca tus favoritos"
      type="favorites"
    />

    <div v-else class="favorites-container">
      <div class="favorites-grid">
        <div v-for="site in favorites" :key="site.id" class="favorite-card">
          <div class="favorite-image">
            <img :src="site.image" :alt="site.name" loading="lazy"/>
            <span class="favorite-badge">♡</span>
          </div>
          <div class="favorite-content">
            <h3 class="favorite-name">{{ site.name }}</h3>
            <p class="favorite-location">{{ site.location }}</p>
            <RatingStars :rating="Math.round(site.rating)" />
            <router-link :to="`/sitio/${site.id}`" class="btn-visit">Ver Sitio</router-link>
          </div>
        </div>
      </div>

      <Pagination
        :current-page="currentPage"
        :total-pages="totalPages"
        @prev="$emit('prev-page')"
        @next="$emit('next-page')"
      />
    </div>

    <div v-if="error" class="error-message">
      <svg class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <circle cx="12" cy="12" r="10"/>
        <path d="M12 8v4M12 16h.01"/>
      </svg>
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import RatingStars from './RatingStars.vue'
import EmptyState from './EmptyState.vue'
import Pagination from './Pagination.vue'

defineProps({
  favorites: {
    type: Array,
    required: true
  },
  loadingFavorites: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  },
  currentPage: {
    type: Number,
    required: true
  },
  totalPages: {
    type: Number,
    required: true
  }
})

defineEmits(['prev-page', 'next-page'])
</script>

<style scoped>
.favorites-section {
  min-height: 400px;
}

.favorites-container {
  display: flex;
  flex-direction: column;
}

.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.favorite-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s;
}

.favorite-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.favorite-image {
  position: relative;
  width: 100%;
  height: 200px;
  background: #f3f4f6;
  overflow: hidden;
}

.favorite-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.favorite-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 36px;
  height: 36px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: #D4AF37;
}

.favorite-content {
  padding: 16px;
}

.favorite-name {
  margin: 0 0 4px 0;
  font-size: 16px;
  color: #1f2937;
  font-weight: 600;
}

.favorite-location {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #6b7280;
}

.btn-visit {
  display: inline-block;
  width: 100%;
  padding: 8px 12px;
  background: #8B7355;
  color: white;
  border-radius: 6px;
  text-align: center;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s;
  margin-top: 8px;
  box-sizing: border-box;
}

.btn-visit:hover {
  background: #704a3a;
  text-decoration: none;
}

.loading-state {
  text-align: center;
  padding: 48px 24px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e5e7eb;
  border-top-color: #8B7355;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-state p {
  color: #6b7280;
  margin: 0;
}

.error-message {
  background: #fee2e2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 24px;
}

.error-icon {
  width: 20px;
  height: 20px;
  color: #dc2626;
  flex-shrink: 0;
}

.error-message p {
  margin: 0;
  color: #dc2626;
  font-size: 14px;
}

@media (max-width: 768px) {
  .favorites-grid {
    grid-template-columns: 1fr;
  }
}
</style>
