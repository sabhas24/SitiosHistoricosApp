<template>
  <div class="login-success-view">
    <div class="card">
      <svg width="64" height="64" fill="none" viewBox="0 0 24 24"><circle cx="12" cy="12" r="12" fill="#4ade80"/><path d="M7 13l3 3 7-7" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <h2>¡Inicio de sesión exitoso!</h2>
      <p>Serás redirigido en unos segundos...</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onMounted(() => {
  const redirectPath = localStorage.getItem('redirectAfterLogin') || '/'
  localStorage.removeItem('redirectAfterLogin')
  setTimeout(() => {
    router.push(redirectPath)
  }, 2000)
})
</script>

<!-- Styles moved to Tailwind / main.css utilities -->


