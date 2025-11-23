import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// Log de configuración inicial


// Interceptor para agregar token JWT si existe
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('jwt_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`

    }

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
