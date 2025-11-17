<template>
  <div class="flex justify-end mb-4">
    <select v-model="sort" @change="$emit('update:modelValue', sort)" class="border border-gray-300 rounded px-3 py-1">
      <option value="desc">Más recientes primero</option>
      <option value="asc">Más antiguos primero</option>
    </select>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  modelValue: String
});

const emit = defineEmits(['update:modelValue']);

const sort = ref(props.modelValue || 'desc');
</script>
