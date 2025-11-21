<template>
  <section class="site-reviews">
    <div class="reviews-header">
      <h2>Reseñas de la Comunidad</h2>
      <div v-if="isAuthenticated && !showForm && !myReview">
        <button @click="openForm" class="btn-primary">
          <span class="icon">✎</span>
          Escribir reseña
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
    </div>

    <div v-else>
      <!-- Review Form -->
      <div v-if="showForm" class="review-form-container">
        <h3>{{ editing ? 'Editar tu reseña' : 'Comparte tu experiencia' }}</h3>
        <form @submit.prevent="submitReview" class="review-form">
          <div class="form-group">
            <label>Calificación</label>
            <RatingInput v-model="form.rating" />
          </div>

          <div class="form-group">
            <label>Comentario</label>
            <textarea 
              v-model="form.comment" 
              rows="4" 
              placeholder="¿Qué te pareció este sitio? Cuéntanos más..."
            ></textarea>
            <p class="hint">Mínimo 20 caracteres.</p>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary">
              {{ editing ? 'Guardar cambios' : 'Publicar reseña' }}
            </button>
            <button type="button" @click="closeForm" class="btn-secondary">
              Cancelar
            </button>
            <button v-if="editing" type="button" @click="confirmDelete" class="btn-danger">
              Eliminar
            </button>
          </div>

          <div v-if="statusMessage" class="status-message">
            {{ statusMessage }}
          </div>
        </form>
      </div>

      <!-- Empty State -->
      <div v-if="reviews.length === 0 && !showForm" class="empty-state">
        <div class="empty-icon">💬</div>
        <h3>No hay reseñas aún</h3>
        <p>Sé el primero en compartir tu opinión sobre este sitio.</p>
        <div class="mt-action" v-if="isAuthenticated">
          <button @click="openForm" class="btn-primary">Escribir reseña</button>
        </div>
        <div class="mt-action" v-else>
          <a href="/login" class="link-primary">Inicia sesión para escribir una reseña</a>
        </div>
      </div>

      <!-- Reviews List -->
      <div v-else class="reviews-grid">
        <div v-for="r in reviews" :key="r.id" class="review-card">
          <div class="review-content-wrapper">
            <div class="avatar-wrapper">
              <div class="avatar">
                {{ getInitials(r.author_name) }}
              </div>
            </div>
            <div class="review-main">
              <div class="review-top">
                <p class="author-name">
                  {{ r.author_name || 'Usuario Anónimo' }}
                </p>
                <div class="user-actions" v-if="isAuthenticated && myReview && myReview.id === r.id">
                  <button @click="startEdit(r)" class="btn-icon" title="Editar">
                    ✎
                  </button>
                </div>
              </div>
              <div class="rating-row">
                <div class="stars">
                  <span v-for="i in 5" :key="i" class="star" :class="{ filled: i <= r.rating }">★</span>
                </div>
                <span class="date">{{ formatDate(r.inserted_at) }}</span>
              </div>
              <div class="review-text">
                {{ r.comment }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
<script setup>
import { ref, onMounted, watch } from 'vue'
import RatingInput from './RatingInput.vue'
import reviewsService from '../services/reviewsService'
import { useAuthStore } from '../stores/auth'

const props = defineProps({ siteId: { type: [Number, String], required: true } })

const auth = useAuthStore()
const isAuthenticated = ref(!!auth.isAuthenticated)
watch(() => auth.isAuthenticated, (v) => (isAuthenticated.value = !!v))

const reviews = ref([])
const myReview = ref(null)
const loading = ref(false)
const showForm = ref(false)
const editing = ref(false)
const statusMessage = ref('')

const form = ref({ rating: 5, comment: '' })

function formatDate(iso) {
  try {
    return new Date(iso).toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' })
  } catch (e) {
    return iso
  }
}

function getInitials(name) {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase()
}

async function loadReviews() {
  loading.value = true
  try {
    const data = await reviewsService.getPublicReviews(props.siteId, 1, 20)
    reviews.value = data.data || []
  } catch (err) {
    console.error('Error loading reviews', err)
  } finally {
    loading.value = false
  }
}

async function loadMyReview() {
  if (!isAuthenticated.value) { myReview.value = null; return }
  try {
    const data = await reviewsService.getMyReview(props.siteId)
    myReview.value = data
    if (myReview.value) {
      form.value.rating = myReview.value.rating
      form.value.comment = myReview.value.comment
    }
  } catch (err) {
    if (err.response && err.response.status === 404) {
      myReview.value = null
    } else if (err.response && err.response.status === 401) {
      try { auth.clearUser() } catch (e) {}
      myReview.value = null
      isAuthenticated.value = false
    }
  }
}

onMounted(async () => {
  await loadReviews()
  await loadMyReview()
})

function openForm() {
  if (!isAuthenticated.value) {
    window.location.href = '/login'
    return
  }
  showForm.value = true
  editing.value = !!myReview.value
  statusMessage.value = ''
}

function closeForm() {
  showForm.value = false
  statusMessage.value = ''
}

function startEdit(review) {
  editing.value = true
  showForm.value = true
  form.value.rating = review.rating
  form.value.comment = review.comment
}

async function submitReview() {
  statusMessage.value = ''
  const r = form.value.rating
  const c = (form.value.comment || '').trim()
  const errors = []
  if (!r || r < 1 || r > 5) errors.push('La calificación debe ser entre 1 y 5')
  if (!c || c.length < 20) errors.push('El comentario debe tener al menos 20 caracteres')
  if (c.length > 1000) errors.push('El comentario debe tener como máximo 1000 caracteres')
  if (errors.length) { statusMessage.value = errors.join('. '); return }

  try {
    if (editing.value && myReview.value) {
      await reviewsService.updateReview(props.siteId, myReview.value.id, form.value.rating, form.value.comment)
      statusMessage.value = 'Reseña actualizada.'
    } else {
      await reviewsService.createReview(props.siteId, form.value.rating, form.value.comment)
      statusMessage.value = 'Reseña creada.'
    }
    await loadReviews()
    await loadMyReview()
    editing.value = false
    showForm.value = false
  } catch (err) {
    statusMessage.value = err.response?.data?.error?.message || 'No se pudo enviar la reseña.'
  }
}

async function confirmDelete() {
  if (!confirm('¿Eliminar tu reseña?')) return
  try {
    if (!myReview.value) return
    await reviewsService.deleteReview(props.siteId, myReview.value.id)
    statusMessage.value = 'Reseña eliminada.'
    await loadReviews()
    myReview.value = null
    showForm.value = false
  } catch (err) {
    statusMessage.value = err.response?.data?.error?.message || 'No se pudo eliminar la reseña.'
  }
}
</script>

<style scoped>
.site-reviews {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

.reviews-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.reviews-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

/* Buttons */
.btn-primary {
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #4338ca;
}

.btn-secondary {
  padding: 0.5rem 1rem;
  background-color: white;
  color: #374151;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-secondary:hover {
  background-color: #f9fafb;
}

.btn-danger {
  padding: 0.5rem 1rem;
  background-color: #fee2e2;
  color: #b91c1c;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  margin-left: auto;
}

.btn-danger:hover {
  background-color: #fecaca;
}

.icon {
  margin-right: 0.5rem;
}

/* Loading */
.loading-container {
  display: flex;
  justify-content: center;
  padding: 3rem 0;
}

.spinner {
  width: 2rem;
  height: 2rem;
  border: 2px solid #e5e7eb;
  border-top-color: #4f46e5;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Form */
.review-form-container {
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.review-form-container h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  margin-top: 0;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.25rem;
}

textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-family: inherit;
  font-size: 0.875rem;
  resize: vertical;
}

textarea:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.hint {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.status-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #eff6ff;
  color: #1e40af;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 3rem;
  background-color: #f9fafb;
  border: 1px dashed #d1d5db;
  border-radius: 0.75rem;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #9ca3af;
}

.empty-state h3 {
  font-size: 0.875rem;
  font-weight: 500;
  color: #111827;
  margin: 0 0 0.25rem 0;
}

.empty-state p {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
}

.mt-action {
  margin-top: 1.5rem;
}

.link-primary {
  color: #4f46e5;
  font-weight: 500;
  font-size: 0.875rem;
  text-decoration: none;
}

.link-primary:hover {
  text-decoration: underline;
}

/* Reviews List */
.reviews-grid {
  display: grid;
  gap: 1.5rem;
}

.review-card {
  background-color: white;
  border: 1px solid #f3f4f6;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.2s;
}

.review-card:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.review-content-wrapper {
  display: flex;
  gap: 1rem;
}

.avatar-wrapper {
  flex-shrink: 0;
}

.avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.875rem;
}

.review-main {
  flex: 1;
  min-width: 0;
}

.review-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.author-name {
  font-size: 0.875rem;
  font-weight: 500;
  color: #111827;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.btn-icon {
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: 0.25rem;
  font-size: 1rem;
  transition: color 0.2s;
}

.btn-icon:hover {
  color: #4f46e5;
}

.rating-row {
  display: flex;
  align-items: center;
  margin-top: 0.25rem;
}

.stars {
  display: flex;
  color: #d1d5db;
}

.star {
  font-size: 1rem;
}

.star.filled {
  color: #facc15;
}

.date {
  margin-left: 0.5rem;
  font-size: 0.75rem;
  color: #6b7280;
}

.review-text {
  margin-top: 0.75rem;
  font-size: 0.875rem;
  line-height: 1.5;
  color: #4b5563;
}
</style>
