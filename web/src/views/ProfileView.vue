<template>
  <div class="profile-container">
    <!-- Header con info del usuario -->
    <ProfileHeader 
      :user-name="authStore.userName" 
      :user-email="authStore.userEmail"
    />

    <!-- Tabs Navigation -->
    <div class="tabs-container">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        :class="['tab-button', { active: activeTab === tab.id }]"
        @click="activeTab = tab.id"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Contenido de Tabs -->
    <div class="tabs-content">
      <!-- Mis Reseñas -->
      <ReviewsSection
        v-if="activeTab === 'reviews'"
        :reviews="reviews"
        :loading="loading"
        :error="error"
        :current-page="currentPage"
        :total-pages="totalPages"
        @prev-page="previousPage('reviews')"
        @next-page="nextPage('reviews')"
      />

      <!-- Mis Sitios Favoritos -->
      <FavoritesSection
        v-if="activeTab === 'favorites'"
        :favorites="favorites"
        :loading-favorites="loadingFavorites"
        :error="errorFavorites"
        :current-page="currentPageFavorites"
        :total-pages="totalPagesFavorites"
        @prev-page="previousPage('favorites')"
        @next-page="nextPage('favorites')"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { profileService } from '../services/profileService'
import ProfileHeader from '../components/profile/ProfileHeader.vue'
import ReviewsSection from '../components/profile/ReviewsSection.vue'
import FavoritesSection from '../components/profile/FavoritesSection.vue'

const router = useRouter()
const authStore = useAuthStore()

const activeTab = ref('reviews')
const reviews = ref([])
const favorites = ref([])
const currentPage = ref(1)
const currentPageFavorites = ref(1)
const totalPages = ref(1)
const totalPagesFavorites = ref(1)
const loading = ref(false)
const loadingFavorites = ref(false)
const error = ref(null)
const errorFavorites = ref(null)

const tabs = [
  { id: 'reviews', label: 'Mis Reseñas' },
  { id: 'favorites', label: 'Sitios Favoritos' }
]

if (!authStore.isAuthenticated) {
  router.push('/login')
}

onMounted(async () => {
  await loadReviews()
})

const loadReviews = async () => {
  loading.value = true
  error.value = null
  try {
    const data = await profileService.getReviews(currentPage.value, 25, 'lasted')
    reviews.value = data.items
    totalPages.value = data.totalPages
  } catch (err) {
    console.error('[v0] Error loading reviews:', err)
    error.value = 'No pudimos cargar tus reseñas. Intenta nuevamente.'
  } finally {
    loading.value = false
  }
}

const loadFavorites = async () => {
  loadingFavorites.value = true
  errorFavorites.value = null
  try {
    const data = await profileService.getFavorites(currentPageFavorites.value, 25, 'lasted')
    favorites.value = data.items
    totalPagesFavorites.value = data.totalPages
  } catch (err) {
    console.error('[v0] Error loading favorites:', err)
    errorFavorites.value = 'No pudimos cargar tus sitios favoritos. Intenta nuevamente.'
  } finally {
    loadingFavorites.value = false
  }
}

const nextPage = async (section) => {
  if (section === 'reviews' && currentPage.value < totalPages.value) {
    currentPage.value++
    await loadReviews()
  } else if (section === 'favorites' && currentPageFavorites.value < totalPagesFavorites.value) {
    currentPageFavorites.value++
    await loadFavorites()
  }
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const previousPage = async (section) => {
  if (section === 'reviews' && currentPage.value > 1) {
    currentPage.value--
    await loadReviews()
  } else if (section === 'favorites' && currentPageFavorites.value > 1) {
    currentPageFavorites.value--
    await loadFavorites()
  }
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

watch(activeTab, (newTab) => {
  if (newTab === 'favorites' && favorites.value.length === 0 && !loadingFavorites.value) {
    loadFavorites()
  }
})
</script>

<style scoped>
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 16px;
}

.tabs-container {
  display: flex;
  gap: 8px;
  margin-bottom: 32px;
  border-bottom: 2px solid #e5e7eb;
  overflow-x: auto;
}

.tab-button {
  padding: 12px 16px;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  color: #6b7280;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.tab-button:hover {
  color: #8B7355;
}

.tab-button.active {
  color: #8B7355;
  border-bottom-color: #8B7355;
}

.tabs-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .profile-container {
    padding: 16px 12px;
  }

  .tabs-container {
    margin-bottom: 24px;
  }

  .tab-button {
    padding: 10px 12px;
    font-size: 14px;
  }
}
</style>
