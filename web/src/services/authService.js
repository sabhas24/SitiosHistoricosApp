import api from '../config/api';


export const authService ={
    async login(email, password) {
        const response = await api.post('/user/login', { email, password });
        return response.data;
    },
    async loginGoogle() {
        const response = await api.get('/user/login/google');
        return response.data;
    },
    async register(name, email, password) {
        const response = await api.post('/user/register', { name, email, password });
        return response.data;
    },
    async logout() {
        const response = await api.post('/user/logout');
        return response.data;
    },
    async getCurrentUser() {
        const response = await api.get('/user/user');
        return response.data;
    },
    redirectToGoogleLogin() {
        window.location.href = 'http://localhost:5000/api/auth/google/login';
    }
}