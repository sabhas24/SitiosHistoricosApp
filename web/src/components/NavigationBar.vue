<template>
  <nav :class="[transparent ? 'bg-white/80 backdrop-blur-sm border-b border-gray-200' : 'bg-white border-b border-gray-200', 'sticky top-0 z-50']">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="nav-brand">
        <RouterLink to="/" class="brand-link">
          <span class="brand-name">PatrimonioBA</span>
        </RouterLink>
      </div>
      
      <div :class="[mobileMenuOpen ? 'block' : 'hidden', 'sm:flex sm:items-center sm:gap-8']">
        <RouterLink to="/" class="text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium" @click="closeMobileMenu">Inicio</RouterLink>
        <RouterLink to="/map" class="text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium" @click="closeMobileMenu">Mapa</RouterLink>
      </div>

      <UserMenu />
      
      <button class="sm:hidden p-2 rounded-md text-gray-500 hover:bg-gray-100" @click="toggleMobileMenu" aria-label="Toggle menu">
        <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
          <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import UserMenu from './UserMenu.vue'

defineProps({
  transparent: {
    type: Boolean,
    default: false
  }
})

const mobileMenuOpen = ref(false)

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}
</script>

<!-- NavigationBar styles converted to Tailwind utilities -->


