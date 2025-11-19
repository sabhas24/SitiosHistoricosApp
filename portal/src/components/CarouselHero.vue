<template>
  <section class="carousel-hero">
    <div class="carousel">
      <div class="slides" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
        <div v-for="(slide, i) in slides" :key="i" class="slide">
          <img :src="slide.image" :alt="slide.title" />
          <div class="overlay"></div>
          <div class="content">
            <h1 class="title">{{ slide.title }}</h1>
            <p class="subtitle">{{ slide.subtitle }}</p>
            <div class="actions">
              <router-link class="primary-btn" :to="slide.ctaHref">{{ slide.ctaText }}</router-link>
              <a v-if="slide.secondaryHref" class="secondary-btn" :href="slide.secondaryHref">{{ slide.secondaryText }}</a>
            </div>
          </div>
        </div>
      </div>
      <button class="nav prev" @click="prev">‹</button>
      <button class="nav next" @click="next">›</button>
      <div class="dots">
        <button 
          v-for="(s, i) in slides" 
          :key="i" 
          class="dot" 
          :class="{ active: i === currentIndex }"
          @click="go(i)"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

// Assuming minioImg can construct URLs for assets in the public folder
import { minioImg } from '../utils/minioImages.js'

const slides = ref([
  {
    title: 'PatrimonioBA',
    subtitle: 'Descubre y explora el patrimonio histórico de Buenos Aires',
    image: 'https://turismo.buenosaires.gob.ar/sites/turismo/files/field/image/congreso_nacional_fuente_1200.jpg',
    ctaText: 'Explorar mapa',
    ctaHref: '/map'
  },
  {
    title: 'Sitios emblemáticos',
    subtitle: 'Recorré los lugares más visitados y mejor puntuados',
    image: 'https://turismo.buenosaires.gob.ar/sites/turismo/files/field/image/congreso_nacional_fuente_1200.jpg',
    ctaText: 'Ver destacados',
    ctaHref: '/map?sort=visits'
  },
  {
    title: 'Tu guía cultural',
    subtitle: 'Museos, arquitectura, monumentos y mucho más',
    image: 'https://turismo.buenosaires.gob.ar/sites/turismo/files/field/image/congreso_nacional_fuente_1200.jpg',
    ctaText: 'Buscar categorías',
    ctaHref: '/map?category=all'
  }
])

const currentIndex = ref(0)
let timer = null

const next = () => {
  currentIndex.value = (currentIndex.value + 1) % slides.value.length
}

const prev = () => {
  currentIndex.value = (currentIndex.value - 1 + slides.value.length) % slides.value.length
}

const go = (i) => {
  currentIndex.value = i
}

const startAutoPlay = () => {
  timer = setInterval(next, 5000)
}

const stopAutoPlay = () => {
  if (timer) clearInterval(timer)
}

onMounted(() => {
  startAutoPlay()
})

onBeforeUnmount(() => {
  stopAutoPlay()
})
</script>

<style scoped>
.carousel-hero {
  position: relative;
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.carousel-hero::before,
.carousel-hero::after {
  content: "";
  position: absolute;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  filter: blur(80px);
  z-index: -3;
  animation: float 12s ease-in-out infinite;
}

.carousel-hero::before {
  background: radial-gradient(circle at 30% 30%, #3b82f6 0%, transparent 60%);
  top: -120px;
  left: -120px;
}

.carousel-hero::after {
  background: radial-gradient(circle at 70% 70%, #8b5cf6 0%, transparent 60%);
  bottom: -120px;
  right: -120px;
  animation-delay: 3s;
}

.carousel {
  position: relative;
  width: 100%;
  height: 70vh;
  min-height: 500px;
  overflow: hidden;
}

.slides {
  display: flex;
  height: 100%;
  width: 100%;
  transition: transform 0.6s ease;
}

.slide {
  position: relative;
  min-width: 100%;
  width: 100%;
  height: 100%;
  flex-shrink: 0;
}

.slide img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.7) 0%, rgba(118, 75, 162, 0.7) 100%);
  z-index: 1;
}

.content {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 0 24px;
  color: white;
  z-index: 2;
  animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 16px;
  color: white;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  letter-spacing: -0.02em;
}

.subtitle {
  font-size: 1.35rem;
  color: rgba(255, 255, 255, 0.95);
  margin-bottom: 32px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  max-width: 600px;
}

.actions {
  display: flex;
  gap: 12px;
}

.primary-btn,
.secondary-btn {
  display: inline-block;
  padding: 14px 32px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.05rem;
  transition: all 0.3s ease;
}

.primary-btn {
  background: rgba(255, 255, 255, 0.95);
  color: #667eea;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.primary-btn:hover {
  background: white;
  transform: translateY(-2px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.25);
}

.secondary-btn {
  background: rgba(255,255,255,0.15);
  color: white;
  border: 2px solid rgba(255,255,255,0.3);
  backdrop-filter: blur(10px);
}

.secondary-btn:hover {
  background: rgba(255,255,255,0.25);
  border-color: rgba(255,255,255,0.5);
  transform: translateY(-2px);
}

.nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(10px);
  border: none;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  z-index: 3;
  color: #667eea;
  font-weight: bold;
}

.nav:hover {
  background: white;
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 6px 30px rgba(0, 0, 0, 0.25);
}

.prev { left: 24px; }
.next { right: 24px; }

.dots {
  position: absolute;
  bottom: 30px;
  left: 0;
  right: 0;
  display: flex;
  gap: 10px;
  justify-content: center;
  z-index: 3;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255,255,255,0.4);
  border: 2px solid rgba(255,255,255,0.6);
  cursor: pointer;
  transition: all 0.3s ease;
}

.dot:hover {
  background: rgba(255,255,255,0.6);
  transform: scale(1.1);
}

.dot.active { 
  background: white;
  border-color: white;
  transform: scale(1.2);
}

@media (max-width: 768px) {
  .carousel {
    height: 60vh;
    min-height: 450px;
  }
  
  .title {
    font-size: 2.5rem;
  }
  
  .subtitle {
    font-size: 1.1rem;
  }
  
  .nav {
    width: 44px;
    height: 44px;
    font-size: 24px;
  }
  
  .prev { left: 16px; }
  .next { right: 16px; }
  
  .primary-btn,
  .secondary-btn {
    padding: 12px 24px;
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .carousel {
    height: 55vh;
    min-height: 400px;
  }
  
  .title {
    font-size: 2rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
  
  .actions {
    flex-direction: column;
    gap: 10px;
  }
}

@keyframes float {
  0% { transform: translate3d(0,0,0); }
  50% { transform: translate3d(20px,-10px,0); }
  100% { transform: translate3d(0,0,0); }
}
</style>