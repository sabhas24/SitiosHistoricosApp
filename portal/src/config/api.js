import axios from 'axios';


const api = axios.create({
    baseURL: "http://grupo44.proyecto2025.linti.unlp.edu.ar:5000/api",
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