<script setup>
import { RouterView } from 'vue-router'
import { onMounted }  from 'vue';
import { useAuthStore } from './stores/auth';

const authStore = useAuthStore();

onMounted(() => {
  authStore.checkSession();
});

</script>

<template>
  <div id="app" class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-blue-100 flex flex-col">
    <div class="w-full sticky top-0 z-50">
      <NavigationBar />
    </div>
    <main class="flex-1 w-full max-w-5xl mx-auto px-4 py-8">
      <RouterView />
    </main>
    <footer class="w-full text-center py-6 text-gray-400 text-sm bg-transparent">
      © 2025 PatrimonioBA. Todos los derechos reservados.
    </footer>
  </div>
</template>
