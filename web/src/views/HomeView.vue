<template>
  <div class="home-page">
    <NavigationBar />
    
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-image-container">
        <img 
          src="https://images.unsplash.com/photo-1589909202802-8f4aadce1849?w=1920&h=1080&fit=crop" 
          alt="Obelisco de Buenos Aires"
          class="hero-image"
        />
        <div class="hero-overlay"></div>
      </div>
      <div class="hero-content">
        <h1 class="hero-title">Redescubre la Historia de Buenos Aires</h1>
        <p class="hero-subtitle">
          Tu guía al corazón histórico de la ciudad, explorando sus joyas arquitectónicas 
          y las historias en cada esquina.
        </p>
        <router-link to="/sitios" class="hero-button">
          Comienza tu recorrido
        </router-link>
      </div>
    </section>
    
    <!-- Image Grid Section - Colecciones -->
    <section class="collections-section">
      <h2 class="section-title">Explora Nuestras Colecciones</h2>
      <div class="collections-grid">
        <div class="collection-card">
          <div class="collection-image" style="background-image: url('https://images.unsplash.com/photo-1564399579883-451a5d44ec08?w=600&h=800&fit=crop')"></div>
          <div class="collection-info">
            <h3>Joyas Arquitectónicas</h3>
            <p>Maravíllate con la arquitectura que cuenta la historia de la ciudad.</p>
          </div>
        </div>
        <div class="collection-card">
          <div class="collection-image" style="background-image: url('https://images.unsplash.com/photo-1558642084-fd07fae5282e?w=600&h=800&fit=crop')"></div>
          <div class="collection-info">
            <h3>Historias en cada Esquina</h3>
            <p>Descubre los secretos y leyendas que se esconden en las calles de BA.</p>
          </div>
        </div>
        <div class="collection-card">
          <div class="collection-image" style="background-image: url('https://images.unsplash.com/photo-1524661135-423995f22d0b?w=600&h=800&fit=crop')"></div>
          <div class="collection-info">
            <h3>Recorridos Imperdibles</h3>
            <p>Sigue nuestras rutas curadas para no perderte ningún detalle esencial.</p>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Interactive Map Preview -->
    <section class="map-preview-section">
      <h2 class="section-title">Mapa Interactivo de Sitios</h2>
      <div class="map-container">
        <div class="map-placeholder">
          <img 
            src="https://maps.geoapify.com/v1/staticmap?style=osm-bright&width=800&height=400&center=lonlat:-58.3816,-34.6037&zoom=12&apiKey=YOUR_API_KEY" 
            alt="Mapa de Buenos Aires"
            @error="handleMapError"
          />
        </div>
        <router-link to="/map" class="map-button">
          Ver Mapa Completo
        </router-link>
      </div>
    </section>
    
    <!-- About Us Section -->
    <section class="about-section">
      <div class="about-grid">
        <div class="about-content">
          <h2>Nuestra Misión</h2>
          <p>
            En PatrimoniosBA, nos dedicamos a preservar y difundir el invaluable patrimonio 
            cultural de Buenos Aires. Creemos que cada edificio, plaza y calle tiene una historia 
            que contar. Nuestra misión es hacer estas historias accesibles a todos, fomentando 
            una conexión más profunda entre los ciudadanos, los visitantes y el legado histórico 
            de la ciudad.
          </p>
        </div>
        <div class="about-image-container">
          <img 
            src="https://images.unsplash.com/photo-1609137144813-7d9921338f24?w=600&h=600&fit=crop" 
            alt="Detalle arquitectónico histórico"
            class="about-image"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import NavigationBar from '../components/NavigationBar.vue'

const isAuthenticated = ref(false)

const handleMapError = (event) => {
  event.target.src = 'https://via.placeholder.com/800x400/667eea/ffffff?text=Mapa+de+Buenos+Aires'
}

onMounted(() => {
  isAuthenticated.value = false
})
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: #FDFBF7;
}

/* Hero Section */
.hero-section {
  position: relative;
  min-height: calc(100vh - 68px);
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px 24px;
  overflow: hidden;
}

.hero-image-container {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(18, 26, 33, 0.7) 0%, rgba(18, 26, 33, 0.3) 50%, rgba(18, 26, 33, 0.1) 100%);
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 900px;
  margin: 0 auto;
}

.hero-title {
  font-size: 4rem;
  font-weight: 900;
  color: white;
  margin-bottom: 24px;
  line-height: 1.1;
  font-family: 'Lora', serif;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.hero-subtitle {
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.95);
  margin-bottom: 32px;
  line-height: 1.6;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.hero-button {
  display: inline-block;
  padding: 16px 32px;
  background: #4A90E2;
  color: white;
  font-weight: 700;
  font-size: 1rem;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(74, 144, 226, 0.4);
}

.hero-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(74, 144, 226, 0.5);
  background: #3a80d2;
}

/* Collections Section */
.collections-section {
  padding: 80px 24px;
  background: rgba(245, 239, 230, 0.3);
}

.section-title {
  font-size: 2.25rem;
  font-weight: 700;
  text-align: center;
  color: #2C3E50;
  margin-bottom: 48px;
  font-family: 'Lora', serif;
}

.collections-grid {
  max-width: 1280px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}

.collection-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.collection-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.collection-image {
  width: 100%;
  aspect-ratio: 4/5;
  background-size: cover;
  background-position: center;
}

.collection-info {
  padding: 24px;
  text-align: center;
}

.collection-info h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2C3E50;
  margin-bottom: 8px;
  font-family: 'Lora', serif;
}

.collection-info p {
  color: #7F8C8D;
  font-size: 0.95rem;
  line-height: 1.5;
}

/* Map Preview Section */
.map-preview-section {
  padding: 80px 24px;
  background: white;
}

.map-container {
  max-width: 1000px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
}

.map-placeholder {
  width: 100%;
  height: 400px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(245, 239, 230, 0.5);
}

.map-placeholder img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.map-button {
  padding: 14px 28px;
  background: #4A90E2;
  color: white;
  font-weight: 700;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.map-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(74, 144, 226, 0.4);
  background: #3a80d2;
}

/* About Section */
.about-section {
  padding: 80px 24px;
  background: rgba(245, 239, 230, 0.3);
}

.about-grid {
  max-width: 1000px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 64px;
  align-items: center;
}

.about-content h2 {
  font-size: 2.25rem;
  font-weight: 700;
  color: #2C3E50;
  margin-bottom: 20px;
  font-family: 'Lora', serif;
}

.about-content p {
  color: #7F8C8D;
  font-size: 1.05rem;
  line-height: 1.7;
}

.about-image-container {
  display: flex;
  justify-content: center;
}

.about-image {
  width: 100%;
  max-width: 450px;
  aspect-ratio: 1;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
}

/* Responsive */
@media (max-width: 1024px) {
  .collections-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
  
  .about-grid {
    grid-template-columns: 1fr;
    gap: 40px;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .collections-grid {
    grid-template-columns: 1fr;
  }
  
  .collections-section,
  .map-preview-section,
  .about-section {
    padding: 60px 16px;
  }
  
  .section-title {
    font-size: 1.875rem;
  }
  
  .about-content {
    text-align: center;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-button {
    padding: 14px 24px;
    font-size: 0.95rem;
  }
}
</style>
