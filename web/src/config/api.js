import axios from 'axios';

const api=axios.create({
    baseURL:'/api',
    withCredentials: true,
    headers:{
        'Content-Type':'application/json'
    } 
});
api.interceptors.response.use(
    response => response,
    error => {
        if (error.response && error.response.status === 401) {
            if (error.config.url.includes('/me/')) {
                localStorage.removeItem('user');
                localStorage.setItem('isAuthenticated', 'false');
            } else {
                localStorage.removeItem('user');
                localStorage.setItem('isAuthenticated', 'false');
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);
export default api;