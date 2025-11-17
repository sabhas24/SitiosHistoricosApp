<template>
  <div class="reviews-section">
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Cargando reseñas...</p>
    </div>

    <EmptyState
      v-else-if="reviews.length === 0"
      title="Aún no escribiste reseñas"
      message="Comienza a explorar sitios históricos y comparte tus experiencias"
      type="reviews"
    />

    <div v-else class="reviews-list">
      <div v-for="review in reviews" :key="review.id" class="review-card">
        <div class="review-header">
          <h3 class="review-site">{{ review.sitio_nombre }}</h3>
          <span class="review-date">{{ formatDate(review.fecha) }}</span>
        </div>
        <RatingStars :rating="review.calificacion" show-value />
        <p class="review-excerpt">{{ review.resena || review.comentario }}</p>
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
  reviews: {
    type: Array,
    required: true
  },
  loading: {
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

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.reviews-section {
  min-height: 400px;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.review-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 20px;
  transition: all 0.2s;
}

.review-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 12px;
  gap: 16px;
}

.review-site {
  margin: 0;
  font-size: 18px;
  color: #1f2937;
  flex: 1;
}

.review-date {
  font-size: 14px;
  color: #6b7280;
  white-space: nowrap;
}

.review-excerpt {
  margin: 12px 0 0 0;
  color: #4b5563;
  font-size: 14px;
  line-height: 1.6;
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
</style>
