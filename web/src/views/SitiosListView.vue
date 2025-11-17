<template>
  <div class="sitios-catalog-page">
    <NavigationBar />
    
    <main class="main-content">
      <div class="content-wrapper">
        <!-- Left Sidebar - Filtros -->
        <aside class="filters-sidebar">
          <div class="filters-container">
            <div class="filters-header">
              <h3>Filtros</h3>
              <button @click="clearFilters" class="clear-link">Limpiar</button>
            </div>
            
            <!-- Buscar por nombre -->
            <div class="filter-group">
              <label class="filter-label">Buscar por nombre</label>
              <div class="search-input-wrapper">
                <svg class="search-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <circle cx="11" cy="11" r="8"></circle>
                  <path d="m21 21-4.35-4.35"></path>
                </svg>
                <input
                  v-model="filters.name"
                  type="text"
                  placeholder="Ej: Manzana de las Luces"
                  @input="debouncedSearch"
                  class="filter-search-input"
                />
              </div>
            </div>
            
            <!-- Filtrar por provincia -->
            <div class="filter-group">
              <h4 class="filter-subtitle">Provincia</h4>
              <div class="checkbox-list">
                <label class="checkbox-item">
                  <input 
                    type="checkbox" 
                    value="Buenos Aires"
                    @change="toggleProvince('Buenos Aires')"
                    :checked="selectedProvinces.includes('Buenos Aires')"
                  />
                  <span>Buenos Aires</span>
                </label>
                <label class="checkbox-item">
                  <input 
                    type="checkbox" 
                    value="Córdoba"
                    @change="toggleProvince('Córdoba')"
                    :checked="selectedProvinces.includes('Córdoba')"
                  />
                  <span>Córdoba</span>
                </label>
                <label class="checkbox-item">
                  <input 
                    type="checkbox" 
                    value="Salta"
                    @change="toggleProvince('Salta')"
                    :checked="selectedProvinces.includes('Salta')"
                  />
                  <span>Salta</span>
                </label>
              </div>
            </div>
            
            <!-- Filtrar por tipo -->
            <div class="filter-group">
              <h4 class="filter-subtitle">Tipo de Patrimonio</h4>
              <div class="checkbox-list">
                <label class="checkbox-item">
                  <input 
                    type="checkbox" 
                    value="Arquitectónico"
                    @change="toggleCategory('Arquitectónico')"
                    :checked="selectedCategories.includes('Arquitectónico')"
                  />
                  <span>Arquitectónico</span>
                </label>
                <label class="checkbox-item">
                  <input 
                    type="checkbox" 
                    value="Natural"
                    @change="toggleCategory('Natural')"
                    :checked="selectedCategories.includes('Natural')"
                  />
                  <span>Natural</span>
                </label>
                <label class="checkbox-item">
                  <input 
                    type="checkbox" 
                    value="Arqueológico"
                    @change="toggleCategory('Arqueológico')"
                    :checked="selectedCategories.includes('Arqueológico')"
                  />
                  <span>Arqueológico</span>
                </label>
                <label class="checkbox-item">
                  <input 
                    type="checkbox" 
                    value="Cultural"
                    @change="toggleCategory('Cultural')"
                    :checked="selectedCategories.includes('Cultural')"
                  />
                  <span>Cultural</span>
                </label>
              </div>
            </div>
            
            <button @click="applyFilters" class="apply-filters-btn">
              Aplicar Filtros
            </button>
          </div>
        </aside>
        
        <!-- Right Content - Resultados -->
        <div class="results-section">
          <!-- Header -->
          <div class="results-header">
            <div>
              <h1 class="page-title">Explora el Patrimonio Nacional</h1>
              <p class="results-count">Mostrando {{ meta.total }} sitios históricos</p>
            </div>
            <div class="sort-controls">
              <label for="sort" class="sort-label">Ordenar por:</label>
              <select 
                id="sort"
                v-model="filters.order_by" 
                @change="applyFilters" 
                class="sort-select"
              >
                <option value="name">Nombre (A-Z)</option>
                <option value="created_at">Más Recientes</option>
                <option value="visits">Más Visitados</option>
              </select>
            </div>
          </div>
          
          <!-- Loading state -->
          <div v-if="loading && !sitios.length" class="loading-state">
            <div class="spinner"></div>
            <p>Cargando sitios...</p>
          </div>
          
          <!-- Error state -->
          <div v-else-if="error" class="error-state">
            <div class="error-icon">⚠️</div>
            <h3>Error al cargar sitios</h3>
            <p>{{ errorMessage }}</p>
            <button @click="loadSitios" class="retry-btn">Reintentar</button>
          </div>
          
          <!-- Empty state -->
          <div v-else-if="!sitios.length" class="empty-state">
            <div class="empty-icon">🔍</div>
            <h3>No se encontraron sitios</h3>
            <p>Intenta ajustar los filtros de búsqueda</p>
          </div>
          
          <!-- Sitios Grid -->
          <div v-else>
            <div class="sitios-grid">
              <router-link 
                v-for="sitio in sitios" 
                :key="sitio.id"
                :to="`/sitio/${sitio.id}`"
                class="site-card"
              >
                <div class="card-image-wrapper">
                  <img 
                    :src="sitio.imagen_principal || 'https://via.placeholder.com/400x300/17cf54/ffffff?text=Sin+Imagen'" 
                    :alt="sitio.nombre"
                    class="card-image"
                  />
                  <button class="favorite-btn" @click.prevent="toggleFavorite(sitio.id)">
                    <svg class="heart-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                    </svg>
                  </button>
                </div>
                <div class="card-content">
                  <h3 class="card-title">{{ sitio.nombre }}</h3>
                  <p class="card-location">{{ sitio.ciudad }}, {{ sitio.provincia }}</p>
                  <p class="card-description">{{ sitio.descripcion_breve || 'Sin descripción disponible' }}</p>
                  <div class="card-tags">
                    <span 
                      v-for="(tag, index) in sitio.tags?.slice(0, 2)" 
                      :key="index"
                      class="tag"
                    >
                      {{ tag }}
                    </span>
                  </div>
                </div>
              </router-link>
            </div>
            
            <!-- Paginación -->
            <nav class="pagination" aria-label="Pagination">
              <ul class="pagination-list">
                <li>
                  <button 
                    @click="goToPage(meta.page - 1)"
                    :disabled="meta.page === 1 || loading"
                    class="pagination-arrow"
                  >
                    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                    </svg>
                  </button>
                </li>
                <li v-for="pageNum in visiblePages" :key="pageNum">
                  <button
                    v-if="pageNum !== '...'"
                    @click="goToPage(pageNum)"
                    :class="['pagination-number', { active: pageNum === meta.page }]"
                    :disabled="loading"
                  >
                    {{ pageNum }}
                  </button>
                  <span v-else class="pagination-ellipsis">...</span>
                </li>
                <li>
                  <button 
                    @click="goToPage(meta.page + 1)"
                    :disabled="meta.page === meta.pages || loading"
                    class="pagination-arrow"
                  >
                    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </button>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import NavigationBar from '../components/NavigationBar.vue'
