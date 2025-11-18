<template>
  <section class="interests-section">
    <div class="container">
      <div class="header">
        <h2>Explorá por intereses</h2>
        <p>Descubrí categorías destacadas del patrimonio</p>
      </div>

      <div class="grid">
        <div v-for="item in items" :key="item.title" class="card">
          <div class="icon">{{ item.icon }}</div>
          <h3 class="title">{{ item.title }}</h3>
          <p class="desc">{{ item.desc }}</p>
          <router-link class="link" :to="item.href">Ver más →</router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const items = [
  { icon: '🏛️', title: 'Museos', desc: 'Colecciones y espacios culturales', href: '/map?category=museos' },
  { icon: '🏗️', title: 'Arquitectura', desc: 'Edificios y obras emblemáticas', href: '/map?category=arquitectura' },
  { icon: '🗿', title: 'Monumentos', desc: 'Hitos y esculturas históricas', href: '/map?category=monumentos' },
  { icon: '🧭', title: 'Sitios arqueológicos', desc: 'Vestigios y hallazgos', href: '/map?category=arqueologicos' },
]
</script>

<style scoped>
.interests-section { padding: 48px 0; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
.header { text-align: center; margin-bottom: 28px; }
.header h2 { font-size: 1.75rem; font-weight: 700; color: var(--text-primary); }
.header p { color: var(--text-secondary); }

.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.card {
  background: linear-gradient(180deg, #ffffff, #f8fafc);
  border-radius: var(--radius-lg);
  padding: 20px;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: 1px solid var(--border-color);
}

.card:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); }
.icon { font-size: 2rem; }
.title { font-size: 1.1rem; margin: 8px 0; color: var(--text-primary); }
.desc { color: var(--text-secondary); font-size: 0.95rem; }
.link { display: inline-block; margin-top: 8px; color: var(--primary-color); text-decoration: none; font-weight: 600; }
.link:hover { text-decoration: underline; }

@media (max-width: 1024px) { .grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px) { .grid { grid-template-columns: 1fr; } }
</style>