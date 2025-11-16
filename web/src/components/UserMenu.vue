<template>
  <div class="user-menu">
   
    <div v-if="!authStore.isAuthenticated" class="auth-actions">
      <RouterLink to="/login" class="btn-login">
        Iniciar Sesión
      </RouterLink>
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
        <button @mousedown="handleLogout" class="dropdown-item">
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

const handleLogout = () => {
  authStore.clearUser()
  router.push('/login')
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

@media (max-width: 768px) {
  .user-name {
    display: none;
  }
  
  .dropdown-menu {
    right: -8px;
  }
}
</style>
