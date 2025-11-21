import axios from 'axios';



const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'https://admin-grupo44.proyecto2025.linti.unlp.edu.ar/api';
console.log('API Base URL being used:', apiBaseUrl);

const api = axios.create({
    baseURL: apiBaseUrl,
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json'
    }
});

api.interceptors.request.use(
    config => config,
    error => Promise.reject(error)
);

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Usuario no autenticado - no redirigir automáticamente
            console.log('Usuario no autenticado');
        }
        return Promise.reject(error);
    }
);

export default api;