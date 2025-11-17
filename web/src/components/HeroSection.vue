<template>
  <section class="relative min-h-[60vh] flex items-center justify-center py-20 px-4 bg-gradient-to-br from-blue-50 via-purple-50 to-blue-50">
    <div class="max-w-3xl text-center">
      <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 mb-3">{{ projectTitle }}</h1>
      <p v-if="subtitle" class="text-lg sm:text-xl text-gray-600 mb-6">{{ subtitle }}</p>

      <form @submit.prevent="handleSearch" class="mx-auto max-w-xl">
        <div class="relative">
          <input v-model="searchQuery" type="text" placeholder="Buscar sitios históricos..." class="w-full px-5 py-3 rounded-full border border-gray-200 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-300"/>
          <button type="submit" class="absolute right-1 top-1/2 -translate-y-1/2 bg-blue-600 text-white rounded-full p-2 hover:bg-blue-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          </button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

defineProps({
  projectTitle: { type: String, default: 'PatrimonioBA' },
  subtitle: { type: String, default: 'Descubre y explora el patrimonio histórico de Buenos Aires' },
})

const router = useRouter()
const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value.trim()) router.push({ path: '/map', query: { search: searchQuery.value.trim() } })
}

onMounted(() => {})
</script>

<!-- Styling handled by Tailwind utilities -->
<template>
  <section class="relative min-h-[60vh] flex items-center justify-center py-20 px-4 bg-gradient-to-br from-blue-50 via-purple-50 to-blue-50">
    <div class="max-w-3xl text-center">
      <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 mb-3">{{ projectTitle }}</h1>
      <p v-if="subtitle" class="text-lg sm:text-xl text-gray-600 mb-6">{{ subtitle }}</p>

      <form @submit.prevent="handleSearch" class="mx-auto max-w-xl">
        <div class="relative">
          <input v-model="searchQuery" type="text" placeholder="Buscar sitios históricos..." class="w-full px-5 py-3 rounded-full border border-gray-200 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-300"/>
          <button type="submit" class="absolute right-1 top-1/2 -translate-y-1/2 bg-blue-600 text-white rounded-full p-2 hover:bg-blue-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          </button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { minioImg } from '../utils/minioImages.js'

defineProps({
  projectTitle: { type: String, default: 'PatrimonioBA' },
  subtitle: { type: String, default: 'Descubre y explora el patrimonio histórico de Buenos Aires' },
  backgroundImage: { type: String, default: null }
})

const router = useRouter()
const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value.trim()) router.push({ path: '/map', query: { search: searchQuery.value.trim() } })
}

onMounted(() => {})
</script>

<!-- Styling handled by Tailwind utilities -->
<template>
  <section class="relative min-h-[60vh] flex items-center justify-center py-20 px-4 bg-gradient-to-br from-blue-50 via-purple-50 to-blue-50">
    <div class="max-w-3xl text-center">
      <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 mb-3">{{ projectTitle }}</h1>
      <p v-if="subtitle" class="text-lg sm:text-xl text-gray-600 mb-6">{{ subtitle }}</p>

      <form @submit.prevent="handleSearch" class="mx-auto max-w-xl">
        <div class="relative">
          <input v-model="searchQuery" type="text" placeholder="Buscar sitios históricos..." class="w-full px-5 py-3 rounded-full border border-gray-200 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-300"/>
          <button type="submit" class="absolute right-1 top-1/2 -translate-y-1/2 bg-blue-600 text-white rounded-full p-2 hover:bg-blue-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          </button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { minioImg } from '../utils/minioImages.js'

defineProps({
  projectTitle: { type: String, default: 'PatrimonioBA' },
  subtitle: { type: String, default: 'Descubre y explora el patrimonio histórico de Buenos Aires' },
  backgroundImage: { type: String, default: null }
})

const router = useRouter()
const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value.trim()) router.push({ path: '/map', query: { search: searchQuery.value.trim() } })
}

onMounted(() => {})
</script>

<!-- Styling handled by Tailwind utilities -->
<template>
  <section class="relative min-h-[60vh] flex items-center justify-center py-20 px-4 bg-gradient-to-br from-blue-50 via-purple-50 to-blue-50">
    <div class="max-w-3xl text-center">
      <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 mb-3">{{ projectTitle }}</h1>
      <p v-if="subtitle" class="text-lg sm:text-xl text-gray-600 mb-6">{{ subtitle }}</p>

      <form @submit.prevent="handleSearch" class="mx-auto max-w-xl">
        <div class="relative">
          <input v-model="searchQuery" type="text" placeholder="Buscar sitios históricos..." class="w-full px-5 py-3 rounded-full border border-gray-200 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-300"/>
          <button type="submit" class="absolute right-1 top-1/2 -translate-y-1/2 bg-blue-600 text-white rounded-full p-2 hover:bg-blue-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          </button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { minioImg } from '../utils/minioImages.js'

defineProps({
  projectTitle: { type: String, default: 'PatrimonioBA' },
  subtitle: { type: String, default: 'Descubre y explora el patrimonio histórico de Buenos Aires' },
  backgroundImage: { type: String, default: null }
})

const router = useRouter()
const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value.trim()) router.push({ path: '/map', query: { search: searchQuery.value.trim() } })
}

onMounted(() => {})
</script>

<!-- Styling handled by Tailwind utilities -->
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
    </script>

    <!-- Styles moved to Tailwind / main.css utilities -->


.hero-overlay {

  position: absolute;
