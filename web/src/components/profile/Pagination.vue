<template>
  <div class="pagination">
    <button
      class="btn-pagination"
      :disabled="currentPage === 1"
      @click="$emit('prev')"
    >
      ← Anterior
    </button>

    <span class="pagination-info">
      Página {{ currentPage }} de {{ totalPages }}
    </span>

    <button
      class="btn-pagination"
      :disabled="currentPage === totalPages"
      @click="$emit('next')"
    >
      Siguiente →
    </button>
  </div>
</template>

<script setup>
defineProps({
  currentPage: {
    type: Number,
    required: true
  },
  totalPages: {
    type: Number,
    required: true
  }
})

defineEmits(['prev', 'next'])
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 32px;
}

.btn-pagination {
  padding: 8px 16px;
  background: #8B7355;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-pagination:hover:not(:disabled) {
  background: #704a3a;
}

.btn-pagination:disabled {
  background: #d1d5db;
  cursor: not-allowed;
}

.pagination-info {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

@media (max-width: 768px) {
  .pagination {
    flex-direction: column;
    gap: 12px;
  }

  .btn-pagination {
    width: 100%;
    max-width: 120px;
  }
}
</style>
