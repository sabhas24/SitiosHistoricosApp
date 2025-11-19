<template>
  <nav 
    class="navbar"
    :class="{ 'navbar--scrolled': isScrolled, 'navbar--transparent': transparent && !isScrolled }"
  >
    <div class="container navbar__content">
      <!-- Brand -->
      <div class="navbar__brand">
        <RouterLink to="/" class="brand-link">
          <span class="brand-text">PatrimonioBA</span>
        </RouterLink>
      </div>
      
      <!-- Desktop Menu -->
      <div class="navbar__menu">
        <RouterLink 
          v-for="item in navItems" 
          :key="item.path" 
          :to="item.path"
          class="nav-link"
          active-class="nav-link--active"
        >
          {{ item.name }}
        </RouterLink>
      </div>

      <!-- User Menu & Mobile Toggle -->
      <div class="navbar__actions">
        <UserMenu />
        
        <!-- Mobile Menu Button -->
        <button 
          class="mobile-toggle"
          @click="toggleMobileMenu"
          aria-label="Toggle menu"
        >
          <svg 
            class="icon" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              v-if="!mobileMenuOpen" 
              stroke-linecap="round" 
              stroke-linejoin="round" 
              stroke-width="2" 
              d="M4 6h16M4 12h16M4 18h16"
            />
            <path 
              v-else 
              stroke-linecap="round" 
              stroke-linejoin="round" 
              stroke-width="2" 
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <Transition name="slide-fade">
      <div v-if="mobileMenuOpen" class="mobile-menu">
        <div class="mobile-menu__content">
          <RouterLink 
            v-for="item in navItems" 
            :key="item.path" 
            :to="item.path"
            class="mobile-link"
            active-class="mobile-link--active"
            @click="closeMobileMenu"
          >
            {{ item.name }}
          </RouterLink>
        </div>
      </div>
    </Transition>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import UserMenu from './UserMenu.vue'

defineProps({
  transparent: {
    type: Boolean,
    default: false
  }
})

const mobileMenuOpen = ref(false)
const isScrolled = ref(false)

const navItems = [
  { name: 'Inicio', path: '/' },
  { name: 'Sitios', path: '/sitios' },
  { name: 'Mapa', path: '/map' }
]

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 1000;
  width: 100%;
  transition: background-color var(--transition-normal), box-shadow var(--transition-normal);
  background-color: rgba(17, 24, 39, 0.8); 
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.navbar--transparent {
  border-bottom-color: transparent;
}

.navbar--scrolled .brand-text {
  background: linear-gradient(to right, var(--color-blue-600), var(--color-blue-800));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.navbar__content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 4rem;
}

.navbar__brand {
  flex-shrink: 0;
}

.brand-text {
  font-size: 1.5rem;
  font-weight: 700;
  /* Se quita el degradado para que sea blanco sólido */
  color: white;
  text-shadow: 0 0 2px white, 0 0 2px white, 0 0 2px white, 0 0 2px white;
  transition: opacity var(--transition-fast);
}

.navbar__menu {
  display: none;
  align-items: center;
  gap: 0.5rem;
}

@media (min-width: 768px) {
  .navbar__menu {
    display: flex;
  }
}

.nav-link {
  padding: 0.5rem 1rem;
  border-radius: var(--radius-full);
  font-size: 0.875rem;
  font-weight: 500;
  color: white;
  transition: all var(--transition-fast);
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.15);
  color: white;
}

.nav-link--active {
  background-color: white !important;
  color: #1f2937 !important; /* Color oscuro para el texto */
  font-weight: 600;
}

.navbar__actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.mobile-toggle {
  display: block;
  padding: 0.5rem;
  border-radius: var(--radius-md);
  color: var(--color-slate-600);
  transition: background-color var(--transition-fast);
}

@media (min-width: 768px) {
  .mobile-toggle {
    display: none;
  }
}

.mobile-toggle:hover {
  background-color: var(--color-slate-100);
}

.icon {
  width: 1.5rem;
  height: 1.5rem;
}

/* Mobile Menu */
.mobile-menu {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background-color: white;
  border-bottom: 1px solid var(--color-slate-200);
  box-shadow: var(--shadow-lg);
}

.mobile-menu__content {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mobile-link {
  display: block;
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 500;
  color: var(--color-slate-600);
  transition: all var(--transition-fast);
}

.mobile-link:hover {
  background-color: var(--color-slate-50);
  color: var(--color-blue-600);
}

.mobile-link--active {
  background-color: var(--color-blue-50);
  color: var(--color-blue-700);
}

/* Transitions */
.slide-fade-enter-active {
  transition: all 0.2s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.15s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}
</style>
