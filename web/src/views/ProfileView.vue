<template>
  <div class="profile-container" >
    <button @click="goBack" class="back-button">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="back-icon">
        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
      </svg>
      Volver
    </button>
    <!-- Header con info del usuario -->
    <ProfileHeader 
      v-if="authStore.user"
      :user-name="authStore.userName" 
      :user-email="authStore.userEmail"
      :profile-picture="userProfilePicture"
      :profile-color="profileColor"
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
import { ref, onMounted, watch, computed } from 'vue'
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
const profileColor = ref('#8B7355')

const goBack = () => {
  router.go(-1)
}

function getProfileColor(user) {
  const paleta = [
    "#d32f2f", "#c2185b", "#7b1fa2", "#512da8", "#303f9f", 
    "#1976d2", "#0288d1", "#0097a7", "#00796b", "#388e3c", 
    "#689f38", "#afb42b", "#fbc02d", "#ffa000", "#f57c00", 
    "#e64a19", "#5d4037", "#616161"
  ];
  let name = user?.userName || user?.userEmail || "anonimo";
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  const index = Math.abs(hash % paleta.length);
  return paleta[index];
}

const userProfilePicture = computed(() => {
  const pic = authStore.user?.profile_picture || '' 
  console.log('URL de imagen detectada:', pic)
  return pic
})
onMounted(async () => {
  profileColor.value = getProfileColor(authStore)
  console.log('ProfileView - user:', authStore.user.value)
  console.log('ProfileView - user profile_picture:', authStore.user.value?.profile_picture)
  await loadReviews()
})

const tabs = [
  { id: 'reviews', label: 'Mis Reseñas' },
  { id: 'favorites', label: 'Sitios Favoritos' }
]

if (!authStore.isAuthenticated) {
  router.push('/login')
}


const loadReviews = async () => {
  loading.value = true
  error.value = null
  try {
    const data = await profileService.getReviews(currentPage.value, 25, 'lasted')
    reviews.value = data.items
    totalPages.value = data.totalPages
  } catch (err) {
    console.error(' Error loading reviews:', err)
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
    console.error('Error loading favorites:', err)
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
  color: v-bind(profileColor);
}

.tab-button.active {
  color: v-bind(profileColor);
  border-bottom-color: v-bind(profileColor);
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

.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  border: 1px solid #d0e7d7;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #0e1b12;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 16px;
}

.back-button:hover {
  background: #e7f3eb;
  border-color: #a3d3b3;
}

.back-icon {
  width: 20px;
  height: 20px;
  stroke-width: 2;
}
</style>
