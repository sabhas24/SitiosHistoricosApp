<template>
  <section class="featured-section">
    <div class="section-header">
      <h2 class="section-title">{{ title }}</h2>
      <button 
        v-if="showViewAll && sites.length > 0" 
        @click="handleViewAll"
        class="view-all-btn"
      >
        Ver todos →
      </button>
    </div>
    
    <div v-if="loading" class="loading-state">
      <div class="skeleton-grid">
        <div v-for="n in 4" :key="n" class="skeleton-card"></div>
      </div>
    </div>
    
    <div v-else-if="error" class="error-state">
      <p>Error al cargar {{ title.toLowerCase() }}</p>
      <button @click="retry" class="retry-btn">Reintentar</button>
    </div>
    
    <div v-else-if="sites.length === 0" class="empty-state">
      <div class="empty-icon">📍</div>
      <p>{{ emptyMessage }}</p>
    </div>
    
    <div v-else class="sites-grid">
      <SiteCard 
        v-for="site in sites" 
        :key="site.id" 
        :site="site"
      />
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import SiteCard from './SiteCard.vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  endpoint: {
    type: String,
    required: true
  },
  emptyMessage: {
    type: String,
    default: 'No hay contenido disponible'
  },
  showViewAll: {
    type: Boolean,
    default: true
  },
  filterParams: {
    type: Object,
    default: () => ({})
  }
})

const router = useRouter()
const sites = ref([])
const loading = ref(true)
const error = ref(false)

const loadSites = async () => {
  try {
    loading.value = true
    error.value = false
    
    // DATOS MOCK TEMPORALES, REEMPLAZAR POR LA API
    await new Promise(resolve => setTimeout(resolve, 1000))
    sites.value = generateMockSites()
    
  } catch (err) {
    console.error('Error loading sites:', err)
    error.value = true
  } finally {
    loading.value = false
  }
}

const generateMockSites = () => {
  const mockSites = [
    { id: 1, name: 'OBELISCO', city: 'Buenos Aires', province: 'CABA', rating: 4.5, image: null },
    { id: 2, name: 'obelisco', city: 'Buenos Aires', province: 'CABA', rating: 4.8, image: null }
  ]
  
  return mockSites
}

const handleViewAll = () => {
  const queryParams = new URLSearchParams(props.filterParams).toString()
  router.push(`/map${queryParams ? '?' + queryParams : ''}`)
}

const retry = () => {
  loadSites()
}

onMounted(() => {
  loadSites()
})
</script>

<style scoped>
.featured-section {
  margin-bottom: 48px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.view-all-btn {
  background: none;
  border: none;
  color: #3b82f6;
  font-size: 1rem;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.view-all-btn:hover {
  background-color: #f3f4f6;
}

.sites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.loading-state {
  margin: 24px 0;
}

.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.skeleton-card {
  height: 320px;
  background: #f3f4f6;
  border-radius: 12px;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.error-state {
  text-align: center;
  padding: 48px 24px;
  color: #6b7280;
}

.retry-btn {
  margin-top: 16px;
  padding: 8px 16px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.empty-state {
  text-align: center;
  padding: 48px 24px;
  color: #6b7280;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 16px;
  opacity: 0.5;
}

/* Mobile responsive */
@media (max-width: 640px) {
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .section-title {
    font-size: 1.25rem;
  }
  
  .sites-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .skeleton-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}

@media (max-width: 768px) {
  .sites-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  }
}
</style>
