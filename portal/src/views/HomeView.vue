<template>
  <div class="home-view">
    <NavigationBar :transparent="true" />

    <HeroSection />

    <main class="main-content">
      <div class="container content-wrapper">
        
        <FeaturedSection
          title="Más visitados"
          endpoint="/sitios/mas-visitados"
          empty-message="No hay datos de visitas disponibles"
          :filter-params="{order_by: 'visits_desc'}"
        />
        
        <FeaturedSection
          title="Mejor puntuados"
          endpoint="/sitios/mejor-puntuados"
          empty-message="No hay sitios puntuados aún"
          :filter-params="{order_by: 'rating_desc'}"
        />
        
        <FeaturedSection
          v-if="authStore.isAuthenticated"
          title="Favoritos"
          endpoint="/sitios/favoritos"
          empty-message="Aún no tienes sitios favoritos"
          :is-favorites="true"
        />
        
        <FeaturedSection
          title="Recientemente agregados"
          endpoint="/sitios/recientes"
          empty-message="No hay sitios agregados recientemente"
          :filter-params="{order_by: 'latest'}"
        />
        
      </div>
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import NavigationBar from '../components/NavigationBar.vue'
import HeroSection from '../components/HeroSection.vue'
import FeaturedSection from '../components/homeSection/FeaturedSection.vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

onMounted(() => {
})
</script>

<style scoped>
.home-view {
  min-height: 100vh;
}

.main-content {
  padding-bottom: 5rem;
}

.content-wrapper {
  padding-top: 3rem;
  padding-bottom: 3rem;
  display: flex;
  flex-direction: column;
  gap: 3rem;
}
</style>
