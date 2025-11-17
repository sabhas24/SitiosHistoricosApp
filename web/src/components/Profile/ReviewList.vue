<script setup>
import { ref, onMounted, watch } from 'vue';

// Importar los componentes "hijos" que hemos creado
import SortSelector from './SortSelector.vue';
import EmptyState from './EmptyState.vue';
import Pagination from  './Pagination.vue';
import ReviewCard from './ReviewCard.vue';
import {profileService } from '@/services/profileService';  // Sin 's' al final
// --- Props ---
// Este componente "inteligente" recibe el ID del usuario para saber
// qué reseñas debe buscar en la API.
// No necesita props, ya que usa el usuario autenticado

// --- Estado Reactivo ---
// Aquí es donde vive el estado de esta sección
const reviews = ref([]); // La lista de reseñas
const isLoading = ref(true); // Para mostrar un spinner o mensaje
const currentPage = ref(1); // La página actual
const totalPages = ref(1); // El total de páginas (vendría de la API)
const currentSort = ref('desc'); // El orden actual (conectado a SortSelector)



// --- Métodos ---
/**
 * Simula una llamada a la API para buscar las reseñas del usuario.
 * (Req. Funcional 5: Paginación server-side)
 */
const fetchReviews = async () => {
  isLoading.value = true;
  // Endpoint no disponible, mostrar vacío
  reviews.value = [];
  totalPages.value = 1;
  isLoading.value = false;
};
  
  

// --- Hooks del Ciclo de Vida ---
// Carga las reseñas cuando el componente se monta por primera vez
onMounted(() => {
  fetchReviews();
});

// "Observa" los cambios en la página actual o el orden.
// Si cambian, vuelve a llamar a la API.
watch([currentPage, currentSort], () => {
  fetchReviews();
});

</script>

<template>
  <div>
    <!-- Estado de Carga -->
    <div v-if="isLoading" class="text-center text-gray-500 py-10">
      Cargando reseñas...
    </div>

    <!-- Estado Vacío (Req. Funcional 7) -->
    <EmptyState
      v-else-if="reviews.length === 0"
      title="Funcionalidad en desarrollo"
      message="Las reseñas estarán disponibles próximamente."
    >
      <template #icon>
        <div class="text-2xl">🚧</div>
      </template>
    </EmptyState>

    <!-- Estado con Contenido -->
    <div v-else>
      <!-- Componente Selector de Orden (Req. Funcional 6) -->
      <!-- v-model conecta 'currentSort' con el componente hijo -->
      <SortSelector v-model="currentSort" />

      <!-- Lista de Reseñas (Req. Funcional 3) -->
      <div class="space-y-4">
        <ReviewCard
          v-for="review in reviews"
          :key="review.id"
          :review="review"
        />
      </div>

      <!-- Componente Paginación (Req. Funcional 5) -->
      <Pagination
        :current-page="currentPage"
        :total-pages="totalPages"
        @page-changed="(newPage) => currentPage = newPage"
      />
    </div>
  </div>
</template>
