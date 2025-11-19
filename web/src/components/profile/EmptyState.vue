<template>
  <div class="empty-state">
    <div class="empty-state-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <g v-if="type === 'reviews'">
          <path d="M11 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6M2 12h20M12 2v10M18 15l-3 3l-3-3" />
        </g>
        <g v-else-if="type === 'favorites'">
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
        </g>
        <g v-else>
          <circle cx="12" cy="12" r="10" />
          <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
          <path d="M12 17h.01" />
        </g>
      </svg>
    </div>
    <h3 class="empty-state-title">{{ title }}</h3>
    <p class="empty-state-message">{{ message }}</p>
    <button v-if="showButton" class="btn-explore" @click="$emit('explore')">
      {{ buttonText }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  message: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'default'
  },
  showButton: {
    type: Boolean,
    default: false
  },
  buttonText: {
    type: String,
    default: 'Explorar'
  }
})

defineEmits(['explore'])
</script>

<style scoped>
.empty-state {
  text-align: center;
  padding: 48px 24px;
  max-width: 400px;
  margin: 0 auto;
}

.empty-state-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 24px;
  color: #9ca3af;
}

.empty-state-icon svg {
  width: 100%;
  height: 100%;
}

.empty-state-title {
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.empty-state-message {
  font-size: 16px;
  color: #6b7280;
  margin: 0 0 24px 0;
  line-height: 1.5;
}

.btn-explore {
  background: #8B7355;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-explore:hover {
  background: #704a3a;
}
</style>
