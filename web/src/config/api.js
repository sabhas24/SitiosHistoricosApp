import axios from 'axios';

// Create axios instance with default configuration
const api = axios.create({
    baseURL: '/api',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json'
    }
});

// Response interceptor for handling authentication errors
api.interceptors.response.use(
    response => response,
    error => {
        if (error.response && error.response.status === 401) {
            const isAuthCheck = error.config && error.config.url && error.config.url.includes('/me/');

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