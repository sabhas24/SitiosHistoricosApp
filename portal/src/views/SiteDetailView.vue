<template>
  <div class="site-detail-page">
    <NavigationBar />

    <section v-if="loading" class="state-card">
      <div class="spinner" />
      <p>Cargando sitio...</p>
    </section>

    <section v-else-if="error" class="state-card">
      <div class="error-icon">⚠️</div>
      <h2>No pudimos cargar el sitio</h2>
      <p>{{ errorMessage }}</p>
      <button class="primary-btn" @click="loadSitio">Reintentar</button>
      <router-link class="ghost-btn" to="/">Volver al inicio</router-link>
    </section>

    <section v-else-if="sitio" class="site-detail">
      <article class="hero-card">
        <img :src="heroImage" :alt="sitio.nombre" class="hero-img" />
        <div class="hero-overlay" />
        <div class="hero-text">
          <p class="hero-eyebrow">{{ sitio.categoria || 'Sitio histórico' }}</p>
          <h1>{{ sitio.nombre }}</h1>
          <p class="hero-subtitle">{{ sitio.descripcion_breve }}</p>
        </div>
        <button 
          class="hero-favorite-btn" 
          type="button" 
          v-if="sitio && sitio.id" 
          :class="{ 'is-favorite': isFavorite }"
          @click="toggleFavorite"
          title="Favoritos"
        >
          <svg
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
        </button>
      </article>

      <main class="detail-body">
        <div class="body-grid">
          <section class="narrative">
            <p class="lede">{{ sitio.descripcion_breve }}</p>

            <article class="info-block" v-if="sitio.descripcion_completa">
              <h2>Historia</h2>
              <p>{{ sitio.descripcion_completa }}</p>
            </article>

            <article class="info-block" v-if="sitio.descripcion_completa">
              <h2>Arquitectura y Simbolismo</h2>
              <p>{{ sitio.descripcion_completa }}</p>
            </article>
          </section>

          <aside class="sidebar">
            <div class="card datos-clave">
              <h3>Datos Clave</h3>
              <dl>
                <div class="dato" v-for="item in datosClave" :key="item.label">
                  <dt>{{ item.label }}</dt>
                  <dd>{{ item.value }}</dd>
                </div>
              </dl>
            </div>

            <div class="card info-practica">
              <h3>Información Práctica</h3>
              <div class="info-row" v-for="item in infoPractica" :key="item.label">
                <div class="info-icon">{{ item.icon }}</div>
                <div>
                  <p class="info-label">{{ item.label }}</p>
                  <p class="info-value">
                    <template v-if="item.href">
                      <a :href="item.href" target="_blank" rel="noopener">{{ item.value }}</a>
                    </template>
                    <template v-else>
                      {{ item.value }}
                    </template>
                  </p>
                </div>
              </div>
            </div>

          </aside>
        </div>
      </main>

      <section v-if="galleryImages.length" class="gallery-section">
        <h2>Galería</h2>
        <div class="gallery-grid">
          <figure
            v-for="(imagen, index) in galleryImages"
            :key="imagen.id || index"
            :class="['gallery-item', { featured: index === 0 }]"
          >
            <img :src="minioImg(imagen.url_publica)" :alt="imagen.titulo_alt || sitio.nombre" />
          </figure>
        </div>
      </section>

      <section v-if="sitio.latitud && sitio.longitud" class="map-section">
        <h2>Ubicación</h2>
        <div class="map-card">
          <div id="map" class="map-canvas" />
          <button class="map-btn" type="button" @click="openDirections">
            Abrir en Mapas
          </button>
        </div>
      </section>
    </section>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import NavigationBar from '../components/NavigationBar.vue'
import sitiosService from '../services/sitiosService'
import { minioImg } from '../utils/minioImages'
import api from '../config/api'

const route = useRoute()

const sitio = ref(null)
const loading = ref(true)
const error = ref(false)
const errorMessage = ref('Ocurrió un error inesperado.')
const isFavorite = ref(false)
let map = null

