<template>
  <section class="newsletter-section">
    <div class="container">
      <div class="card">
        <div class="content">
          <h2>Suscribite al newsletter</h2>
          <p>Recibí novedades, eventos y sitios destacados en tu correo</p>
        </div>
        <form class="form" @submit.prevent="submit">
          <input v-model="email" type="email" placeholder="Tu email" class="input" />
          <button class="btn" :disabled="loading">Suscribirme</button>
        </form>
        <p v-if="message" class="message">{{ message }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const loading = ref(false)
const message = ref('')

const submit = async () => {
  message.value = ''
  const value = email.value.trim()
  if (!value || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
    message.value = 'Ingresá un email válido'
    return
  }
  loading.value = true
  await new Promise(r => setTimeout(r, 800))
  loading.value = false
  email.value = ''
  message.value = '¡Gracias por suscribirte!'
}
</script>

<style scoped>
.newsletter-section { padding: 60px 0; }
.container { max-width: 1000px; margin: 0 auto; padding: 0 20px; }
.card { background: white; border-radius: var(--radius-xl); box-shadow: var(--shadow-lg); padding: 28px; }
.content h2 { font-size: 1.75rem; font-weight: 700; color: var(--text-primary); }
.content p { color: var(--text-secondary); margin-top: 6px; }
.form { display: grid; grid-template-columns: 1fr auto; gap: 12px; margin-top: 20px; }
.input { padding: 14px 16px; border: 2px solid var(--border-color); border-radius: var(--radius-md); font-size: 1rem; }
.input:focus { outline: none; border-color: var(--primary-color); }
.btn { padding: 14px 18px; background: var(--primary-color); color: white; border: none; border-radius: var(--radius-md); cursor: pointer; font-weight: 600; }
.btn:hover { background: var(--primary-dark); }
.btn:disabled { opacity: 0.7; cursor: not-allowed; }
.message { margin-top: 12px; color: var(--text-secondary); }

@media (max-width: 640px) { .form { grid-template-columns: 1fr; } }
</style>