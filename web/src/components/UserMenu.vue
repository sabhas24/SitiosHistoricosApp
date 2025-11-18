<template>
  <div class="user-menu">
   
    <div v-if="!authStore.isAuthenticated" class="auth-actions">
      <RouterLink to="/login" class="btn-login">
        Iniciar Sesión
      </RouterLink>
    </div>
      <div v-if="!authStore.isAuthenticated" class="auth-actions">
        <button class="btn-login" @click="goToLogin">
          Iniciar Sesión
        </button>
      </div>
    
    
    <div v-else class="user-dropdown">
      <button 
        class="user-button" 
        @click="toggleDropdown"
        @blur="closeDropdown"
      >
        <div class="user-avatar">
          {{ userInitial }}
        </div>
        <span class="user-name">{{ authStore.userName }}</span>
        <svg 
          class="dropdown-icon" 
          :class="{ 'dropdown-icon-open': dropdownOpen }"
          width="16" 
          height="16" 
          viewBox="0 0 16 16" 
          fill="none"
        >
          <path d="M4 6L8 10L12 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
      
      <div v-if="dropdownOpen" class="dropdown-menu">
        <div class="dropdown-header">
          <div class="dropdown-user-info">
            <p class="dropdown-user-name">{{ authStore.userName }}</p>
            <p class="dropdown-user-email">{{ authStore.userEmail }}</p>
          </div>
        </div>
        <div class="dropdown-divider"></div>
        <RouterLink to="/profile" class="dropdown-item" @click="closeDropdown">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M8 8C9.65685 8 11 6.65685 11 5C11 3.34315 9.65685 2 8 2C6.34315 2 5 3.34315 5 5C5 6.65685 6.34315 8 8 8Z" stroke="currentColor" stroke-width="1.5"/>
            <path d="M2.5 14C2.5 11.7909 5.13401 10 8 10C10.866 10 13.5 11.7909 13.5 14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          Perfil
        </RouterLink>
        <RouterLink to="/profile" class="dropdown-item" @click="closeDropdown">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M8 2C5.33333 2 3.2 3.2 2.4 5M8 2C10.6667 2 12.8 3.2 13.6 5M3 8H13M6 10.5V12.5M10 10.5V12.5M3.5 13.5H12.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Mis Reseñas
        </RouterLink>
        <RouterLink to="/profile" class="dropdown-item" @click="closeDropdown">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M8 2C4.68629 2 2 4.68629 2 8C2 11.3137 4.68629 14 8 14C11.3137 14 14 11.3137 14 8C14 4.68629 11.3137 2 8 2ZM8 10C6.89543 10 6 9.10457 6 8C6 6.89543 6.89543 6 8 6C9.10457 6 10 6.89543 10 8C10 9.10457 9.10457 10 8 10Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
          </svg>
          Sitios Favoritos
        </RouterLink>
        <div class="dropdown-divider"></div>
        <button @mousedown="handleLogout" class="dropdown-item logout-item">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M6 14H3.33333C2.97971 14 2.64057 13.8595 2.39052 13.6095C2.14048 13.3594 2 13.0203 2 12.6667V3.33333C2 2.97971 2.14048 2.64057 2.39052 2.39052C2.64057 2.14048 2.97971 2 3.33333 2H6M10.6667 11.3333L14 8M14 8L10.6667 4.66667M14 8H6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Cerrar Sesión
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
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

const closeDropdown = () => {
  setTimeout(() => {
    dropdownOpen.value = false
  }, 200)
}

const handleLogout = async () => {
  try {
    await api.post('/user/logout', {}, { withCredentials: true })
  } catch (e) {
    console.error('Logout error:', e)
  }
  authStore.clearUser()
  router.push('/login')
}

const goToLogin = () => {
  router.push({ name: 'login', query: { redirect: router.currentRoute.value.fullPath } })
}
</script>

<style scoped>
.user-menu {
  display: flex;
  align-items: center;
}

.auth-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.btn-login {
  padding: 8px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  display: inline-block;
}

.btn-login:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  text-decoration: none;
}

.user-dropdown {
  position: relative;
}

.user-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.user-button:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
}

.user-name {
  color: #1f2937;
  font-weight: 500;
  font-size: 14px;
}

.dropdown-icon {
  color: #6b7280;
  transition: transform 0.2s;
}

.dropdown-icon-open {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  min-width: 220px;
  z-index: 1000;
  animation: slideDown 0.2s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-header {
  padding: 12px 16px;
}

.dropdown-user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.dropdown-user-name {
  font-weight: 600;
  color: #1f2937;
  font-size: 14px;
  margin: 0;
}

.dropdown-user-email {
  color: #6b7280;
  font-size: 12px;
  margin: 0;
  word-break: break-all;
}

.dropdown-divider {
  height: 1px;
  background: #e5e7eb;
  margin: 0;
}

.dropdown-item {
  width: 100%;
  padding: 12px 16px;
  border: none;
  background: none;
  text-align: left;
  color: #dc2626;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.dropdown-item:hover {
  background: #fee2e2;
}

.dropdown-item svg {
  flex-shrink: 0;
}

.logout-item {
  color: #dc2626;
}

@media (max-width: 768px) {
  .user-name {
    display: none;
  }
  
  .dropdown-menu {
    right: -8px;
  }
}
</style>
