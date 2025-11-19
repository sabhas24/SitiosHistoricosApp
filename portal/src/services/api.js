import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://grupo44.proyecto2025.linti.unlp.edu.ar/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// Log de configuración inicial
console.log('🔧 API configurada:', API_BASE_URL);

// Interceptor para agregar token JWT si existe
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('jwt_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
      console.log('🔐 Token JWT agregado al request');
    }
    console.log('📤 Request a:', config.url);
    return config
  },
  (error) => {
    console.error('❌ Error en request:', error);
    return Promise.reject(error)
  }
)

// Interceptor para manejar errores
apiClient.interceptors.response.use(
  (response) => {
    console.log('📥 Response exitoso:', response.status, 'de', response.config.url);
    return response;
  },
  (error) => {
    console.error('🚨 Error API:', error.response?.status, error.response?.data || error.message);
    if (error.response?.status === 401) {
      console.warn('⚠️ Token expirado - limpiando localStorage');
      // Token expirado o inválido
      localStorage.removeItem('jwt_token')
      // Opcional: redirigir a login
    }
    return Promise.reject(error)
  }
)

export default apiClient
