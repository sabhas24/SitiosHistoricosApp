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

<style scoped>
.login-success-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #4ade80 0%, #38bdf8 100%);
}
.card {
  background: #fff;
  padding: 48px 32px;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.12);
  display: flex;
  flex-direction: column;
  align-items: center;
}
svg {
  margin-bottom: 16px;
}
h2 {
  color: #16a34a;
  margin-bottom: 12px;
  font-size: 2rem;
}
p {
  color: #334155;
  font-size: 1.1rem;
}
</style>
