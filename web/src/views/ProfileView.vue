<script setup>
import { computed, ref } from 'vue';
import { useAuthStore } from '../stores/auth';

// --- 1. Importar todos los componentes "hijos" ---
import ProfileHeader from '../components/Profile/ProfileHeader.vue';
import ReviewList from '../components/Profile/ReviewList.vue';
import FavoriteList from '../components/Profile/FavoriteList.vue';

// --- 2. Estado (State) ---
const authStore = useAuthStore();
// (Simulación) Objeto del usuario que vendría de la sesión (Fase 1)
const currentUser = computed(() => ({
  id: authStore.userId, 
  name: authStore.userName,
  email: authStore.userEmail
}));

// El estado que controla qué pestaña se está mostrando
const currentTab = ref('reviews'); // 'reviews' o 'favorites'

// --- 3. Métodos ---

// Esta función se activa cuando se hace clic en una pestaña.
const changeTab = (newTab) => {
  currentTab.value = newTab;
};

</script>

<template>
  <!-- 
    Este es el componente "Padre" o "Vista" (Sección 1 del plan)
    Su trabajo es ensamblar todos los componentes que creamos.
  -->
  <main class="max-w-4xl mx-auto p-4 md:p-6">
    
    <!-- Botón Volver (opcional) -->
    <div class="mb-4">
      <a href="#" class="text-blue-600 hover:underline">&larr; Volver</a>
    </div>

    <!-- Componente de Cabecera -->
    <!-- :usuario="currentUser" le pasa el objeto 'currentUser' al "prop" 'usuario' -->
    <ProfileHeader :usuario="currentUser" />

    <div class="mt-6">
      
      <!-- Pestañas -->
      <div class="flex border-b mb-4">
        <button @click="changeTab('reviews')" :class="currentTab === 'reviews' ? 'border-b-2 border-blue-500' : ''" class="px-4 py-2">Mis reseñas</button>
        <button @click="changeTab('favorites')" :class="currentTab === 'favorites' ? 'border-b-2 border-blue-500' : ''" class="px-4 py-2">Mis sitios favoritos</button>
      </div>
      
      <!-- Contenido dinámico de la pestaña -->
      <div class="mt-5">
        
        <!-- Componente Listado Reseñas -->
        <ReviewList v-if="currentTab === 'reviews'" />
        
        <!-- Componente Listado Favoritos -->
        <FavoriteList v-if="currentTab === 'favorites'" />

      </div>
    </div>
  </main>
</template>
