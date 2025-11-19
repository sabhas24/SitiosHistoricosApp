<template>
  <button
    @click="toggleFavorite"
    :class="[
      'favorite-btn', 
      { 
        'favorite-btn--active': isFavorite, 
        'favorite-btn--loading': loading,
        'favorite-btn--compact': variant === 'compact'
      }
    ]"
    :disabled="loading || !isAuthenticated"
    :title="buttonTitle"
  >
    <div class="favorite-btn__content">
      <svg
        v-if="!loading"
        :class="['favorite-btn__icon', { 'favorite-btn__icon--filled': isFavorite }]"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        :fill="isFavorite ? 'currentColor' : 'none'"
        stroke="currentColor"
        stroke-width="2"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"
        />
      </svg>
      <div v-else class="favorite-btn__spinner"></div>
      <span class="favorite-btn__text">
        {{ buttonText }}
      </span>
    </div>
  </button>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '../stores/auth'
import favoritesService from '../services/favoritesService'

const props = defineProps({
  siteId: {
    type: Number,
    required: true
  },
  variant: {
    type: String,
    default: 'default', // 'default' | 'compact'
  }
})

const emit = defineEmits(['favoriteChanged'])

const authStore = useAuthStore()
const isFavorite = ref(false)
const loading = ref(false)

const isAuthenticated = computed(() => authStore.isAuthenticated)

const buttonText = computed(() => {
  if (loading.value) return 'Cargando...'
  if (props.variant === 'compact') return ''
  return isFavorite.value ? 'Quitar de favoritos' : 'Agregar a favoritos'
})

const buttonTitle = computed(() => {
  if (!isAuthenticated.value) return 'Inicia sesión para agregar favoritos'
  if (loading.value) return 'Cargando...'
  return isFavorite.value ? 'Quitar de favoritos' : 'Agregar a favoritos'
})

const checkFavoriteStatus = async () => {
  if (!isAuthenticated.value) return
  
  try {
    loading.value = true
    isFavorite.value = await favoritesService.isFavorite(props.siteId)
  } catch (error) {
    console.error('Error checking favorite status:', error)
  } finally {
    loading.value = false
  }
}

const toggleFavorite = async () => {
  if (!isAuthenticated.value) {
    // Opcional: mostrar modal de login o redirigir
    return
  }

  try {
    loading.value = true
    
    if (isFavorite.value) {
      await favoritesService.removeFromFavorites(props.siteId)
      isFavorite.value = false
    } else {
      await favoritesService.addToFavorites(props.siteId)
      isFavorite.value = true
    }
    
    // Emitir evento para que el componente padre pueda reaccionar
    emit('favoriteChanged', {
      siteId: props.siteId,
      isFavorite: isFavorite.value
    })
    
  } catch (error) {
    console.error('Error toggling favorite:', error)
    // Opcional: mostrar notificación de error
  } finally {
    loading.value = false
  }
}

// Verificar estado inicial cuando el componente se monta
onMounted(() => {
  checkFavoriteStatus()
})

// Reaccionar a cambios en el estado de autenticación
watch(() => authStore.isAuthenticated, (newVal) => {
  if (newVal) {
    checkFavoriteStatus()
  } else {
    isFavorite.value = false
  }
})
</script>

<style scoped>
.favorite-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  color: #64748b;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 160px;
  justify-content: center;
}

.favorite-btn:hover:not(:disabled) {
  border-color: #e11d48;
  color: #e11d48;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(225, 29, 72, 0.15);
}

.favorite-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.favorite-btn--active {
  border-color: #e11d48;
  background: #e11d48;
  color: white;
}

.favorite-btn--active:hover:not(:disabled) {
  background: #be185d;
  border-color: #be185d;
}

.favorite-btn--loading {
  cursor: wait;
}

.favorite-btn__content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.favorite-btn__icon {
  width: 20px;
  height: 20px;
  transition: all 0.2s ease;
}

.favorite-btn__icon--filled {
  color: currentColor;
}

.favorite-btn__text {
  font-size: 14px;
  font-weight: 500;
}

.favorite-btn__spinner {
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Variante compacta */
.favorite-btn--compact {
  min-width: auto;
  padding: 8px;
  border-radius: 50%;
}

.favorite-btn--compact .favorite-btn__text {
  display: none;
}

/* Responsive */
@media (max-width: 768px) {
  .favorite-btn {
    padding: 10px 20px;
    min-width: 140px;
  }
  
  .favorite-btn__text {
    font-size: 13px;
  }
  
  .favorite-btn__icon {
    width: 18px;
    height: 18px;
  }
}
</style>
