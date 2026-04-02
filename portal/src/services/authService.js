import api from '../config/api';

export const authService = {
    async login(email, password) {
        const response = await api.post('/user/login', { email, password });
        return response.data;
    },
    async loginGoogle() {
        window.location.href = `${api.defaults.baseURL}/user/login/google`;
      },
    //modificar
    async register(name, email, password) {
        const response = await api.post('/user/register', { name, email, password });
        return response.data;
    },
    async logout() {
        const response = await api.post('/user/logout');
        return response.data;
    },
    async getCurrentUser() {
        const response = await api.get('/me');
        return response.data;
    },
    redirectToGoogleLogin() {
        window.location.href = `${api.defaults.baseURL}/auth/google/login`;
    }
}