import SiteCard from '../components/SiteCard.vue'
import sitiosService from '../services/sitiosService'

const route = useRoute()
const router = useRouter()

const sitios = ref([])
const loading = ref(false)
const error = ref(false)
const errorMessage = ref('')

const filters = ref({
  name: '',
  city: '',
  province: '',
  order_by: 'name',
  page: 1,
  per_page: 12
})

const selectedProvinces = ref([])
const selectedCategories = ref(['Arquitectónico', 'Cultural'])

const meta = ref({
  total: 0,
  page: 1,
  per_page: 12,
  pages: 1
})

// Debounce para búsqueda
let searchTimeout = null
const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    filters.value.page = 1
    applyFilters()
  }, 500)
}

const loadSitios = async () => {
  try {
    loading.value = true
    error.value = false
    
    const params = {
      page: filters.value.page,
      per_page: filters.value.per_page,
      order_by: filters.value.order_by,
    }
    
    if (filters.value.name) params.name = filters.value.name
    if (filters.value.city) params.city = filters.value.city
    if (filters.value.province) params.province = filters.value.province
    
    const response = await sitiosService.getSitios(params)
    sitios.value = response.sitios || []
    meta.value = response.meta || { total: 0, page: 1, per_page: 12, pages: 1 }
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' })
    
  } catch (err) {
    console.error('Error al cargar sitios:', err)
    error.value = true
    errorMessage.value = err.response?.data?.message || 'Error al cargar los sitios'
  } finally {
    loading.value = false
  }
}

