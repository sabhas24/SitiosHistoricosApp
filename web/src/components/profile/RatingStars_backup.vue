<template>
  <div class="rating-container">
    <div class="stars">
      <span v-for="i in 5" :key="i" :class="['star', { filled: i <= rating }]">★</span>
    </div>
    <span v-if="showValue" class="rating-value">{{ rating }}/5</span>
  </div>
</template>

<script setup>
defineProps({
  rating: {
    type: Number,
    required: true,
    validator: (value) => value >= 1 && value <= 5
  },
  showValue: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.rating-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stars {
  display: flex;
  gap: 2px;
}

.star {
  font-size: 18px;
  color: #d1d5db;
  cursor: default;
}

.star.filled {
  color: #D4AF37;
}

.rating-value {
  font-size: 14px;
  color: #6b7280;
  font-weight: 600;
}
</style>
