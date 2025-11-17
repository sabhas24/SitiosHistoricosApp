<script setup>
import { ref, onMounted, watch } from 'vue';

// Importar los componentes "hijos" que hemos creado
import SortSelector from './SortSelector.vue';
import EmptyState from './EmptyState.vue';
import Pagination from './Pagination.vue';
import SiteCard from './SiteCard.vue';
import { profileService } from '@/services/profileService';

// --- Props ---
// No necesita props, ya que usa el usuario autenticado

// --- Estado Reactivo ---
const favorites = ref([]); // La lista de favoritos
const isLoading = ref(true); // Para mostrar un spinner
const currentPage = ref(1); // La página actual
const totalPages = ref(1); // El total de páginas
const currentSort = ref('desc'); // El orden actual 

// --- Métodos ---
/**
 * Llama a la API para buscar los favoritos del usuario.
 */
const fetchFavorites = async () => {
  isLoading.value = true;
  try {
    const data = await profileService.getFavorites(currentPage.value, 25, currentSort.value);
    favorites.value = data.items;
    totalPages.value = data.totalPages;
  } catch (error) {
    console.error('Error al cargar los favoritos:', error);
    favorites.value = [];
    totalPages.value = 1;
  } finally {
    isLoading.value = false;
  }
};

// --- Hooks del Ciclo de Vida ---
onMounted(() => {
  fetchFavorites();
});

// "Observa" los cambios en la página actual o el orden.
watch([currentPage, currentSort], () => {
  fetchFavorites();
});

</script>

<template>
  <div>
    <!-- Estado de Carga -->
    <div v-if="isLoading" class="text-center text-gray-500 py-10">
      Cargando sitios favoritos...
    </div>

    <!-- Estado Vacío (Req. Funcional 7) -->
    <EmptyState
      v-else-if="favorites.length === 0"
      title="Aún no marcaste ningún sitio como favorito"
      message="Usa el ícono de corazón en un sitio para guardarlo aquí."
    >
      <!-- Slot de Icono: Pasamos un icono de corazón -->
      <template #icon>
        <div class="text-2xl">❤️</div>
      </template>
    </EmptyState>

    <!-- Estado con Contenido -->
    <div v-else>
      <!-- Componente Selector de Orden -->
      <SortSelector v-model="currentSort" />

      <!-- Lista de Favoritos (Req. Funcional 4) -->
      <!-- Nota: Usamos un 'grid' como en la maqueta original -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <SiteCard
          v-for="site in favorites"
          :key="site.id"
          :site="site"
        />
      </div>

      <!-- Componente Paginación -->
      <Pagination
        :current-page="currentPage"
        :total-pages="totalPages"
        @page-changed="(newPage) => currentPage = newPage"
      />
    </div>
  </div>
</template>
