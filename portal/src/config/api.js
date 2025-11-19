import axios from 'axios';


const api = axios.create({
    baseURL: 'https://grupo44.proyecto2025.linti.unlp.edu.ar/api',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json'
    }
});


api.interceptors.response.use(
    response => response,
    error => {
        if (error.response && error.response.status === 401) {
            const url = error.config && error.config.url ? error.config.url : ''

            const isAuthCheck = url.includes('/me')

            if (isAuthCheck) {
                localStorage.removeItem('user');
                localStorage.setItem('isAuthenticated', 'false');
            } else {
                localStorage.removeItem('user');
                localStorage.setItem('isAuthenticated', 'false');

                if (!window.location.pathname.includes('/login')) {
                    window.location.href = '/login';
                }
            }
        }
        return Promise.reject(error);
    }
);

export default api;