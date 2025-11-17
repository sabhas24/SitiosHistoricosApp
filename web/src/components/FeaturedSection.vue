<template>
  <section class="py-8">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-gray-900">{{ title }}</h2>
      <button v-if="showViewAll" @click="handleViewAll" class="text-sm text-blue-600 hover:underline">Ver todos →</button>
    </div>

    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="n in 6" :key="n" class="h-56 bg-gray-100 rounded-lg animate-pulse"></div>
    </div>

    <div v-else-if="sites.length === 0" class="text-center text-gray-600 py-8">
      {{ emptyMessage }}
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <SiteCard v-for="site in sites" :key="site.id" :site="site" />
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import SiteCard from './Profile/SiteCard.vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  title: { type: String, required: true },
  endpoint: { type: String, required: true },
  emptyMessage: { type: String, default: 'No hay contenido disponible' },
  showViewAll: { type: Boolean, default: true }
})

const router = useRouter()
const sites = ref([])
const loading = ref(true)

const loadSites = async () => {
  loading.value = true
  // placeholder
  sites.value = [{ id: 1, name: 'Obelisco', city: 'BA', province: 'CABA', rating: 4.5, image: '' }]
  loading.value = false
}

const handleViewAll = () => router.push('/map')
onMounted(loadSites)
</script>

<!-- Styling handled via Tailwind utilities -->
<template>
  <section class="py-8">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-gray-900">{{ title }}</h2>
      <button v-if="showViewAll" @click="handleViewAll" class="text-sm text-blue-600 hover:underline">Ver todos →</button>
    </div>

    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="n in 6" :key="n" class="h-56 bg-gray-100 rounded-lg animate-pulse"></div>
    </div>

    <div v-else-if="sites.length === 0" class="text-center text-gray-600 py-8">
      {{ emptyMessage }}
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <SiteCard v-for="site in sites" :key="site.id" :site="site" />
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import SiteCard from './Profile/SiteCard.vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  title: { type: String, required: true },
  endpoint: { type: String, required: true },
  emptyMessage: { type: String, default: 'No hay contenido disponible' },
  showViewAll: { type: Boolean, default: true }
})

<!-- Styling handled via Tailwind utilities -->
  router.push(`/map${queryParams ? '?' + queryParams : ''}`)
}

const retry = () => {
  loadSites()
}

onMounted(() => {
  loadSites()
})
</script>

<!-- Styles moved to Tailwind utilities; no scoped CSS needed -->
.featured-section {
  margin-bottom: 48px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.view-all-btn {
  background: none;
  border: none;
</script>
<!-- Styles moved to Tailwind utilities; no scoped CSS needed -->
  cursor: pointer;
