<template>
  <div class="rating-input">
    <button
      v-for="n in 5"
      :key="n"
      :class="['star', { active: n <= internalValue }]"
      @click.prevent="update(n)"
      :title="`${n} stars`"
    >
      ★
    </button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
const props = defineProps({ modelValue: { type: Number, default: 0 } })
const emit = defineEmits(['update:modelValue'])

const internalValue = ref(props.modelValue || 0)

watch(() => props.modelValue, (v) => (internalValue.value = v || 0))

function update(n) {
  internalValue.value = n
  emit('update:modelValue', n)
}
</script>

<style scoped>
.rating-input { display: inline-flex; gap: 6px }
.star {
  background: transparent;
  border: none;
  font-size: 1.4rem;
  color: #ddd;
  cursor: pointer;
}
.star.active { color: #f59e0b }
.star:focus { outline: 2px solid rgba(99,102,241,0.25); border-radius: 4px }
</style>
