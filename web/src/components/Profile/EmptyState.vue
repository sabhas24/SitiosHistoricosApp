<script setup>

// Este componente recibe el título y el mensaje que debe mostrar
// Asignamos a 'props' para la sintaxis correcta
const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  message: {
    type: String,
    required: true,
  }
});
</script>

<template>
  <div class="text-center bg-white p-10 rounded-lg shadow-sm">
    <div class="mx-auto h-12 w-12 text-gray-400">
      
      <!-- 
        SLOT DE ICONO:
        El componente "padre" (ej. ListadoReseñas) puede
        insertar su propio icono SVG aquí.
      -->
      <slot name="icon">
        <!-- Icono genérico por defecto si no se provee uno -->
        <div class="text-2xl">📄</div>
      </slot>
    </div>
    <!-- Usamos props.title y props.message -->
    <h3 class="mt-2 text-lg font-medium text-gray-900">{{ props.title }}</h3>
    <p class="mt-1 text-sm text-gray-500">{{ props.message }}</p>
  </div>
</template> 
