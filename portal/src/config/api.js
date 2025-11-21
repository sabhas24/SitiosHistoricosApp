import axios from 'axios';


const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
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