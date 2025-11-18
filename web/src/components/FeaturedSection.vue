<template>
  <section class="featured-section">
    <div class="section-header">
      <h2 class="section-title">{{ title }}</h2>
      <button 
        v-if="showViewAll" 
        @click="handleViewAll"
        class="view-all-link"
      >
        Ver todos >
      </button>
    </div>
    
    <div v-if="loading" class="loading-state">
      <div class="skeleton-grid">
        <div v-for="n in 4" :key="n" class="skeleton-card"></div>
      </div>
    </div>
    
    <div v-else-if="error" class="error-state">
      <p>Error al cargar contenido</p>
      <button @click="retry" class="retry-btn">Reintentar</button>
    </div>
    
    <div v-else-if="sites.length === 0" class="empty-state-container">
      <div class="empty-pill">No hay contenido</div>
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
import sitiosService from '../services/sitiosService'

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
    
    // Llamar a la API con los parámetros del endpoint
    const params = {
      per_page: 8,
      ...props.filterParams
    }
    
    const response = await sitiosService.getSitios(params)
    sites.value = response.sitios || []
    
  } catch (err) {
    console.error('Error loading sites:', err)
    error.value = true
  } finally {
    loading.value = false
  }
}

const handleViewAll = () => {
  // Construir query params para la vista de listado
  const query = {}
  
  if (props.filterParams.sort) {
    query.order_by = props.filterParams.sort
  }
  
  router.push({ name: 'sitios-list', query })
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
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 0;
  border-bottom: none;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  position: relative;
}

.section-title::before {
  content: '';
  position: absolute;
  bottom: -16px;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
}

.view-all-link {
  background: none;
  border: none;
  color: #374151;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  padding: 4px 8px;
  transition: color 0.2s ease;
}

.view-all-link:hover {
  color: #000;
  text-decoration: underline;
}

.sites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
}

.loading-state {
  margin: 0;
}

.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
}

.skeleton-card {
  height: 280px;
  background: #f3f4f6;
  border-radius: 8px;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.error-state {
  text-align: center;
  padding: 32px;
  color: #6b7280;
}

.retry-btn {
  margin-top: 8px;
  padding: 6px 12px;
  background: #e5e7eb;
  color: #374151;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.empty-state-container {
  display: flex;
  justify-content: center;
  padding: 32px 0;
}

.empty-pill {
  background: #f3f4f6;
  color: #4b5563;
  padding: 8px 24px;
  border-radius: 999px;
  font-size: 0.9rem;
  font-weight: 500;
  border: 1px solid #e5e7eb;
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
    grid-template-columns: 1fr; /* Mobile first: stack vertically */
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
