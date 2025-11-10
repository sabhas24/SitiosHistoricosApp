<template>
  <nav class="main-navigation" :class="{ 'nav-transparent': transparent }">
    <div class="nav-container">
      <div class="nav-brand">
        <RouterLink to="/" class="brand-link">
          <span class="brand-name">PatrimonioBA</span>
        </RouterLink>
      </div>
      
      <div class="nav-menu" :class="{ 'nav-menu-open': mobileMenuOpen }">
        <RouterLink to="/" class="nav-link" @click="closeMobileMenu">Inicio</RouterLink>
        <RouterLink to="/map" class="nav-link" @click="closeMobileMenu">Mapa</RouterLink>
      </div>
      
      <button 
        class="mobile-menu-btn"
        @click="toggleMobileMenu"
        aria-label="Toggle menu"
      >
        <span class="hamburger" :class="{ 'hamburger-open': mobileMenuOpen }"></span>
      </button>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'

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

<style scoped>
.main-navigation {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  z-index: 100;
  transition: all 0.3s ease;
}

.nav-transparent {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
}

.nav-brand {
  font-size: 1.5rem;
  font-weight: 700;
}

.brand-link {
  color: #1f2937;
  text-decoration: none;
  transition: color 0.2s;
}

.brand-link:hover {
  color: #3b82f6;
  text-decoration: none;
}

.brand-name {
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 32px;
}

.nav-link {
  color: #6b7280;
  text-decoration: none;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 6px;
  transition: all 0.2s;
}

.nav-link:hover {
  color: #3b82f6;
  background-color: rgba(59, 130, 246, 0.1);
  text-decoration: none;
}

.nav-link.router-link-exact-active {
  color: #3b82f6;
  background-color: rgba(59, 130, 246, 0.1);
}

.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.mobile-menu-btn:hover {
  background-color: #f3f4f6;
}

.hamburger {
  display: block;
  width: 24px;
  height: 2px;
  background: #374151;
  position: relative;
  transition: all 0.3s ease;
}

.hamburger::before,
.hamburger::after {
  content: '';
  display: block;
  width: 24px;
  height: 2px;
  background: #374151;
  position: absolute;
  transition: all 0.3s ease;
}

.hamburger::before {
  transform: translateY(-8px);
}

.hamburger::after {
  transform: translateY(8px);
}

.hamburger-open {
  background: transparent;
}

.hamburger-open::before {
  transform: rotate(45deg);
}

.hamburger-open::after {
  transform: rotate(-45deg);
}

/* Mobile responsive */
@media (max-width: 768px) {
  .nav-container {
    padding: 0 16px;
  }
  
  .nav-menu {
    position: fixed;
    top: 70px;
    left: 0;
    right: 0;
    background: white;
    flex-direction: column;
    align-items: stretch;
    gap: 0;
    padding: 20px;
    border-bottom: 1px solid #e5e7eb;
    transform: translateY(-100%);
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
  }
  
  .nav-menu-open {
    transform: translateY(0);
    opacity: 1;
    visibility: visible;
  }
  
  .nav-link {
    padding: 16px;
    text-align: center;
    border-bottom: 1px solid #f3f4f6;
  }
  
  .nav-link:last-child {
    border-bottom: none;
  }
  
  .mobile-menu-btn {
    display: block;
  }
}
</style>