const applyFilters = () => {
  filters.value.page = 1
  updateURL()
  loadSitios()
}

const toggleProvince = (province) => {
  const index = selectedProvinces.value.indexOf(province)
  if (index > -1) {
    selectedProvinces.value.splice(index, 1)
  } else {
    selectedProvinces.value.push(province)
  }
}

const toggleCategory = (category) => {
  const index = selectedCategories.value.indexOf(category)
  if (index > -1) {
    selectedCategories.value.splice(index, 1)
  } else {
    selectedCategories.value.push(category)
  }
}

const toggleFavorite = (sitioId) => {
  console.log('Toggle favorite:', sitioId)
  // Aquí implementar la lógica de favoritos
}

const clearFilters = () => {
  filters.value = {
    name: '',
    city: '',
    province: '',
    order_by: 'name',
    page: 1,
    per_page: 12
  }
  selectedProvinces.value = []
  selectedCategories.value = []
  updateURL()
  loadSitios()
}

const goToPage = (page) => {
  if (page < 1 || page > meta.value.pages) return
  filters.value.page = page
  updateURL()
  loadSitios()
}

const updateURL = () => {
  const query = {}
  if (filters.value.name) query.name = filters.value.name
  if (filters.value.city) query.city = filters.value.city
  if (filters.value.province) query.province = filters.value.province
  if (filters.value.order_by !== 'name') query.order_by = filters.value.order_by
  if (filters.value.page > 1) query.page = filters.value.page
  
  router.push({ query })
}

const loadFiltersFromURL = () => {
  if (route.query.name) filters.value.name = route.query.name
  if (route.query.city) filters.value.city = route.query.city
  if (route.query.province) filters.value.province = route.query.province
  if (route.query.order_by) filters.value.order_by = route.query.order_by
  if (route.query.page) filters.value.page = parseInt(route.query.page)
}

// Calcular páginas visibles en la paginación
const visiblePages = computed(() => {
  const current = meta.value.page
  const total = meta.value.pages
  const pages = []
  
  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    if (current <= 4) {
      for (let i = 1; i <= 5; i++) pages.push(i)
      pages.push('...')
      pages.push(total)
    } else if (current >= total - 3) {
      pages.push(1)
      pages.push('...')
      for (let i = total - 4; i <= total; i++) pages.push(i)
    } else {
      pages.push(1)
      pages.push('...')
      for (let i = current - 1; i <= current + 1; i++) pages.push(i)
      pages.push('...')
      pages.push(total)
    }
  }
  
  return pages
})

onMounted(() => {
  loadFiltersFromURL()
  loadSitios()
})
</script>

<style scoped>
.sitios-catalog-page {
  min-height: 100vh;
  background: #f6f8f6;
  font-family: 'Public Sans', sans-serif;
}

.main-content {
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 32px 24px;
}

.content-wrapper {
  display: flex;
  gap: 32px;
}

/* Left Sidebar - Filtros */
.filters-sidebar {
  width: 280px;
  flex-shrink: 0;
}

.filters-container {
  position: sticky;
  top: 96px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e7f3eb;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.filters-header h3 {
  font-size: 1.125rem;
  font-weight: 700;
  color: #0e1b12;
  margin: 0;
}

.clear-link {
  font-size: 0.875rem;
  font-weight: 500;
  color: #17cf54;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  text-decoration: underline;
}

.clear-link:hover {
  color: #12a842;
}

.filter-group {
  margin-bottom: 24px;
}

.filter-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #0e1b12;
  margin-bottom: 8px;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 12px;
  width: 20px;
  height: 20px;
  color: #4e9767;
  stroke-width: 2;
}

.filter-search-input {
  width: 100%;
  height: 44px;
  padding: 0 12px 0 40px;
  background: #e7f3eb;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  color: #0e1b12;
}

.filter-search-input::placeholder {
  color: #4e9767;
}

.filter-search-input:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(23, 207, 84, 0.2);
}

.filter-subtitle {
  font-size: 0.875rem;
  font-weight: 500;
  color: #0e1b12;
  margin-bottom: 8px;
}

.checkbox-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.checkbox-item input[type="checkbox"] {
  width: 20px;
  height: 20px;
  border: 2px solid #d0e7d7;
  border-radius: 4px;
  cursor: pointer;
  accent-color: #17cf54;
}