const heroImage = computed(() => {
  if (!sitio.value) return minioImg()
  if (sitio.value.imagen_principal) return minioImg(sitio.value.imagen_principal)
  const fallback = sitio.value.imagenes?.[0]?.url_publica
  return minioImg(fallback)
})

const galleryImages = computed(() => sitio.value?.imagenes || [])

const datosClave = computed(() => {
  if (!sitio.value) return []
  return [
    { label: 'Año de construcción', value: sitio.value.anio_inauguracion },
    { label: 'Estilo arquitectónico', value: sitio.value.categoria },
    {
      label: 'Estado',
      value: sitio.value.estado_conservacion || 'Monumento Histórico Nacional',
    },
  ].filter((item) => Boolean(item.value))
})

const infoPractica = computed(() => {
  if (!sitio.value) return []
  return [
    {
      icon: '📍',
      label: 'Dirección',
      value: `${sitio.value.ciudad || 'Ciudad'}, ${sitio.value.provincia || 'Provincia'}`,
    },
    {
      icon: '🕐',
      label: 'Horarios',
      value: 'Visitas guiadas: Lunes a Sábado, 10:00-18:00',
    },
    {
      icon: '🌐',
      label: 'Sitio Web',
      value: 'palaciobarolo.com.ar',
      href: '#',
    },
  ]
})

const loadSitio = async () => {
  try {
    loading.value = true
    error.value = false

    const sitioId = Number(route.params.id)
    if (Number.isNaN(sitioId)) {
      throw new Error('ID de sitio inválido')
    }

    const response = await sitiosService.getSitioById(sitioId)
    sitio.value = response

    await nextTick()
    if (sitio.value.latitud && sitio.value.longitud) {
      initMap()
    }
  } catch (err) {
    console.error('Error al cargar sitio', err)
    error.value = true
    errorMessage.value = err.response?.data?.message || err.message
  } finally {
    loading.value = false
  }
}

const initMap = () => {
  setTimeout(() => {
    const mapElement = document.getElementById('map')
    if (!mapElement || map) return

    map = L.map('map', { scrollWheelZoom: false }).setView(
      [sitio.value.latitud, sitio.value.longitud],
      15,
    )

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
    }).addTo(map)

    L.marker([sitio.value.latitud, sitio.value.longitud])
      .addTo(map)
      .bindPopup(`<b>${sitio.value.nombre}</b><br>${sitio.value.ciudad || ''}`)
  }, 150)
}

const openDirections = () => {
  if (!sitio.value?.latitud || !sitio.value?.longitud) return
  const url = `https://www.google.com/maps/dir/?api=1&destination=${sitio.value.latitud},${sitio.value.longitud}`
  window.open(url, '_blank')
}

const toggleFavorite = async () => {
  try {
    if (isFavorite.value) {
      await api.delete(`/sitios/${sitio.value.id}/favoritos`)
      isFavorite.value = false
    } else {
      await api.put(`/sitios/${sitio.value.id}/favoritos`)
      isFavorite.value = true
    }
  } catch (err) {
    console.error('Error toggling favorite:', err)
  }
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
:global(body) {
  background: #f9f5ef;
}

.site-detail-page {
  min-height: 100vh;
  background: #f9f5ef;
  padding-bottom: 80px;
}

.state-card {
  max-width: 960px;
  margin: 80px auto;
  padding: 48px;
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 15px 45px rgba(15, 23, 42, 0.08);
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: center;
}

.spinner {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 4px solid #e5e7eb;
  border-top-color: #2563eb;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.primary-btn,
.ghost-btn {
  padding: 12px 32px;
  border-radius: 999px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  text-decoration: none;
}

.primary-btn {
  background: #2563eb;
  color: #fff;
}

.ghost-btn {
  border: 1px solid #d1d5db;
  color: #1f2937;
}

.hero-card {
  position: relative;
  max-width: 1100px;
  margin: 48px auto;
  border-radius: 28px;
  overflow: hidden;
  box-shadow: 0 25px 60px rgba(15, 23, 42, 0.2);
}

.hero-img {
  width: 100%;
  height: 480px;
  object-fit: cover;
  display: block;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.05) 0%, rgba(0, 0, 0, 0.75) 100%);
}

