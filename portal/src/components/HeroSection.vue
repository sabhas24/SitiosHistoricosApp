<template>
  <section class="hero-section">
    <div class="hero-content">
      <h1 class="hero-title">{{ projectTitle }}</h1>
      <p v-if="subtitle" class="hero-subtitle">{{ subtitle }}</p>
      
      <div class="search-container">
        <form @submit.prevent="handleSearch" class="search-form">
          <div class="search-input-group">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Buscar sitios históricos..."
              class="search-input"
              ref="searchInput"
            />
            <button type="submit" class="search-button">
              <svg xmlns="http://www.w3.org/2000/svg" class="search-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </div>
        </form>
      </div>
    </div>
    
    <div v-if="backgroundImage" class="hero-background">
      <img :src="minioImg(backgroundImage)" :alt="projectTitle" loading="lazy" />
      <div class="hero-overlay"></div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { minioImg } from '../utils/minioImages.js'

defineProps({
  projectTitle: {
    type: String,
    default: 'PatrimonioBA'
  },
  subtitle: {
    type: String,
    default: 'Descubre y explora el patrimonio histórico de Buenos Aires'
  },
  backgroundImage: {
    type: String,
    default: null
  }
})

const router = useRouter()
const searchInput = ref(null)
const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/map',
      query: { search: searchQuery.value.trim() }
    })
  }
}

onMounted(() => {
  if (window.innerWidth > 768) {
    setTimeout(() => {
      searchInput.value?.focus()
    }, 500)
  }
})
</script>

<style scoped>
.hero-section {
  position: relative;
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 80px 20px 60px;
  overflow: hidden;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -2;
}

.hero-background img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: -1;
}

.hero-content {
  text-align: center;
  max-width: 600px;
  z-index: 1;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 16px;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #6b7280;
  margin-bottom: 32px;
  line-height: 1.5;
}

.hero-section:has(.hero-background) .hero-title {
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.hero-section:has(.hero-background) .hero-subtitle {
  color: rgba(255, 255, 255, 0.9);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.search-container {
  width: 100%;
}

.search-form {
  margin-bottom: 24px;
}

.search-input-group {
  position: relative;
  max-width: 500px;
  margin: 0 auto;
}

.search-input {
  width: 100%;
  padding: 16px 60px 16px 20px;
  font-size: 1.1rem;
  border: 2px solid #e5e7eb;
  border-radius: 50px;
  background: white;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1), 0 4px 12px rgba(0, 0, 0, 0.15);
}

.search-button {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: #3b82f6;
  border: none;
  border-radius: 50%;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;
}

.search-button:hover {
  background: #2563eb;
}

.search-icon {
  width: 20px;
  height: 20px;
  color: white;
}

.quick-suggestions {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.suggestions-label {
  font-size: 0.9rem;
  color: #6b7280;
  font-weight: 500;
}

.suggestions-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.suggestion-chip {
  padding: 6px 16px;
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-radius: 20px;
  color: #3b82f6;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.suggestion-chip:hover {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.3);
}

/* Mobile responsive */
@media (max-width: 768px) {
  .hero-section {
    min-height: 50vh;
    padding: 60px 16px 40px;
  }
  
  .hero-title {
    font-size: 2.25rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .search-input {
    font-size: 1rem;
    padding: 14px 55px 14px 18px;
  }
  
  .search-button {
    width: 40px;
    height: 40px;
  }
  
  .search-icon {
    width: 18px;
    height: 18px;
  }
  
  .suggestions-list {
    gap: 6px;
  }
  
  .suggestion-chip {
    font-size: 0.85rem;
    padding: 5px 12px;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 1.875rem;
  }
  
  .quick-suggestions {
    padding: 0 10px;
  }
}
</style>
