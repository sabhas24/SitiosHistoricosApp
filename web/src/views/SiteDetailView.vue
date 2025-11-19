<template>
  <div class="site-detail-page">
    <NavigationBar />
    
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Cargando sitio...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <div class="error-icon">⚠️</div>
      <h2>Error al cargar el sitio</h2>
      <p>{{ errorMessage }}</p>
      <button @click="loadSitio" class="retry-btn">Reintentar</button>
      <router-link to="/" class="back-btn">Volver al inicio</router-link>
    </div>
    
    <div v-else-if="sitio" class="site-detail">
      <!-- Hero Section con imagen -->
      <div class="hero-section">
        <img 
          :src="getSiteImageUrl()"
          :alt="sitio.nombre"
        />
        <div class="hero-overlay"></div>
        <div class="hero-content">
          <div class="container">
            <h1 class="site-title">{{ sitio.nombre }}</h1>
            <p class="site-location">
              <span class="icon">📍</span>
              {{ formatLocation(sitio) }}
            </p>
          </div>
        </div>
      </div>
      
      <!-- Contenido principal -->
      <div class="main-content">
        <div class="container">
          <div class="content-grid">
            <!-- Columna principal -->
            <div class="main-column">
              <!-- Descripción Breve -->
              <section v-if="sitio.descripcion_breve" class="section">
                <h2>Descripción</h2>
                <p class="description">{{ sitio.descripcion_breve }}</p>
              </section>
              
              <!-- Descripción Completa -->
              <section v-if="sitio.descripcion_completa" class="section">
                <h2>Historia y Detalles</h2>
                <p class="historia">{{ sitio.descripcion_completa }}</p>
              </section>
            </div>
            
            <!-- Sidebar -->
            <div class="sidebar">
              <!-- Información básica -->
              <div class="info-card">
                <h3>Información</h3>
                <div class="info-item">
                  <span class="label">Ciudad:</span>
                  <span class="value">{{ sitio.ciudad }}</span>
                </div>
                <div class="info-item">
                  <span class="label">Provincia:</span>
                  <span class="value">{{ sitio.provincia }}</span>
                </div>
                <div class="info-item" v-if="sitio.categoria">
                  <span class="label">Categoría:</span>
                  <span class="value">{{ sitio.categoria }}</span>
                </div>
                <div class="info-item" v-if="sitio.anio_inauguracion">
                  <span class="label">Año inauguración:</span>
                  <span class="value">{{ sitio.anio_inauguracion }}</span>
                </div>
                <div class="info-item" v-if="sitio.estado_conservacion">
                  <span class="label">Estado:</span>
                  <span class="value">
                    <span :class="['badge', `badge-${sitio.estado_conservacion.toLowerCase()}`]">
                      {{ sitio.estado_conservacion }}
                    </span>
                  </span>
                </div>
              </div>
              
              <!-- Tags -->
              <div v-if="sitio.tags && sitio.tags.length > 0" class="info-card">
                <h3>Etiquetas</h3>
                <div class="tags-list">
                  <span 
                    v-for="(tag, index) in sitio.tags" 
                    :key="index"
                    class="tag"
                  >
                    {{ tag }}
                  </span>
                </div>
              </div>
              
              <!-- Mapa Leaflet -->
              <div v-if="sitio.latitud && sitio.longitud" class="info-card">
                <h3>Ubicación en el Mapa</h3>
                <div id="map" class="leaflet-map"></div>
                <a 
                  :href="`https://www.google.com/maps?q=${sitio.latitud},${sitio.longitud}`"
                  target="_blank"
                  class="map-link"
                >
                  Abrir en Google Maps →
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import NavigationBar from '../components/NavigationBar.vue'
import sitiosService from '../services/sitiosService'
import { minioImg } from '../utils/minioImages'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const route = useRoute()
const router = useRouter()

const sitio = ref(null)
const loading = ref(true)
const error = ref(false)
const errorMessage = ref('')
let map = null

const loadSitio = async () => {
  try {
    loading.value = true
    error.value = false
    
    const sitioId = parseInt(route.params.id)
    
    if (isNaN(sitioId)) {
      throw new Error('ID de sitio inválido')
    }
    
    const response = await sitiosService.getSitioById(sitioId)
    sitio.value = response
    
    // Inicializar mapa después de cargar el sitio
    await nextTick()
    if (sitio.value.latitud && sitio.value.longitud) {
      initMap()
    }
    
  } catch (err) {
    console.error('Error al cargar sitio:', err)
    error.value = true
    errorMessage.value = err.response?.data?.message || 'No se pudo cargar el sitio'
  } finally {
    loading.value = false
  }
}

