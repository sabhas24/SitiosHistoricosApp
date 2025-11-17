<script setup>

// Este componente recibe un solo objeto 'review' como prop.
const props = defineProps({
  review: {
    type: Object,
    required: true
    /*
    default: () => ({
      siteName: "Cargando...",
      siteUrl: "#",
      rating: 0,
      date: "...",
      excerpt: "Cargando contenido de la reseña..."
    })
    */
  }
});

// Calcula las estrellas (ej. ★★★★☆) basado en el rating
// Añadimos un fallback (|| 0) por si el rating no está definido
const stars = '★'.repeat(props.review?.rating || 0) + '☆'.repeat(5 - (props.review?.rating || 0));
</script>

<template>
  <!-- 
    Tarjeta individual para una reseña (Req. Funcional 3)
    Extraído de la maqueta 'perfil_usuario.html'
  -->
  <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
    <div class="flex justify-between items-center mb-2">
      <!-- El nombre del sitio es un enlace -->
      <a 
        :href="props.review.siteUrl" 
        class="text-lg font-semibold text-blue-600 hover:underline"
      >
        {{ props.review.siteName }}
      </a>
      <!-- La fecha de la reseña -->
      <span class="text-sm text-gray-500">{{ props.review.date }}</span>
    </div>
    
    <!-- Las estrellas (1-5) -->
    <div class="text-yellow-500 text-lg mb-2">{{ stars }}</div>
    
    <!-- El extracto de la reseña -->
    <p class="text-gray-700 italic">"{{ props.review.excerpt }}"</p>
  </div>
</template>
