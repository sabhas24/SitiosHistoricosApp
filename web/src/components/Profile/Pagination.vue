<script setup>

// --- Props ---
// Recibe la página actual y el total de páginas
// para saber qué mostrar y qué deshabilitar.
const props = defineProps({
  currentPage: {
    type: Number,
    required: true,
    default: 1,
  },
  totalPages: {
    type: Number,
    required: true,
    default: 1,
  },
});

// --- Emits ---
// Define el evento que se enviará al padre
const emit = defineEmits(['page-changed']);

// --- Métodos ---
// Emite el evento con la nueva página solicitada
const goToPage = (page) => {
  // Validaciones para no ir más allá de los límites
  if (page < 1 || page > props.totalPages) {
    return;
  }
  emit('page-changed', page);
};
</script>

<template>
  <nav 
    v-if="totalPages > 1" 
    class="flex items-center justify-between border-t border-gray-200 px-4 py-6 mt-6"
  >
    <!-- Botón ANTERIOR -->
    <button 
      @click="goToPage(currentPage - 1)" 
      :disabled="currentPage <= 1"
      class="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      Anterior
    </button>
    
    <!-- Info de página actual -->
    <span class="text-sm text-gray-700 mx-4">
      Página {{ currentPage }} de {{ totalPages }}
    </span>
    
    <!-- Botón SIGUIENTE -->
    <button 
      @click="goToPage(currentPage + 1)" 
      :disabled="currentPage >= totalPages"
      class="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      Siguiente
    </button>
  </nav>
</template>
