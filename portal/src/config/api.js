import axios from 'axios';

// Create axios instance with default configuration
const api = axios.create({
    baseURL: 'https://admin-grupo44.proyecto2025.linti.unlp.edu.ar/api',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json'
    }
});

// Log de configuración inicial
console.log('🔧 API configurada correctamente:', api.defaults.baseURL);

// Prueba de conexión automática
console.log('🔍 Probando conexión a la API...');
api.get('/').then((response) => {
  console.log('✅ API respondiendo correctamente! Status:', response.status);
}).catch((error) => {
  console.error('❌ Error conectando a API:', error.response?.status || error.message);
});

// Request interceptor para log de requests
api.interceptors.request.use(
    config => {
        console.log('📤 Request a:', config.url);
        return config;
    },
    error => {
        console.error('❌ Error en request:', error);
        return Promise.reject(error);
    }
);

// Response interceptor for handling authentication errors
api.interceptors.response.use(
    response => {
        console.log('📥 Response exitoso:', response.status, 'de', response.config.url);
        return response;
    },
    error => {
        console.error('🚨 Error en API:', error.response?.status, error.response?.data || error.message);
        if (error.response && error.response.status === 401) {
            const url = error.config && error.config.url ? error.config.url : ''
            // Consider any endpoint that includes '/me' (e.g. '/me', '/me/', '/sites/:id/reviews/me')
            // as an auth-check so we only clear local storage but avoid forcing a redirect loop.
            const isAuthCheck = url.includes('/me')

            if (isAuthCheck) {
                localStorage.removeItem('user');
                localStorage.setItem('isAuthenticated', 'false');
            } else {
                localStorage.removeItem('user');
                localStorage.setItem('isAuthenticated', 'false');
                // Only redirect if not already on login page to avoid loops
                if (!window.location.pathname.includes('/login')) {
                    window.location.href = '/login';
                }
            }
        }
        return Promise.reject(error);
    }
);

export default api;