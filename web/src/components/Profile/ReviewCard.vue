<script setup>

const props = defineProps({
  review: {
    type: Object,
    required: true
   
  }
});

// Calcula las estrellas (ej. ★★★★☆) basado en el rating
// Añadimos un fallback (|| 0) por si el rating no está definido
const stars = '★'.repeat(props.review?.rating || 0) + '☆'.repeat(5 - (props.review?.rating || 0));
</script>

<template>
  <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
    <div class="flex justify-between items-center mb-2">
      <!-- El nombre del sitio es un enlace -->
      <a
        :href="'/sites/' + props.review.site_id"
        class="text-lg font-semibold text-blue-600 hover:underline"
      >
        {{ props.review.site_name || 'Sitio ' + props.review.site_id }}
      </a>
      <!-- La fecha de la reseña -->
      <span class="text-sm text-gray-500">{{ props.review.inserted_at }}</span>
    </div>

    <!-- Las estrellas (1-5) -->
    <div class="text-yellow-500 text-lg mb-2">{{ stars }}</div>

    <!-- El extracto de la reseña -->
    <p class="text-gray-700 italic">"{{ props.review.comment }}"</p>
  </div>
</template>
