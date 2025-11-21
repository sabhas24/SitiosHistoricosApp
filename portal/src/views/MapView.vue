<template>
  <div class="map-view">
    <NavigationBar />
    
    <div class="map-container">
      <div id="interactive-map" class="map-canvas"></div>
      
      <div class="map-controls">
        <div class="control-info">
          <p class="info-text">
            <span class="icon">📍</span>
            <strong>{{ sitesCount }}</strong> sitios encontrados
          </p>
          <p class="info-hint">Mueve y haz zoom en el mapa para explorar</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import NavigationBar from '../components/NavigationBar.vue'
import sitiosService from '../services/sitiosService'
import { minioImg } from '../utils/minioImages'

const sitesCount = ref(0)
let map = null
let markers = []

// Coordenadas del centro de Argentina
const DEFAULT_CENTER = [-38.4161, -63.6167]
const DEFAULT_ZOOM = 5

// Función para calcular el radio en metros basado en el nivel de zoom
const calculateRadius = (zoom) => {
  // Fórmula aproximada: a mayor zoom, menor radio
  // Zoom 5 (país completo) = ~500km
  // Zoom 10 (provincia) = ~50km
  // Zoom 15 (ciudad) = ~5km
  const baseRadius = 500000 // 500km en metros
  const radiusMeters = baseRadius / Math.pow(2, zoom - 5)
  return Math.max(radiusMeters, 1000) // Mínimo 1km
}

// Función para limpiar marcadores existentes
const clearMarkers = () => {
  markers.forEach(marker => map.removeLayer(marker))
  markers = []
}

// Función para cargar y mostrar sitios
const loadSites = async () => {
  if (!map) return

  const center = map.getCenter()
  const zoom = map.getZoom()
  const radius = calculateRadius(zoom)

  try {
    const response = await sitiosService.getSitios({
      lat: center.lat,
      long: center.lng,
      radius: radius,
      per_page: 100
    })

    clearMarkers()
    
    const sites = response.sitios || []
    sitesCount.value = sites.length

    sites.forEach(site => {
      if (site.latitud && site.longitud) {
        const marker = L.marker([site.latitud, site.longitud], {
          icon: L.divIcon({
            className: 'custom-marker',
            html: `<div class="marker-pin">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#dc2626">
                      <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                    </svg>
                  </div>`,
            iconSize: [40, 50],
            iconAnchor: [20, 50],
            popupAnchor: [0, -50]
          })
        })

        const popupContent = `
          <div class="marker-popup">
            <img src="${minioImg(site.imagen_principal)}" alt="${site.nombre}" class="popup-image" />
            <h3 class="popup-title">${site.nombre}</h3>
            <p class="popup-location">${site.ciudad || ''}, ${site.provincia || ''}</p>
            <p class="popup-rating">⭐ ${site.calificacion_promedio?.toFixed(1) || 'N/A'}</p>
            <a href="/sitio/${site.id}" class="popup-link">Ver detalles →</a>
          </div>
        `

        marker.bindPopup(popupContent, {
          maxWidth: 250,
          className: 'custom-popup'
        })

        marker.addTo(map)
        markers.push(marker)
      }
    })
  } catch (error) {
    console.error('Error loading sites:', error)
  }
}

// Debounce para evitar demasiadas llamadas al mover el mapa
let loadTimeout = null
const debouncedLoadSites = () => {
  if (loadTimeout) clearTimeout(loadTimeout)
  loadTimeout = setTimeout(loadSites, 500)
}

onMounted(() => {
  // Inicializar el mapa
  map = L.map('interactive-map').setView(DEFAULT_CENTER, DEFAULT_ZOOM)

  // Agregar capa de tiles
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 18,
    minZoom: 4
  }).addTo(map)

  // Cargar sitios iniciales
  loadSites()

  // Escuchar eventos de movimiento y zoom
  map.on('moveend', debouncedLoadSites)
  map.on('zoomend', debouncedLoadSites)
})

onUnmounted(() => {
  if (map) {
    map.remove()
    map = null
  }
  if (loadTimeout) {
    clearTimeout(loadTimeout)
  }
})
</script>

<style scoped>
.map-view {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.map-container {
  flex: 1;
  position: relative;
  background: #f3f4f6;
}

.map-canvas {
  width: 100%;
  height: 100%;
}

.map-controls {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 1000;
}

.control-info {
  background: white;
  border-radius: 12px;
  padding: 16px 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 200px;
}

.info-text {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #1f2937;
  display: flex;
  align-items: center;
  gap: 8px;
}

.icon {
  font-size: 20px;
}

.info-text strong {
  color: #8B7355;
  font-weight: 700;
}

.info-hint {
  margin: 0;
  font-size: 12px;
  color: #6b7280;
}

/* Estilos para marcadores personalizados */
:deep(.custom-marker) {
  background: transparent;
  border: none;
}

:deep(.marker-pin) {
  width: 40px;
  height: 50px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
  transition: transform 0.2s;
}

:deep(.marker-pin:hover) {
  transform: scale(1.1);
}

/* Estilos para popups personalizados */
:deep(.custom-popup .leaflet-popup-content-wrapper) {
  border-radius: 12px;
  padding: 0;
  overflow: hidden;
}

:deep(.custom-popup .leaflet-popup-content) {
  margin: 0;
  width: 250px !important;
}

:deep(.marker-popup) {
  display: flex;
  flex-direction: column;
}

:deep(.popup-image) {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

:deep(.popup-title) {
  margin: 12px 12px 4px;
  font-size: 16px;
  font-weight: 700;
  color: #1f2937;
}

:deep(.popup-location) {
  margin: 0 12px 4px;
  font-size: 13px;
  color: #6b7280;
}

:deep(.popup-rating) {
  margin: 0 12px 12px;
  font-size: 14px;
  color: #8B7355;
  font-weight: 600;
}

:deep(.popup-link) {
  display: block;
  padding: 10px 12px;
  background: #8B7355;
  color: white;
  text-align: center;
  text-decoration: none;
  font-weight: 500;
  font-size: 14px;
  transition: background 0.2s;
}

:deep(.popup-link:hover) {
  background: #704a3a;
}

@media (max-width: 768px) {
  .map-controls {
    top: 10px;
    right: 10px;
  }

  .control-info {
    padding: 12px 16px;
    min-width: 160px;
  }

  .info-text {
    font-size: 14px;
  }

  .info-hint {
    font-size: 11px;
  }
}
</style>