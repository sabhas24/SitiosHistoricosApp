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
          <div class="header-right">
             <span class="review-date">{{ formatDate(review.fecha_creacion) }}</span>
             <div class="status-badge" :class="review.estado.toLowerCase()">
               {{ formatStatus(review.estado) }}
             </div>
             <div class="actions">
                <button @click="editReview(review)" class="btn-icon edit" title="Editar">✎</button>
                <button @click="deleteReview(review)" class="btn-icon delete" title="Eliminar">🗑️</button>
             </div>
          </div>
        </div>
        <RatingStars :rating="review.calificacion" show-value />
        <p class="review-excerpt">{{ review.resena || review.comentario }}</p>
        
        <!-- Rejection Notice -->
        <div v-if="review.estado === 'Rechazada'" class="rejection-notice">
          <div class="notice-header">
            <span class="icon">⚠️</span>
            <strong>Tu reseña fue rechazada</strong>
          </div>
          <p class="rejection-reason" v-if="review.motivo_rechazo">
            Motivo: {{ review.motivo_rechazo }}
          </p>
          <p class="rejection-help">Puedes editarla para corregir los problemas señalados.</p>
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

import { useRouter } from 'vue-router'
import reviewsService from '../../services/reviewsService'

const emit = defineEmits(['prev-page', 'next-page', 'review-deleted'])

const router = useRouter()

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatStatus = (status) => {
  const map = {
    'Pendiente': 'Pendiente',
    'Aprobada': 'Publicada',
    'Rechazada': 'Rechazada'
  }
  return map[status] || status
}

const editReview = (review) => {
  router.push({
    path: `/sitio/${review.sitio_id}`,
    query: { edit: 'true' }
  })
}

const deleteReview = async (review) => {
  if (!confirm('¿Estás seguro de que quieres eliminar esta reseña?')) return
  
  try {
    
    await reviewsService.deleteReview(review.sitio_id || review.site_id, review.id)
    emit('review-deleted') 
  } catch (e) {
    console.error(e)
    alert('No se pudo eliminar la reseña.')
  }
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

.header-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.btn-icon:hover {
  background-color: #f3f4f6;
}

.btn-icon.delete:hover {
  background-color: #fee2e2;
}

/* Status Badges */
.status-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  margin-bottom: 4px;
}

.status-badge.pendiente {
  background-color: #fff7ed;
  color: #c2410c;
  border: 1px solid #fdba74;
}

.status-badge.aprobada {
  background-color: #f0fdf4;
  color: #15803d;
  border: 1px solid #86efac;
}

.status-badge.rechazada {
  background-color: #fef2f2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

/* Rejection Notice */
.rejection-notice {
  margin-top: 12px;
  padding: 12px;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
  font-size: 14px;
}

.notice-header {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #991b1b;
  margin-bottom: 4px;
}

.rejection-reason {
  margin: 4px 0;
  color: #7f1d1d;
  font-style: italic;
}

.rejection-help {
  margin: 4px 0 0 0;
  font-size: 12px;
  color: #991b1b;
}
</style>
