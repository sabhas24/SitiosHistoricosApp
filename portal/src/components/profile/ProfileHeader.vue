<template>
  <div class="profile-header" :style="{ backgroundColor: profileColor }">
    <div class="profile-header-content">
      <div class="profile-avatar" @click="openModal">
        <template v-if="profilePicture">
          <img :src="profilePicture" alt="Foto de perfil" class="avatar-img" />
        </template>
        <template v-else>
          {{ userInitial }}
        </template>
      </div>
      <div class="profile-info">
        <h1 class="profile-name">{{ userName }}</h1>
        <p class="profile-email">{{ userEmail }}</p>
        <p class="profile-role">amante de la histiria</p>
      </div>
    </div>
  </div>

  <div v-if="isModalOpen" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <span class="close-button" @click="closeModal">&times;</span>
      <img :src="profilePicture" alt="Foto de perfil ampliada" class="modal-image" />
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const isModalOpen = ref(false)

const openModal = () => {
  if (props.profilePicture) {
    isModalOpen.value = true
  }
}

const closeModal = () => {
  isModalOpen.value = false
}


const props = defineProps({
  userName: {
    type: String,
    required: true
  },
  userEmail: {
    type: String,
    required: true
  },
  profilePicture: {
    type: String,
    default: ''
  },
  profileColor: {
    type: String,
    default: '#8B7355'
  },
})

const userInitial = computed(() => {
  return props.userName ? props.userName.charAt(0).toUpperCase() : 'U'
})
</script>

<style scoped>
.profile-header {
  
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
  cursor: pointer;
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

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  position: relative;
  background-color: white;
  padding: 10px;
  border-radius: 8px;
  max-width: 90vw;
  max-height: 90vh;

}

.close-button {
  position: absolute;
  top: 1px;
  right: 20px;
  font-size: 30px;
  font-weight: bold;
  cursor: pointer;
  color: rgb(252, 250, 250);
  text-shadow: 0 0 9px rgba(0, 0, 0, 0.8);
  z-index: 1;
}

.modal-image {
  max-width: 100%;
  max-height: 100%;
  display: block;
  margin: 0 auto;
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