const initMap = () => {
  // Esperar un poco para asegurar que el DOM está listo
  setTimeout(() => {
    const mapElement = document.getElementById('map')
    if (!mapElement || map) return
    
    // Crear mapa
    map = L.map('map').setView([sitio.value.latitud, sitio.value.longitud], 15)
    
    // Agregar tiles de OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19
    }).addTo(map)
    
    // Agregar marcador
    const marker = L.marker([sitio.value.latitud, sitio.value.longitud]).addTo(map)
    marker.bindPopup(`<b>${sitio.value.nombre}</b><br>${sitio.value.ciudad}, ${sitio.value.provincia}`)
  }, 100)
}

const getSiteImageUrl = () => {
  // Prioridad: imagen_principal > primera imagen del array > placeholder
  if (sitio.value?.imagen_principal) {
    return minioImg(sitio.value.imagen_principal)
  }
  if (sitio.value?.imagenes && sitio.value.imagenes.length > 0) {
    return minioImg(sitio.value.imagenes[0].url_publica)
  }
  return minioImg()
}

const getPlaceholderImage = () => {
  return getSiteImageUrl()
}

const formatLocation = (site) => {
  const parts = []
  if (site.ciudad) parts.push(site.ciudad)
  if (site.provincia) parts.push(site.provincia)
  return parts.join(', ') || 'Ubicación no especificada'
}

onMounted(() => {
  loadSitio()
})

onUnmounted(() => {
  if (map) {
    map.remove()
    map = null
  }
})
</script>

<style scoped>
.site-detail-page {
  min-height: 100vh;
  background: #f9fafb;
}

.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  padding: 40px 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #e5e7eb;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-icon {
  font-size: 4rem;
  margin-bottom: 16px;
}

.error-container h2 {
  color: #1f2937;
  margin-bottom: 8px;
}

.error-container p {
  color: #6b7280;
  margin-bottom: 24px;
}

.retry-btn,
.back-btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  display: inline-block;
  margin: 8px;
}

.retry-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
}

.back-btn {
  background: white;
  color: #667eea;
  border: 2px solid #667eea;
}

.hero-section {
  position: relative;
  height: 50vh;
  min-height: 400px;
  overflow: hidden;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.7) 0%, rgba(118, 75, 162, 0.7) 100%);
}

.hero-content {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: flex-end;
  padding: 60px 0;
}

.site-title {
  font-size: 3rem;
  font-weight: 800;
  color: white;
  margin: 0 0 16px 0;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.site-location {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.95);
  display: flex;
  align-items: center;
  gap: 8px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.main-content {
  padding: 60px 0 100px;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 40px;
}

.main-column {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.section h2 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 16px;
}

.description,
.historia {
  font-size: 1.1rem;
  line-height: 1.7;
  color: #4b5563;
}

.image-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.gallery-item {
  aspect-ratio: 1;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s;
}

.gallery-item:hover {
  transform: scale(1.05);
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.info-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.info-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 16px 0;
}

.rating-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.rating-stars {
  display: flex;
  gap: 4px;
}

.star {
  font-size: 1.5rem;
  filter: grayscale(1);
  opacity: 0.3;
}

.star.filled {
  filter: none;
  opacity: 1;
}

.rating-number {
  font-size: 2rem;
  font-weight: 700;
  color: #667eea;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f3f4f6;
}

.info-item:last-child {
  border-bottom: none;
}

.info-item .label {
  font-weight: 600;
  color: #6b7280;
}

.info-item .value {
  color: #1f2937;
  text-align: right;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  padding: 6px 16px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  color: #667eea;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.leaflet-map {
  height: 300px;
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 12px;
}

.map-link {
  display: block;
  text-align: center;
  margin-top: 12px;
  color: #667eea;
  font-weight: 600;
  text-decoration: none;
  padding: 10px;
  background: rgba(102, 126, 234, 0.08);
  border-radius: 6px;
  transition: all 0.2s;
}

.map-link:hover {
  background: rgba(102, 126, 234, 0.15);
  text-decoration: none;
}

.badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.badge-bueno {
  background: #d1fae5;
  color: #065f46;
}

.badge-regular {
  background: #fef3c7;
  color: #92400e;
}

.badge-malo {
  background: #fee2e2;
  color: #991b1b;
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .sidebar {
    order: -1;
  }
}

@media (max-width: 768px) {
  .hero-section {
    height: 40vh;
    min-height: 300px;
  }
  
  .site-title {
    font-size: 2rem;
  }
  
  .site-location {
    font-size: 1rem;
  }
  
  .main-content {
    padding: 40px 0 60px;
  }
  
  .image-gallery {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  .sidebar {
    order: -1;
  }
}
</style>
