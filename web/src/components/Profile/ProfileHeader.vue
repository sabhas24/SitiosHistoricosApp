<script setup>
const props = defineProps({
 usuario: {
    type: Object,
    required: true
 }
})

const userInitial = props.usuario.name ? props.usuario.name.charAt(0).toUpperCase() : 'U'

</script>
<template>
  <header class="bg-white p-6 rounded-xl shadow-sm flex flex-col md:flex-row items-center space-y-4 md:space-y-0 md:space-x-6">
    
    <div class="w-24 h-24 rounded-full border-4 border-white shadow-md" style="background: linear-gradient(to bottom right, #3b82f6, #9333ea);" >
      <div class="flex items-center justify-center text-white text-2xl font-bold h-full">
        {{ userInitial }}
      </div>
    </div>
    
    <div class="text-center md:text-left">
      <h1 class="text-3xl font-bold text-gray-900">{{ props.usuario.name }}</h1>
      <p class="text-lg text-gray-600">{{ props.usuario.email }}</p>
    </div>
  </header>
</template>
