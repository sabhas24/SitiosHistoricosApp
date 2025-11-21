<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import SiteCard from './SiteCard.vue'
import sitiosService from '../../services/sitiosService'
import favoritesService from '@/services/favoritesService'

const router = useRouter()

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  endpoint: {
    type: String,
    required: false
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
  },
  isFavorites: {
    type: Boolean,
    default: false
  }
})

const sites = ref([])
const isLoading = ref(true)
const hasError = ref(false)
const carouselTrack = ref(null)


const getCardWidth = () => {
  if (typeof window === 'undefined') return 280
  
  const width = window.innerWidth
  if (width <= 480) return 160
  if (width <= 640) return 200
  if (width <= 768) return 240
  return 280
}

const getGap = () => {
  if (typeof window === 'undefined') return 20
  
  const width = window.innerWidth
  if (width <= 480) return 8
  if (width <= 640) return 12
  if (width <= 768) return 16
  return 20
}

const loadSites = async () => {
  try {
    isLoading.value = true
    hasError.value = false
    
    let response
    if (props.isFavorites) {
      const params = {
        limit: 10,
        order: props.filterParams?.order || 'latest',
        page: props.filterParams?.page || 1
      }
      response = await favoritesService.getFavorites(params.page, params.limit, params.order)
      sites.value = response.items || []
    } else {
     
      if (props.endpoint?.includes('mas-visitados')) {
        response = await sitiosService.getMasVisitados(8)
      } else if (props.endpoint?.includes('mejor-puntuados')) {
        response = await sitiosService.getMejorPuntuados(8)
      } else if (props.endpoint?.includes('recientes')) {
        response = await sitiosService.getRecientes(8)
      } else {
        // Generic method with filters
        const params = {
          per_page: 8,
          ...props.filterParams
        }
        response = await sitiosService.getSitios(params)
      }
      sites.value = response.sitios || []
    }
    
  } catch (err) {
    console.error('Error loading sites:', err)
    hasError.value = true
  } finally {
    isLoading.value = false
  }
}

const handleViewAll = () => {
  // Construir query params para la vista de listado
  const query = {}
  
  if (props.filterParams?.order_by) {
    query.order_by = props.filterParams.order_by
  }
  
  router.push({ name: 'sitios-list', query })
}

const retry = () => {
  loadSites()
}

const scrollLeft = () => {
  if (carouselTrack.value) {
    const scrollAmount = getCardWidth() + getGap()
    carouselTrack.value.scrollBy({ left: -scrollAmount, behavior: 'smooth' })
  }
}

const scrollRight = () => {
  if (carouselTrack.value) {
    const scrollAmount = getCardWidth() + getGap()
    carouselTrack.value.scrollBy({ left: scrollAmount, behavior: 'smooth' })
  }
}

onMounted(() => {
  loadSites()
})
</script>

<template>
  <section class="featured-section">
    <div class="section-header">
      <h2 class="section-title">{{ title }}</h2>
      <div class="header-actions">
        <button 
          v-if="showViewAll" 
          @click="handleViewAll"
          class="view-all-link"
        >
          Ver todos
        </button>
      </div>
    </div>
    
    <div v-if="isLoading" class="loading-state">
      <div class="skeleton-grid">
        <div v-for="n in 4" :key="n" class="skeleton-card"></div>
      </div>
    </div>
    
    <div v-else-if="hasError" class="error-state">
      <p>Error al cargar contenido</p>
      <button @click="retry" class="retry-btn">Reintentar</button>
    </div>
    
    <div v-else-if="sites.length === 0" class="empty-state-container">
      <div class="empty-pill">{{ emptyMessage }}</div>
    </div>
    
    <div v-else class="carousel-container">
      <div class="sites-grid" ref="carouselTrack">
        <SiteCard 
          v-for="site in sites" 
          :key="site.id" 
          :site="site"
        />
      </div>
      <!-- Navigation Buttons -->
      <div class="carousel-nav">
        <button @click="scrollLeft" class="nav-btn nav-btn--prev" aria-label="Anterior">‹</button>
        <button @click="scrollRight" class="nav-btn nav-btn--next" aria-label="Siguiente">›</button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.featured-section {
  margin-bottom: 48px;
  animation: fadeIn 0.6s ease-out;

  background: rgba(28, 37, 54, 0.03 ); 
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 24px 32px; 
  width: 99vw;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
  box-sizing: border-box;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.025);
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.featured-section:hover {
  box-shadow: 0 12px 48px rgba(88, 88, 88, 0.1);
  background-color: rgba(15, 15, 15, 0.15);
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

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #111827;
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
  background-color: #2563eb;
  border: 1px solid #d1d5db;
  color: #ffffff;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  padding: 6px 16px;
  border-radius: 999px;
  transition: all 0.2s ease;
}

