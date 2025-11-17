<template>
  <div class="profile-header">
    <div class="profile-header-content">
      <div class="profile-avatar">
        {{ userInitial }}
      </div>
      <div class="profile-info">
        <h1 class="profile-name">{{ userName }}</h1>
        <p class="profile-email">{{ userEmail }}</p>
        <p class="profile-role">Explorador de Patrimonio Histórico</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  userName: {
    type: String,
    required: true
  },
  userEmail: {
    type: String,
    required: true
  }
})

const userInitial = computed(() => {
  return props.userName ? props.userName.charAt(0).toUpperCase() : 'U'
})
</script>

<style scoped>
.profile-header {
  background: linear-gradient(135deg, #8B7355 0%, #A0826D 100%);
  border-radius: 12px;
  padding: 32px 24px;
  margin-bottom: 32px;
  color: white;
}

.profile-header-content {
  display: flex;
  align-items: center;
  gap: 24px;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  font-weight: bold;
  flex-shrink: 0;
}

.profile-info h1,
.profile-info p {
  margin: 0;
}

.profile-name {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 4px;
}

.profile-email {
  font-size: 16px;
  opacity: 0.9;
  margin-bottom: 8px;
}

.profile-role {
  font-size: 14px;
  opacity: 0.8;
  font-style: italic;
}

@media (max-width: 768px) {
  .profile-header {
    padding: 24px 16px;
  }

  .profile-header-content {
    flex-direction: column;
    text-align: center;
  }

  .profile-avatar {
    width: 64px;
    height: 64px;
    font-size: 28px;
  }

  .profile-name {
    font-size: 24px;
  }
}
</style>
