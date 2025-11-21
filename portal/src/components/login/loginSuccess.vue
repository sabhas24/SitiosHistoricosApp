<template>
  <div class="login-success">
    <h2>¡Inicio de sesión exitoso!</h2>
    <p>Serás redirigido en unos segundos...</p>
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
  }, 3000) 
})
</script>

<style scoped>
.login-success {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}
</style>