.view-all-link:hover {
  background-color: #f3f4f6;
  color: #374151;
  border-color: #9ca3af;
  transform: scale(1.05);
}

.carousel-container {
  position: relative;
}

.carousel-container:hover .nav-btn {
  opacity: 1;
}

.nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background-color: rgba(17, 24, 39, 0.5);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 1.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 10;
  opacity: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-btn:hover {
  background-color: rgba(17, 24, 39, 0.8);
  transform: translateY(-50%) scale(1.05);
}

.nav-btn--prev {
  left: -22px;
}

.nav-btn--next {
  right: -22px;
}

.sites-grid {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: 280px; /* Fixed width for consistent carousel */
  gap: 20px;
  overflow-x: auto;
  padding-bottom: 20px;
  scroll-behavior: smooth;
  scroll-snap-type: x mandatory;
  /* Ocultar la barra de scroll */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}
.sites-grid::-webkit-scrollbar {
  display: none; /* Chrome, Safari, and Opera */
}

.sites-grid > * {
  width: 280px;
  scroll-snap-align: start;
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
@media (max-width: 768px) {
  .featured-section {
    padding: 16px 16px;
    margin-bottom: 32px;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 16px;
  }
  
  .section-title {
    font-size: 1.25rem;
  }
  
  .section-title::before {
    bottom: -12px;
    width: 50px;
    height: 2px;
  }
  
  .sites-grid {
    grid-auto-columns: 240px; /* Fixed width for tablets */
    gap: 16px;
    padding-bottom: 16px;
  }
  
  .sites-grid > * {
    width: 240px;
  }
  
  .skeleton-grid {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 16px;
  }
  
  .skeleton-card {
    height: 240px;
  }
  
  /* Adjust navigation buttons for tablets */
  .nav-btn {
    width: 36px;
    height: 36px;
    font-size: 1.5rem;
  }
  
  .nav-btn--prev {
    left: -18px;
  }
  
  .nav-btn--next {
    right: -18px;
  }
}

@media (max-width: 640px) {
  .featured-section {
    padding: 12px 12px;
    margin-bottom: 24px;
  }
  
  .sites-grid {
    grid-auto-columns: 200px; /* Smaller cards for mobile */
    gap: 12px;
  }
  
  .sites-grid > * {
    width: 200px;
  }
  
  .skeleton-grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 12px;
  }
  
  .skeleton-card {
    height: 200px;
  }
  
  /* Hide navigation buttons on small mobile screens */
  .nav-btn {
    display: none;
  }
}

@media (max-width: 480px) {
  .featured-section {
    padding: 8px 8px;
  }
  
  .sites-grid {
    grid-auto-columns: 160px; /* Even smaller for very small screens */
    gap: 8px;
  }
  
  .sites-grid > * {
    width: 160px;
  }
  
  .skeleton-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 8px;
  }
  
  .skeleton-card {
    height: 160px;
  }
  
  .section-title {
    font-size: 1.1rem;
  }
  
  .view-all-link {
    font-size: 0.85rem;
    padding: 4px 12px;
  }
}
</style>
