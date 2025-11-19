<template>
  <section class="site-reviews">
    <h2>Reseñas y Calificaciones</h2>

    <div v-if="loading">Cargando reseñas...</div>
    <div v-else>
      <div class="actions" v-if="isAuthenticated">
        <button @click="openForm" class="btn-primary">
          {{ myReview ? (editing ? 'Cancelar' : (myReview ? 'Editar mi reseña' : 'Escribir reseña')) : 'Escribir reseña' }}
        </button>
      </div>

      <div v-if="showForm">
        <form @submit.prevent="submitReview" class="review-form">
          <label>Calificación</label>
          <RatingInput v-model="form.rating" />

          <label>Comentario</label>
          <textarea v-model="form.comment" rows="5" />

          <div class="form-actions">
            <button type="submit" class="btn-primary">{{ editing ? 'Guardar cambios' : 'Enviar reseña' }}</button>
            <button type="button" v-if="editing" @click="confirmDelete" class="btn-danger">Eliminar reseña</button>
            <button type="button" @click="closeForm" class="btn-secondary">Cancelar</button>
          </div>

          <p class="note" v-if="statusMessage">{{ statusMessage }}</p>
        </form>
      </div>

      <div v-if="reviews.length === 0" class="no-reviews">Aún no hay reseñas aprobadas para este sitio.</div>

      <ul class="reviews-list">
        <li v-for="r in reviews" :key="r.id" class="review-card">
          <div class="review-header">
            <strong>{{ r.author_name || 'Anónimo' }}</strong>
            <span class="rating">{{ r.rating }} ★</span>
          </div>
          <p class="review-comment">{{ r.comment }}</p>
          <div class="review-meta">{{ formatDate(r.inserted_at) }}</div>
          <div class="review-actions" v-if="isAuthenticated && myReview && myReview.id === r.id">
            <button @click="startEdit(r)" class="btn-link">Editar</button>
            <button @click="confirmDelete" class="btn-link danger">Eliminar</button>
          </div>
        </li>
      </ul>
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
    return new Date(iso).toLocaleString()
  } catch (e) {
    void e
    return iso
  }
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
    // prefill if user has a review
    if (myReview.value) {
      form.value.rating = myReview.value.rating
      form.value.comment = myReview.value.comment
    }
  } catch (err) {
    // 404 means no review yet
    if (err.response && err.response.status === 404) {
      myReview.value = null
    } else if (err.response && err.response.status === 401) {
      // Session expired or invalid — clear local auth state but do not force a redirect here
      try {
        auth.clearUser()
      } catch (e) { void e }
      myReview.value = null
      isAuthenticated.value = false
    } else {
      console.error('Error loading my review', err)
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
  // client-side validation
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
      statusMessage.value = 'Reseña actualizada. Puede quedar pendiente de moderación.'
    } else {
      await reviewsService.createReview(props.siteId, form.value.rating, form.value.comment)
      statusMessage.value = 'Reseña creada. Queda pendiente de moderación.'
    }
    await loadReviews()
    await loadMyReview()
    editing.value = false
    showForm.value = false
  } catch (err) {
    console.error('Error submitting review', err)
    statusMessage.value = err.response?.data?.error?.message || 'No se pudo enviar la reseña.'
  }
}

async function confirmDelete() {
  if (!confirm('¿Eliminar tu reseña? Esta acción no se puede deshacer.')) return
  try {
    if (!myReview.value) return
    await reviewsService.deleteReview(props.siteId, myReview.value.id)
    statusMessage.value = 'Reseña eliminada.'
    await loadReviews()
    myReview.value = null
    showForm.value = false
  } catch (err) {
    console.error('Error deleting review', err)
    statusMessage.value = err.response?.data?.error?.message || 'No se pudo eliminar la reseña.'
  }
}
</script>

<style scoped>
.site-reviews { margin-top: 32px }
.review-form { display:flex; flex-direction:column; gap:8px; margin-bottom:16px }
.form-actions { display:flex; gap:8px; margin-top:8px }
.btn-primary { background:#667eea; color:#fff; border:none; padding:8px 12px; border-radius:6px }
.btn-secondary { background:#fff; border:1px solid #ccc; padding:8px 12px; border-radius:6px }
.btn-danger, .btn-link.danger { color:#dc2626; background:transparent; border:none }
.reviews-list { list-style:none; padding:0; display:flex; flex-direction:column; gap:12px }
.review-card { padding:12px; border-radius:8px; background:#fff; box-shadow:0 1px 3px rgba(0,0,0,0.06) }
.review-header { display:flex; justify-content:space-between; align-items:center }
.rating { color:#f59e0b }
.no-reviews { color:#6b7280 }
.note { color:#374151; font-size:0.95rem }

/* New styles for edit/delete actions */
.review-actions {
  margin-top: 10px;
  display: flex;
  gap: 8px;
  align-items: center;
}
.btn-link {
  background: transparent;
  border: 1px solid transparent;
  padding: 6px 10px;
  border-radius: 8px;
  color: #4b5563;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
  font-size: 0.9rem;
}
.btn-link:hover {
  background: #f3f4f6;
  color: #111827;
  border-color: #e5e7eb;
}
.btn-link.danger {
  color: #b91c1c;
  border-color: transparent;
}
.btn-link.danger:hover {
  background: rgba(239,68,68,0.06);
  border-color: rgba(239,68,68,0.12);
  color: #991b1b;
}

/* Ensure small buttons look good on mobile */
@media (max-width: 600px) {
  .review-header { flex-direction: column; align-items: flex-start; gap: 8px }
  .review-actions { gap: 6px }
  .btn-link { padding: 6px 8px; font-size: 0.85rem }
}
</style>
