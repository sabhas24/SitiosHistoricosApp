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
        <RouterLink to="/sitios" class="nav-link" @click="closeMobileMenu">Sitios</RouterLink>
        <RouterLink to="/map" class="nav-link" @click="closeMobileMenu">Mapa</RouterLink>
      </div>

      <UserMenu />
      
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

<style scoped>
.main-navigation {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(229, 231, 235, 0.5);
  position: sticky;
  top: 0;
  z-index: 100;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.nav-transparent {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
}

.nav-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 75px;
}

.nav-brand {
  font-size: 1.6rem;
  font-weight: 800;
  letter-spacing: -0.02em;
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
  font-weight: 600;
  padding: 10px 20px;
  border-radius: 10px;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 8px;
  left: 20px;
  right: 20px;
  height: 2px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.nav-link:hover {
  color: #667eea;
  background-color: rgba(102, 126, 234, 0.08);
  text-decoration: none;
}

.nav-link:hover::after {
  transform: scaleX(1);
}

.nav-link.router-link-exact-active {
  color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.12) 0%, rgba(118, 75, 162, 0.12) 100%);
}

.nav-link.router-link-exact-active::after {
  transform: scaleX(1);
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
