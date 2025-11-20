import axios from 'axios';

const api = axios.create({
    baseURL: 'https://admin-grupo44.proyecto2025.linti.unlp.edu.ar/api',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json'
    }
});

// Interceptor de requests
api.interceptors.request.use(
    config => config,
    error => Promise.reject(error)
);

// Interceptor de responses para manejar errores de autenticación
api.interceptors.response.use(
    response => response,
    error => {
        if (error.response && error.response.status === 401) {
            localStorage.removeItem('user');
            localStorage.setItem('isAuthenticated', 'false');
            if (!window.location.pathname.includes('/login')) {
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export default api;