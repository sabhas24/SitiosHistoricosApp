<template>
  <div class="home-page">
    <NavigationBar />
    
    <HeroSection 
      project-title="PatrimonioBA"
      subtitle="Descubre y explora el patrimonio histórico de Buenos Aires"
    />
    
    <main class="main-content">
      <div class="container">
        
        <FeaturedSection
          title="Más visitados"
          endpoint="/sitios/mas-visitados"
          empty-message="No hay datos de visitas disponibles"
          :filter-params="{ sort: 'visits', order: 'latest' }"
        />
        
        <FeaturedSection
          title="Mejor puntuados"
          endpoint="/sitios/mejor-puntuados"
          empty-message="No hay sitios puntuados aún"
          :filter-params="{ sort: 'rating', order: 'latest' }"
        />
        
        <FeaturedSection
          v-if="authStore.isAuthenticated"
          title="Favoritos"
          endpoint="/sitios/favoritos"
          empty-message="Aún no tienes sitios favoritos"
          :filter-params="{ favorited: 'true' }"
        />
        
        <FeaturedSection
          title="Recientemente agregados"
          endpoint="/sitios/recientes"
          empty-message="No hay sitios agregados recientemente"
          :filter-params="{ sort: 'created_at', order: 'latest' }"
        />
        
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import NavigationBar from '../components/NavigationBar.vue'
import HeroSection from '../components/HeroSection.vue'
import FeaturedSection from '../components/FeaturedSection.vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

onMounted(() => {
})
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: #FDFBF7;
}

.main-content {
  padding-bottom: 60px;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
}

/* Removed styles for deleted sections (collections, map-preview, about) */
</style>
