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
  <div id="app">
    <RouterView />
    <FooterSection />
  </div>
</template>

<style>

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f8fafc;
  color: #1f2937;
  line-height: 1.6;
}

#app {
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

@media (max-width: 768px) {
  .container {
    padding: 0 16px;
  }
}

button {
  font-family: inherit;
}

input, select, textarea {
  font-family: inherit;
}

a {
  color: #3b82f6;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
