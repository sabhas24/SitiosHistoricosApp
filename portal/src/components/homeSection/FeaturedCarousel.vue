<template>
  <section class="featured-carousel">
    <div class="container">
      <div class="header">
        <h2>{{ title }}</h2>
        <div class="actions">
          <button class="nav" @click="prev">‹</button>
          <button class="nav" @click="next">›</button>
        </div>
      </div>
      <div class="track" ref="track">
        <div class="item" v-for="site in sites" :key="site.id">
          <SiteCard :site="site" />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import SiteCard from './SiteCard.vue'

const props = defineProps({ title: { type: String, default: 'Destacados' } })
const sites = ref([])
const track = ref(null)
const router = useRouter()

const next = () => {
  track.value?.scrollBy({ left: 320, behavior: 'smooth' })
}

const prev = () => {
  track.value?.scrollBy({ left: -320, behavior: 'smooth' })
}

const loadMock = async () => {
  await new Promise(r => setTimeout(r, 400))
  sites.value = Array.from({ length: 8 }).map((_, i) => ({
    id: i + 1,
    name: i % 2 === 0 ? 'OBELISCO' : 'EJEMPLO',
    city: 'Buenos Aires',
    province: 'CABA',
    rating: 4.2 + (i % 3) * 0.2,
    image: null,
  }))
}

onMounted(loadMock)
</script>

<style scoped>
.featured-carousel {
  padding: 24px 0 12px;
  background-color: rgba(0, 0, 0, 0.15);
}
.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.header h2 { font-size: 1.5rem; font-weight: 700; color: var(--text-primary); }
.actions { display: flex; gap: 8px; }
.nav { width: 36px; height: 36px; border-radius: 999px; border: 1px solid var(--border-color); background: white; cursor: pointer; }
.nav:hover { background: var(--background-muted); }
.track { display: grid; grid-auto-flow: column; grid-auto-columns: 280px; gap: 16px; overflow-x: auto; padding-bottom: 8px; scroll-snap-type: x mandatory; }
.item { scroll-snap-align: start; }
@media (max-width: 640px) { .track { grid-auto-columns: 240px; } }
</style>