.checkbox-item span {
  font-size: 0.875rem;
  color: #0e1b12;
}

.apply-filters-btn {
  width: 100%;
  height: 44px;
  background: #17cf54;
  color: #0e1b12;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.apply-filters-btn:hover {
  background: #12a842;
}

/* Results Section */
.results-section {
  flex: 1;
  min-width: 0;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  gap: 16px;
}

.page-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #0e1b12;
  margin: 0 0 8px 0;
}

.results-count {
  font-size: 1rem;
  color: #4e9767;
  margin: 0;
}

.sort-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.sort-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #0e1b12;
  white-space: nowrap;
}

.sort-select {
  background: #e7f3eb;
  border: none;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 0.875rem;
  color: #0e1b12;
  cursor: pointer;
}

.sort-select:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(23, 207, 84, 0.2);
}

.loading-state,
.error-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  text-align: center;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #e5e7eb;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-icon,
.empty-icon {
  font-size: 4rem;
  margin-bottom: 16px;
}

.retry-btn {
  margin-top: 16px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

/* Sitios Grid */
.sitios-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 48px;
}

.site-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #e7f3eb;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  text-decoration: none;
  display: flex;
  flex-direction: column;
}

.site-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

.card-image-wrapper {
  position: relative;
  width: 100%;
  height: 192px;
  overflow: hidden;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.favorite-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 36px;
  height: 36px;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(8px);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.favorite-btn:hover {
  background: rgba(0, 0, 0, 0.5);
}

.heart-icon {
  width: 20px;
  height: 20px;
  color: white;
  stroke-width: 2;
}

.card-content {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #0e1b12;
  margin: 0;
  transition: color 0.2s;
}

.site-card:hover .card-title {
  color: #17cf54;
}

.card-location {
  font-size: 0.875rem;
  color: #4e9767;
  margin: 0;
}

.card-description {
  font-size: 0.875rem;
  color: #0e1b12;
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
}

.tag {
  font-size: 0.75rem;
  font-weight: 500;
  background: rgba(23, 207, 84, 0.15);
  color: #17cf54;
  padding: 4px 12px;
  border-radius: 999px;
}

/* Paginación */
.pagination {
  display: flex;
  justify-content: center;
  padding-top: 32px;
}

.pagination-list {
  display: flex;
  align-items: center;
  gap: 0;
  list-style: none;
  padding: 0;
  margin: 0;
}

.pagination-arrow,
.pagination-number {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 40px;
  height: 40px;
  padding: 0 16px;
  background: white;
  border: 1px solid #e7f3eb;
  color: #4e9767;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  margin-left: -1px;
}

.pagination-arrow:first-child {
  border-top-left-radius: 8px;
  border-bottom-left-radius: 8px;
  margin-left: 0;
}

.pagination-arrow:last-child {
  border-top-right-radius: 8px;
  border-bottom-right-radius: 8px;
}

.pagination-arrow svg,
.pagination-number svg {
  width: 20px;
  height: 20px;
  stroke-width: 2;
}

.pagination-arrow:hover:not(:disabled),
.pagination-number:hover:not(:disabled) {
  background: #f6f8f6;
  color: #0e1b12;
}

.pagination-arrow:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.pagination-number.active {
  background: #17cf54;
  color: white;
  border-color: #17cf54;
  z-index: 1;
}

.pagination-ellipsis {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 40px;
  height: 40px;
  padding: 0 8px;
  color: #4e9767;
  border: none;
  background: transparent;
}

/* Responsive */
@media (max-width: 1024px) {
  .content-wrapper {
    flex-direction: column;
  }
  
  .filters-sidebar {
    width: 100%;
    order: -1;
  }
  
  .filters-container {
    position: static;
  }
  
  .sitios-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }
}

@media (max-width: 768px) {
  .main-content {
    padding: 24px 16px;
  }
  
  .results-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
  
  .sort-controls {
    width: 100%;
  }
  
  .sort-select {
    flex: 1;
  }
  
  .sitios-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .pagination-arrow,
  .pagination-number {
    min-width: 36px;
    height: 36px;
    padding: 0 12px;
    font-size: 0.875rem;
  }
}

@media (max-width: 480px) {
  .pagination-arrow svg {
    width: 18px;
    height: 18px;
  }
  
  .pagination-number {
    min-width: 32px;
    height: 32px;
    padding: 0 8px;
  }
}
</style>
