<template>
  <div class="map-page">
    <NavigationBar />
    
    <main class="main-content">
      <div class="container">
        <div class="map-header">
          <h1>Mapa de Sitios Históricos</h1>
          <p class="subtitle">
            Explora la ubicación de todos los sitios históricos de Buenos Aires
          </p>
        </div>
        
        <div class="map-container">
          <div class="map-wrapper">
            <l-map ref="map" v-model:zoom="zoom" :center="center" class="leaflet-map">
              <l-tile-layer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                layer-type="base"
                name="OpenStreetMap"
                attribution="&copy; OpenStreetMap contributors"
              ></l-tile-layer>
              
              <!-- Marcadores de sitios históricos -->
              <l-marker 
                v-for="site in sites" 
                :key="site.id"
                :lat-lng="[site.latitude, site.longitude]"
                @click="selectSite(site)"
              >
                <l-popup>
                  <div class="popup-content">
                    <h4>{{ site.name }}</h4>
                    <p>{{ site.address }}</p>
                    <div v-if="site.rating" class="popup-rating">
                      <span class="stars">
                        <span v-for="n in Math.floor(site.rating)" :key="n">⭐</span>
                      </span>
                      <span>{{ site.rating.toFixed(1) }}</span>
                    </div>
                    <button @click="showSiteInfo(site)" class="popup-link">
                      Ver detalles →
                    </button>
                  </div>
                </l-popup>
              </l-marker>
            </l-map>
          </div>
          
          <!-- Panel lateral con lista de sitios -->
          <aside class="sites-sidebar">
            <div class="sidebar-header">
              <h3>Sitios en el mapa</h3>
              <div class="search-filter">
                <input 
                  v-model="searchTerm" 
                  type="text" 
                  placeholder="Buscar sitios..."
                  class="search-input"
                />
              </div>
            </div>
            
            <div class="sites-list">
              <div 
                v-for="site in filteredSites" 
                :key="site.id"
                class="site-item"
                :class="{ active: selectedSite?.id === site.id }"
                @click="focusOnSite(site)"
              >
                <div class="site-info">
                  <h4 class="site-name">{{ site.name }}</h4>
                  <p class="site-address">{{ site.address }}</p>
                  <div v-if="site.rating" class="site-rating">
                    <span class="stars">
                      <span v-for="n in Math.floor(site.rating)" :key="n">⭐</span>
                    </span>
                    <span class="rating-value">{{ site.rating.toFixed(1) }}</span>
                  </div>
                </div>
                <button @click="showSiteInfo(site)" class="view-btn">
                  Ver →
                </button>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </main>
  </div>
</template>

</script>

<!-- Styles converted to Tailwind utilities; component uses Tailwind classes now -->
import L from 'leaflet';
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

export default {
  components: {
    NavigationBar,
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
  },
  data() {
    return {
      zoom: 12,
      center: [-34.6118, -58.3960],
      searchTerm: '',
      selectedSite: null,
      sites: [
        {
          id: 1,
          name: 'EJEMPLO',
          address: 'Del Valle Iberlucea 1100',
          latitude: -34.6395,
          longitude: -58.3636,
          rating: 4.5
        },
        {
          id: 2,
          name: 'EJEMPLO2',
          address: 'Cerrito 628',
          latitude: -34.6010,
          longitude: -58.3834,
          rating: 4.8
        }
      ]
    };
  },
  computed: {
    filteredSites() {
      if (!this.searchTerm) return this.sites;
      return this.sites.filter(site => 
        site.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        site.address.toLowerCase().includes(this.searchTerm.toLowerCase())
      );
    }
  },
  methods: {
    selectSite(site) {
      this.selectedSite = site;
    },
    focusOnSite(site) {
      this.selectedSite = site;
      this.center = [site.latitude, site.longitude];
      this.zoom = 16;
    },
    showSiteInfo(site) {
      //MOSTRAR INFO DETALLADA DE SITIO
      console.log('Mostrando información de:', site.name);
      this.selectSite(site);
    }
  },
  mounted() {
    // CARGAR SITIOS REALES DESDE LA API
  }
};
</script>

<!-- Styles moved to Tailwind / main.css utilities -->
.popup-content p {
  margin: 0 0 8px 0;
  color: #6b7280;
  font-size: 0.9rem;
}

.popup-rating {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 8px 0;
  font-size: 0.9rem;
}

.popup-link {
  display: inline-block;
  margin-top: 8px;
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
}

.popup-link:hover {
  text-decoration: underline;
}

.sites-sidebar {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.sidebar-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 16px;
}

.search-input {
  width: 100%;
  padding: 10px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.9rem;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
}

.sites-list {
  flex: 1;
  overflow-y: auto;
}

.site-item {
  padding: 16px 24px;
  border-bottom: 1px solid #e5e7eb;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.site-item:hover,
.site-item.active {
  background-color: #f9fafb;
}

.site-info {
  flex: 1;
}

.site-name {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 4px 0;
}

.site-address {
  font-size: 0.85rem;
  color: #6b7280;
  margin: 0 0 8px 0;
}

.site-rating {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
}

.stars {
  line-height: 1;
}

.rating-value {
  color: #6b7280;
  font-weight: 500;
}

.view-btn {
  color: #3b82f6;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.view-btn:hover {
  background-color: rgba(59, 130, 246, 0.1);
  text-decoration: none;
}

@media (max-width: 1024px) {
  .map-container {
    grid-template-columns: 1fr;
    grid-template-rows: 400px auto;
    height: auto;
  }
  
  .sites-sidebar {
    max-height: 300px;
  }
}

@media (max-width: 768px) {
  .main-content {
    padding: 20px 0;
  }
  
  .container {
    padding: 0 16px;
  }
  
  .map-header h1 {
    font-size: 2rem;
  }
  
  .map-container {
    gap: 16px;
    grid-template-rows: 350px auto;
  }
  
  .sidebar-header,
  .site-item {
    padding: 16px;
  }
}
</style>


