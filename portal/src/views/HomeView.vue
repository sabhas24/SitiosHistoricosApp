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
          :filter-params="{ sort: 'visits', order: 'desc' }"
        />
        
        <FeaturedSection
          title="Mejor puntuados"
          endpoint="/sitios/mejor-puntuados"
          empty-message="No hay sitios puntuados aún"
          :filter-params="{ sort: 'rating', order: 'desc' }"
        />
        
        <FeaturedSection
          title="Favoritos"
          endpoint="/sitios/favoritos"
          empty-message="Aún no tienes sitios favoritos"
          :filter-params="{ favorited: 'true' }"
        />
        
        <FeaturedSection
          title="Recientemente agregados"
          endpoint="/sitios/recientes"
          empty-message="No hay sitios agregados recientemente"
          :filter-params="{ sort: 'created_at', order: 'desc' }"
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

// ESTADO AUTENTICACION MOCK
const isAuthenticated = ref(false)

onMounted(() => {
  //VERIFICAR AUTENTICACION REAL CUANDO ESTE LA API, POR DEFECTO USUARIO NO AUTENTICADO
  isAuthenticated.value = false
})
</script>

<style scoped>
.home-page {
  min-height: 100vh;
}

.main-content {
  padding: 40px 0 80px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

@media (max-width: 768px) {
  .main-content {
    padding: 32px 0 60px;
  }
  
  .container {
    padding: 0 16px;
  }
}
</style>
