<script setup>
import { RouterView } from 'vue-router'
import { onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useConfigStore } from '@/stores/config'
import MaintenanceView from '@/views/MaintenanceView.vue'

const authStore = useAuthStore()
const configStore = useConfigStore()

onMounted(async () => {
  await authStore.checkSession()
  await configStore.fetchConfig()
})
</script>

<template>
  <MaintenanceView v-if="configStore.maintenanceMode" />
  <div v-else class="app-container">
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
