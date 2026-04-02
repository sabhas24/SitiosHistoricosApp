<template>
  <div class="user-menu" ref="menuRef">
    <!-- Login Button (Unauthenticated) -->
    <div v-if="!authStore.isAuthenticated">
      <button 
        @click="goToLogin"
        class="btn-login"
      >
        Iniciar Sesión
      </button>
    </div>
    
    <!-- User Menu (Authenticated) -->
    <div v-else>
      <button 
        @click="toggleDropdown"
        class="user-trigger"
        :class="{ 'user-trigger--active': dropdownOpen }"
      >
        <!-- Avatar -->
        <div class="avatar">
          {{ userInitial }}
        </div>
        
        <!-- User Info (Desktop) -->
        <div class="user-info">
          <span class="user-name">
            {{ authStore.userName }}
          </span>
          <span class="user-role">
            Usuario
          </span>
        </div>

        <!-- Chevron -->
        <svg 
          class="chevron-icon"
          :class="{ 'chevron-icon--rotated': dropdownOpen }"
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      
      <!-- Dropdown Menu -->
      <Transition name="dropdown">
        <div v-if="dropdownOpen" class="dropdown-menu">
          <!-- Header -->
          <div class="dropdown-header">
            <div class="header-content">
              <div class="avatar avatar--large">
                {{ userInitial }}
              </div>
              <div class="header-text">
                <p class="header-name">
                  {{ authStore.userName }}
                </p>
                <p class="header-email header-email--mobile">
                  {{ authStore.userEmail }}
                </p>
              </div>
            </div>
          </div>
          
          <!-- Menu Items -->
          <div class="dropdown-body">
            <!-- Account Section -->
            <div class="menu-section">
              <p class="section-title">Mi Cuenta</p>
              <RouterLink 
                to="/profile" 
                class="menu-item"
                @click="closeDropdown"
              >
                <div class="item-icon">
                  <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <div class="item-content">
                  <span class="item-title">Perfil</span>
                  <span class="item-subtitle">Gestiona tu información</span>
                </div>
              </RouterLink>
            </div>

            <!-- Activity Section -->
            <div class="menu-section">
              <p class="section-title">Actividad</p>
              <RouterLink 
                to="/profile?tab=reviews" 
                class="menu-item"
                @click="closeDropdown"
              >
                <div class="item-icon">
                  <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </div>
                <span class="item-title">Mis Reseñas</span>
              </RouterLink>

              <RouterLink 
                to="/profile?tab=favorites" 
                class="menu-item"
                @click="closeDropdown"
              >
                <div class="item-icon">
                  <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                </div>
                <span class="item-title">Sitios Favoritos</span>
              </RouterLink>
            </div>
            
            <div class="divider"></div>
            
            <!-- Logout -->
            <button 
              @click="handleLogout" 
              class="menu-item menu-item--danger"
            >
              <div class="item-icon item-icon--danger">
                <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </div>
              <span class="item-title">Cerrar Sesión</span>
            </button>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import api from '../../config/api'

const router = useRouter()
const authStore = useAuthStore()
const dropdownOpen = ref(false)
const menuRef = ref(null)

const userInitial = computed(() => {
  return authStore.userName ? authStore.userName.charAt(0).toUpperCase() : 'U'
})

const toggleDropdown = (e) => {
  e.stopPropagation()
  dropdownOpen.value = !dropdownOpen.value
}

const closeDropdown = () => {
  dropdownOpen.value = false
}

const handleClickOutside = (event) => {
  if (menuRef.value && !menuRef.value.contains(event.target)) {
    dropdownOpen.value = false
  }
}

const handleLogout = async () => {
  try {
    await api.post('/user/logout', {}, { withCredentials: true })
  } catch (e) {
    console.error('Logout error:', e)
  }
  authStore.clearUser()
  router.push('/login')
  closeDropdown()
}

const goToLogin = () => {
  router.push({ name: 'login', query: { redirect: router.currentRoute.value.fullPath } })
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.user-menu {
  position: relative;
}

/* Login Button */
.btn-login {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.375rem 1rem;
  font-size: 0.8rem;
  font-weight: 500;
  color: white;
  background-color: var(--color-blue-600);
  border-radius: var(--radius-full);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-fast);
}

@media (min-width: 640px) {
  .btn-login {
    padding: 0.5rem 1.25rem;
    font-size: 0.875rem;
  }
}

.btn-login:hover {
  background-color: var(--color-blue-700);
  box-shadow: var(--shadow-md);
}

/* User Trigger */
.user-trigger {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.5rem;
  background-color: #f3f4f6;
  border: 1px solid transparent;
  border-radius: var(--radius-full);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-fast);
  min-width: fit-content;
}

@media (min-width: 640px) {
  .user-trigger {
    gap: 0.75rem;
    padding: 0.375rem 0.75rem;
    padding-left: 0.5rem;
  }
}

.user-trigger:hover {
  border-color: var(--color-blue-300);
  background-color: #e5e7eb;
  box-shadow: var(--shadow-md);
}

.user-trigger--active {
  border-color: var(--color-blue-300);
  box-shadow: 0 0 0 2px var(--color-blue-100);
}

