<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h1 class="register-title">Crear cuenta</h1>
        <p class="register-subtitle">Regístrate para explorar el patrimonio histórico</p>
      </div>

      <form @submit.prevent="handleSubmit" class="register-form">
        <div class="form-group">
          <label for="name" class="form-label">Nombre</label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            class="form-input"
            :class="{ 'form-input--error': errors.name }"
            placeholder="Tu nombre"
            required
          />
          <span v-if="errors.name" class="form-error">{{ errors.name }}</span>
        </div>

        <div class="form-group">
          <label for="lastName" class="form-label">Apellido</label>
          <input
            id="lastName"
            v-model="form.lastName"
            type="text"
            class="form-input"
            :class="{ 'form-input--error': errors.lastName }"
            placeholder="Tu apellido"
            required
          />
          <span v-if="errors.lastName" class="form-error">{{ errors.lastName }}</span>
        </div>

        <div class="form-group">
          <label for="email" class="form-label">Correo electrónico</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            class="form-input"
            :class="{ 'form-input--error': errors.email }"
            placeholder="tu@email.com"
            required
          />
          <span v-if="errors.email" class="form-error">{{ errors.email }}</span>
        </div>

        <div class="form-group">
          <label for="password" class="form-label">Contraseña</label>
          <div class="password-input-container">
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              class="form-input"
              :class="{ 'form-input--error': errors.password }"
              placeholder="Mínimo 8 caracteres"
              required
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="password-toggle"
              :aria-label="showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
            >
              <svg v-if="showPassword" class="eye-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"></path>
              </svg>
              <svg v-else class="eye-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
              </svg>
            </button>
          </div>
          <span v-if="errors.password" class="form-error">{{ errors.password }}</span>
        </div>

        <div class="form-group">
          <label for="confirmPassword" class="form-label">Confirmar contraseña</label>
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            type="password"
            class="form-input"
            :class="{ 'form-input--error': errors.confirmPassword }"
            placeholder="Repite tu contraseña"
            required
          />
          <span v-if="errors.confirmPassword" class="form-error">{{ errors.confirmPassword }}</span>
        </div>

        <div class="form-group">
          <label class="checkbox-container">
            <input
              v-model="form.acceptTerms"
              type="checkbox"
              class="checkbox-input"
              required
            />
            <span class="checkmark"></span>
            <span class="checkbox-label">
              Acepto los <a href="#" class="link">términos y condiciones</a> y la <a href="#" class="link">política de privacidad</a>
            </span>
          </label>
          <span v-if="errors.acceptTerms" class="form-error">{{ errors.acceptTerms }}</span>
        </div>

        <button
          type="submit"
          class="register-button"
          :disabled="isLoading"
        >
          <span v-if="isLoading" class="loading-spinner"></span>
          {{ isLoading ? 'Creando cuenta...' : 'Crear cuenta' }}
        </button>
      </form>

      <div class="register-footer">
        <p class="login-link">
          ¿Ya tienes cuenta?
          <router-link to="/login" class="link">Inicia sesión</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../config/api'

const router = useRouter()

// Form data
const form = reactive({
  name: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: '',
  acceptTerms: false
})

// UI state
const showPassword = ref(false)
const isLoading = ref(false)

// Errors
const errors = reactive({
  name: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: '',
  acceptTerms: ''
})

