<script setup>
import { RouterView } from 'vue-router'
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useConfigStore } from '@/stores/config'
import FooterSection from './components/FooterSection.vue'

const authStore = useAuthStore()
const configStore = useConfigStore()

onMounted(async () => {
  await authStore.checkSession()
  await configStore.fetchConfig()
})
</script>

<template>
  <div id="app" class="app-container">
    <RouterView />
    <FooterSection />
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
</style>