/* Avatar */
.avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.75rem;
  height: 1.75rem;
  font-size: 0.75rem;
  font-weight: 700;
  color: white;
  background: linear-gradient(135deg, var(--color-blue-500), var(--color-blue-600));
  border-radius: var(--radius-full);
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}

@media (min-width: 640px) {
  .avatar {
    width: 2rem;
    height: 2rem;
    font-size: 0.875rem;
  }
}

.avatar--large {
  width: 3rem;
  height: 3rem;
  font-size: 1.25rem;
  background: white;
  color: var(--color-blue-600);
  border: 2px solid var(--color-blue-100);
}

.user-info {
  display: none;
  flex-direction: column;
  align-items: flex-start;
  margin-right: 0.25rem;
}

@media (min-width: 640px) {
  .user-info {
    display: flex;
  }
}

.user-name {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--color-slate-700);
  transition: color var(--transition-fast);
}

.user-trigger:hover .user-name {
  color: var(--color-blue-700);
}

.user-role {
  font-size: 0.625rem;
  font-weight: 500;
  color: var(--color-slate-500);
}


.chevron-icon {
  width: 0.875rem;
  height: 0.875rem;
  color: var(--color-slate-400);
  transition: transform var(--transition-fast), color var(--transition-fast);
}

@media (min-width: 640px) {
  .chevron-icon {
    width: 1rem;
    height: 1rem;
  }
}

.user-trigger:hover .chevron-icon {
  color: var(--color-blue-500);
}

.chevron-icon--rotated {
  transform: rotate(180deg);
  color: var(--color-blue-500);
}

/* Dropdown Menu */
.dropdown-menu {
  position: absolute;
  right: 0;
  top: 100%;
  margin-top: 0.5rem;
  width: 16rem;
  background-color: #f9fafb; 
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--color-slate-200);
  overflow: hidden;
  z-index: 50;
  transform-origin: top right;
}

@media (max-width: 480px) {
  .dropdown-menu {
    width: calc(100vw - 2rem);
    max-width: 16rem;
    right: -0.5rem;
    left: -0.5rem;
    margin-top: 0.25rem;
  }
}

@media (min-width: 481px) and (max-width: 640px) {
  .dropdown-menu {
    width: 14rem;
  }
}

.dropdown-header {
  padding: 1.25rem;
  background-color: var(--color-slate-50);
  border-bottom: 1px solid var(--color-slate-100);
}

@media (max-width: 640px) {
  .dropdown-header {
    padding: 0.75rem;
  }
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-text {
  overflow: hidden;
}

.header-name {
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--color-slate-900);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.header-email {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--color-slate-500);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.header-email--mobile {
  display: none;
}

@media (min-width: 640px) {
  .header-email--mobile {
    display: block;
  }
}

.dropdown-body {
  padding: 0.5rem;
}

@media (max-width: 640px) {
  .dropdown-body {
    padding: 0.25rem;
  }
}

.menu-section {
  padding: 0.5rem 0.75rem;
}

@media (max-width: 640px) {
  .menu-section {
    padding: 0.25rem 0.5rem;
  }
}

.section-title {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-slate-400);
  margin-bottom: 0.5rem;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 0.75rem;
  border-radius: var(--radius-lg);
  color: var(--color-slate-600);
  transition: all var(--transition-fast);
  width: 100%;
  text-align: left;
}

.menu-item:hover {
  background-color: var(--color-blue-50);
  color: var(--color-blue-700);
}

.item-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.375rem;
  background-color: var(--color-slate-100);
  border-radius: var(--radius-md);
  color: var(--color-slate-500);
  transition: all var(--transition-fast);
}

.menu-item:hover .item-icon {
  background-color: white;
  color: var(--color-blue-600);
  box-shadow: var(--shadow-sm);
}

.item-content {
  display: flex;
  flex-direction: column;
}

.item-subtitle {
  font-size: 0.75rem;
  color: var(--color-slate-400);
}

.menu-item:hover .item-subtitle {
  color: var(--color-blue-500);
  opacity: 0.8;
}

@media (max-width: 640px) {
  .item-subtitle {
    display: none;
  }
  
  .menu-item {
    padding: 0.5rem 0.75rem;
  }
  
  .item-icon {
    padding: 0.25rem;
  }
}

.divider {
  height: 1px;
  background-color: var(--color-slate-100);
  margin: 0.25rem 0.75rem;
}

/* Danger / Logout */
.menu-item--danger {
  color: var(--color-red-600);
}

.menu-item--danger:hover {
  background-color: var(--color-red-50);
  color: var(--color-red-600);
}

.item-icon--danger {
  background-color: var(--color-red-50);
  color: var(--color-red-500);
}

.menu-item--danger:hover .item-icon--danger {
  background-color: white;
  box-shadow: var(--shadow-sm);
}

/* Transitions */
.dropdown-enter-active {
  transition: all 0.2s ease-out;
}

.dropdown-leave-active {
  transition: all 0.15s ease-in;
}

.dropdown-enter-from,
.dropdown-leave-to {
  transform: scale(0.95) translateY(-10px);
  opacity: 0;
}
</style>