// Validation functions
const validateForm = () => {
  // Reset errors
  Object.keys(errors).forEach(key => {
    errors[key] = ''
  })

  let isValid = true

  // Name validation
  if (!form.name.trim()) {
    errors.name = 'El nombre es obligatorio'
    isValid = false
  } else if (form.name.trim().length < 1) {
    errors.name = 'El nombre debe tener al menos 1 caracter'
    isValid = false
  } else if (form.name.trim().length > 80) {
    errors.name = 'El nombre no puede tener más de 80 caracteres'
    isValid = false
  }

  // Last name validation
  if (!form.lastName.trim()) {
    errors.lastName = 'El apellido es obligatorio'
    isValid = false
  } else if (form.lastName.trim().length < 1) {
    errors.lastName = 'El apellido debe tener al menos 1 caracter'
    isValid = false
  } else if (form.lastName.trim().length > 80) {
    errors.lastName = 'El apellido no puede tener más de 80 caracteres'
    isValid = false
  }

  // Email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!form.email.trim()) {
    errors.email = 'El correo electrónico es obligatorio'
    isValid = false
  } else if (!emailRegex.test(form.email)) {
    errors.email = 'Ingresa un correo electrónico válido'
    isValid = false
  }

  // Password validation
  if (!form.password) {
    errors.password = 'La contraseña es obligatoria'
    isValid = false
  } else if (form.password.length < 8) {
    errors.password = 'La contraseña debe tener al menos 8 caracteres'
    isValid = false
  } else if (form.password.length > 128) {
    errors.password = 'La contraseña no puede tener más de 128 caracteres'
    isValid = false
  }

  // Confirm password validation
  if (!form.confirmPassword) {
    errors.confirmPassword = 'Confirma tu contraseña'
    isValid = false
  } else if (form.password !== form.confirmPassword) {
    errors.confirmPassword = 'Las contraseñas no coinciden'
    isValid = false
  }

  // Terms validation
  if (!form.acceptTerms) {
    errors.acceptTerms = 'Debes aceptar los términos y condiciones'
    isValid = false
  }

  return isValid
}

// Submit handler
const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }

  isLoading.value = true

  try {
    const response = await api.post('/user/register', {
      name: form.name.trim(),
      last_name: form.lastName.trim(),
      email: form.email.trim().toLowerCase(),
      password: form.password
    })

    alert('¡Cuenta creada exitosamente! Revisa tu correo para verificar tu cuenta.')
    router.push('/login')

  } catch (error) {
    console.error('Registration error:', error)
    if (error.response?.data?.message) {
      if (error.response.data.message.includes('correo ya está registrado')) {
        errors.email = 'Este correo electrónico ya está registrado'
      } else if (error.response.data.message.includes('validacion')) {
        const validationErrors = error.response.data.details
        if (validationErrors?.email) {
          errors.email = validationErrors.email.join(', ')
        }
        if (validationErrors?.name) {
          errors.name = validationErrors.name.join(', ')
        }
        if (validationErrors?.last_name) {
          errors.lastName = validationErrors.last_name.join(', ')
        }
        if (validationErrors?.password) {
          errors.password = validationErrors.password.join(', ')
        }
      } else {
        errors.email = error.response.data.message
      }
    } else {
      errors.email = 'Error al crear la cuenta. Inténtalo de nuevo.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.register-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 100%;
  max-width: 480px;
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.register-header {
  text-align: center;
  margin-bottom: 32px;
}

.register-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.register-subtitle {
  color: #6b7280;
  font-size: 1rem;
  margin: 0;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.form-input {
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;
  background: #ffffff;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input--error {
  border-color: #ef4444;
}

.form-input--error:focus {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.form-error {
  font-size: 0.875rem;
  color: #ef4444;
  font-weight: 500;
}

.password-input-container {
  position: relative;
}

.password-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  color: #6b7280;
  transition: color 0.2s ease;
}

.password-toggle:hover {
  color: #374151;
}

.eye-icon {
  width: 20px;
  height: 20px;
}

.checkbox-container {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
  font-size: 0.875rem;
  line-height: 1.5;
  color: #374151;
}

.checkbox-input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.checkmark {
  position: relative;
  width: 20px;
  height: 20px;
  background: #ffffff;
  border: 2px solid #d1d5db;
  border-radius: 4px;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.checkbox-container:hover .checkmark {
  border-color: #667eea;
}

.checkbox-input:checked ~ .checkmark {
  background: #667eea;
  border-color: #667eea;
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
  left: 6px;
  top: 2px;
  width: 6px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-input:checked ~ .checkmark:after {
  display: block;
}

.checkbox-label {
  margin: 0;
}

.link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.link:hover {
  text-decoration: underline;
}

.register-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 14px 24px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 8px;
}

.register-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.register-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.register-footer {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
  text-align: center;
}

.login-link {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}

/* Responsive design */
@media (max-width: 640px) {
  .register-container {
    padding: 16px;
  }

  .register-card {
    padding: 24px;
  }

  .register-title {
    font-size: 1.75rem;
  }

  .register-subtitle {
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .register-card {
    padding: 20px;
  }

  .register-form {
    gap: 20px;
  }

  .form-input {
    padding: 10px 14px;
  }
}
</style>