<script setup>

// Este componente recibe el valor actual del orden
defineProps({
  modelValue: {
    type: String,
    default: 'desc',
  },
});

// Define el evento 'update:modelValue' para que funcione con v-model
const emit = defineEmits(['update:modelValue']);

// Función que emite el evento cuando el usuario cambia la selección
const onChange = (event) => {
  emit('update:modelValue', event.target.value);
};
</script>

<template>
  <!-- 
    Componente reutilizable para ordenar (Req. Funcional 6)
    Ubicado en 'common' (comunes) porque se usará en Reseñas y Favoritos.
  -->
  <div class="flex justify-end mb-4">
    <select 
      :value="modelValue" 
      @change="onChange" 
      class="rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
    >
      <option value="desc">Ordenar por fecha (más reciente)</option>
      <option value="asc">Ordenar por fecha (más antigua)</option>
    </select>
  </div>
</template>
