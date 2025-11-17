    <script setup>

// Este componente recibe un solo objeto 'site' como prop.
const props = defineProps({
  site: {
    type: Object,
    required: true
    /*
    default: () => ({
      name: "Cargando...",
      location: "...",
      imageUrl: "https://placehold.co/400x300/E0E7FF/4F46E5?text=...",
      siteUrl: "#"
    })
    */
  }
});
</script>

<template>
  <!-- 
    Tarjeta individual para un sitio favorito (Req. Funcional 4)
    Extraído de la maqueta 'perfil_usuario.html'
  -->
  <a 
    :href="props.site.siteUrl" 
    class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden block transition-shadow hover:shadow-md"
  >
    <!-- Imagen de portada del sitio -->
    <img 
      :src="props.site.imageUrl" 
      :alt="'Imagen de ' + props.site.name" 
      class="h-40 w-full object-cover"
    >
    
    <!-- Información del sitio -->
    <div class="p-4">
      <h3 class="font-semibold text-gray-900 truncate">{{ props.site.name }}</h3>
      <p class="text-sm text-gray-600">{{ props.site.location }}</p>
    </div>
  </a>
</template>