.hero-text {
  position: absolute;
  bottom: 32px;
  left: 48px;
  right: 48px;
  color: #fff;
}

.hero-eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-size: 0.8rem;
  margin-bottom: 12px;
}

.hero-text h1 {
  font-size: clamp(2.5rem, 5vw, 3.4rem);
  margin: 0 0 12px;
  font-weight: 600;
}

.hero-subtitle {
  font-size: 1.1rem;
  max-width: 60ch;
  margin: 0;
}

.detail-body {
  max-width: 1100px;
  margin: 0 auto;
}

.body-grid {
  display: grid;
  grid-template-columns: minmax(0, 3fr) minmax(0, 1.4fr);
  gap: 32px;
}

.narrative {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.lede {
  font-size: 1.15rem;
  line-height: 1.8;
  color: #374151;
  margin: 0;
}

.info-block {
  background: #fff;
  border-radius: 20px;
  padding: 32px;
  box-shadow: inset 0 0 0 1px #f3f4f6;
}

.info-block h2 {
  margin: 0 0 16px;
  font-size: 1.8rem;
  color: #111827;
}

.info-block p {
  margin: 0;
  line-height: 1.7;
  color: #4b5563;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.card {
  background: #fff;
  border-radius: 20px;
  padding: 28px;
  box-shadow: inset 0 0 0 1px #f1f5f9;
}

.card h3 {
  margin: 0 0 16px;
  font-size: 1.2rem;
  color: #111827;
}

.datos-clave dl {
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.dato dt {
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: #9ca3af;
  margin-bottom: 4px;
}

.dato dd {
  margin: 0;
  font-size: 1.15rem;
  color: #111827;
  font-weight: 600;
}

.info-row {
  display: flex;
  gap: 16px;
  padding: 14px 0;
  border-bottom: 1px solid #f1f5f9;
}

.info-row:last-child {
  border-bottom: none;
}

.info-icon {
  font-size: 1.4rem;
}

.info-label {
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  margin: 0;
  color: #9ca3af;
}

.info-value {
  margin: 4px 0 0;
  color: #1f2937;
}

.info-value a {
  color: #2563eb;
  text-decoration: none;
}

.hero-favorite-btn {
  position: absolute;
  top: 24px;
  right: 24px;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.2s ease;
  z-index: 10;
  color: #64748b;
}

.hero-favorite-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
}

.hero-favorite-btn.is-favorite {
  color: #e11d48;
  background: rgba(255, 255, 255, 1);
}

.hero-favorite-btn svg {
  width: 24px;
  height: 24px;
}

.gallery-section,
.map-section {
  max-width: 1100px;
  margin: 48px auto 0;
}

.gallery-section h2,
.map-section h2 {
  font-size: 1.6rem;
  margin-bottom: 20px;
  color: #111827;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
}

.gallery-item {
  border-radius: 18px;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(15, 23, 42, 0.1);
}

.gallery-item.featured {
  grid-row: span 2;
  grid-column: span 2;
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.map-card {
  background: #fff;
  border-radius: 20px;
  padding: 20px;
  box-shadow: inset 0 0 0 1px #f1f5f9;
}

.map-canvas {
  height: 320px;
  border-radius: 16px;
  overflow: hidden;
}

.map-btn {
  margin-top: 16px;
  padding: 12px 20px;
  background: #0f172a;
  color: #fff;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
}

@media (max-width: 960px) {
  .body-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }
}

@media (max-width: 640px) {
  .hero-text {
    left: 24px;
    right: 24px;
  }

  .hero-img {
    height: 360px;
  }

  .gallery-item.featured {
    grid-column: span 1;
    grid-row: span 1;
  }
}
</style>
