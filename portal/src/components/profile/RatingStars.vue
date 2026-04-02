<template>
  <div class="rating-stars">
    <span
      v-for="star in 5"
      :key="star"
      class="star"
      :class="{ filled: star <= rating }"
    >
      ★
    </span>
    <span v-if="showValue" class="rating-value">({{ rating }}/5)</span>
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
.rating-stars {
  display: inline-flex;
  align-items: center;
  gap: 2px;
}

.star {
  font-size: 16px;
  color: #d1d5db;
  transition: color 0.2s;
}

.star.filled {
  color: #fbbf24;
}

.rating-value {
  margin-left: 8px;
  font-size: 14px;
  color: #6b7280;
}
</style>
