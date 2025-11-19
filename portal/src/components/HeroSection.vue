<template>
  <section class="hero-section">
    <div class="hero-content">
      <h1 class="hero-title">
        Descubrí la historia <br>
        <span class="italic-text">de Argentina</span>
      </h1>
      
      <div class="search-container">
        <div class="search-box">
          <input 
            type="text" 
            v-model="searchQuery"
            @keyup.enter="handleSearch"
            placeholder="Buscar sitios, museos, plazas..."
            class="search-input"
            aria-label="Buscar sitios"
          >
          <button 
            @click="handleSearch"
            class="search-button"
            aria-label="Realizar búsqueda"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
          </button>
        </div>
      </div>
    </div>
    
    <div class="hero-background">
      <div class="hero-overlay"></div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ 
      name: 'sitios-list', 
      query: { name: searchQuery.value.trim() } 
    })
  }
}
</script>

<style scoped>
.hero-section {
  position: relative;
  height: 60vh; /* Reduced height as requested */
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 20px;
  margin-top: -80px; /* Pull behind nav */
  padding-top: 80px;
  overflow: hidden;
  background-image: url('https://turismo.buenosaires.gob.ar/sites/turismo/files/field/image/congreso_nacional_fuente_1200.jpg');
  background-size: cover;
  background-position: center;
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 800px;
  width: 100%;
}

.hero-title {
  font-family: var(--font-heading);
  font-size: 4rem;
  line-height: 1.2;
  color: white;
  margin-bottom: 3rem;
  font-weight: 400;
  letter-spacing: -0.02em;
}

.italic-text {
  font-style: italic;
  font-weight: 300;
  color: rgba(255, 255, 255, 0.9);
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1;
}

.search-container {
  max-width: 500px;
  margin: 0 auto;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
  background: white;
  border: 2px solid black;
  border-radius: var(--radius-full);
  padding: 8px;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-sm);
}

.search-box:focus-within {
  border-color: var(--text-primary);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 12px 20px;
  font-size: 1rem;
  color: var(--text-primary);
  outline: none;
}

.search-input::placeholder {
  color: var(--text-muted);
}

.search-button {
  background: #3b82f6; /* Azul para el círculo */
  color: white;
  border: none;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.2s ease, background-color 0.2s ease;
}

.search-button:hover {
  background: var(--primary-dark);
  transform: scale(1.05);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-section {
    height: 50vh;
  }
}
</style>
