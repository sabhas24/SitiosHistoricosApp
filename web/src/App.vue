<script setup>
import { RouterView } from 'vue-router'
import { onMounted }  from 'vue';
import { useAuthStore } from './stores/auth';
import FooterSection from './components/FooterSection.vue'

const authStore = useAuthStore();

onMounted(() => {
  authStore.checkSession();
});
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
