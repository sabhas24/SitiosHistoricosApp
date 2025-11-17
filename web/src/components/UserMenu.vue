<template>
  <div class="user-menu flex items-center space-x-4"> 
   
    <div v-if="!authStore.isAuthenticated" class="flex items-center">
      <RouterLink to="/login" class="px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-semibold hover:shadow-lg transition-shadow">
        Iniciar sesión
      </RouterLink>
    </div>
    
    
    <div v-else class="relative">
      <button @click="toggleDropdown" class="flex items-center gap-3 px-3 py-2 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md focus:outline-none">
        <div class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 text-white flex items-center justify-center font-bold text-lg">
          {{ userInitial }}
        </div>
        <div class="hidden sm:flex flex-col text-left">
          <span class="text-sm font-semibold text-gray-800">{{ authStore.userName }}</span>
          <span class="text-xs text-gray-500">Ver perfil</span>
        </div>
        <svg class="w-4 h-4 text-gray-500" :class="{ 'transform rotate-180': dropdownOpen }" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M6 8L10 12L14 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
      
      <transition name="fade">
        <div v-if="dropdownOpen" class="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg ring-1 ring-black/5 origin-top-right z-50">
          <div class="px-4 py-3 border-b border-gray-100">
            <p class="text-sm font-semibold text-gray-800">{{ authStore.userName }}</p>
            <p class="text-xs text-gray-500 truncate">{{ authStore.userEmail }}</p>
          </div>
          <div class="py-1">
            <RouterLink to="/profile" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">Perfil</RouterLink>
            <RouterLink to="/my-reviews" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">Mis reseñas</RouterLink>
            <RouterLink to="/favorites" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">Sitios favoritos</RouterLink>
          </div>
          <div class="border-t border-gray-100">
            <button @click="handleLogout" class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-50">Cerrar sesión</button>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watchEffect } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../config/api'


const router = useRouter()
const authStore = useAuthStore()
const dropdownOpen = ref(false)

const userInitial = computed(() => {
  return authStore.userName ? authStore.userName.charAt(0).toUpperCase() : 'U'
})

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

// Close dropdown when clicking outside
const onDocumentClick = (e) => {
  const target = e.target
  const root = document.querySelector('.user-menu')
  if (!root) return
  if (!root.contains(target)) dropdownOpen.value = false
}

watchEffect(() => {
  if (dropdownOpen.value) {
    document.addEventListener('click', onDocumentClick)
  } else {
    document.removeEventListener('click', onDocumentClick)
  }
})

const handleLogout = async () => {
  try {
    await api.post('/user/logout', {}, { withCredentials: true })
  } catch (e) {
    console.error(e)
  }
  authStore.clearUser()
  router.push('/login')
}

const goToProfile = () => router.push('/profile')
const goToReviews = () => router.push('/my-reviews')
const goToFavorites = () => router.push('/favorites')
</script>

<!-- Styles converted to Tailwind utilities; no scoped CSS required -->


