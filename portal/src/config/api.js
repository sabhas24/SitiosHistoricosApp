import axios from 'axios';

const apiBaseUrl = "https://admin-grupo44.proyecto2025.linti.unlp.edu.ar/api";




const api = axios.create({
    baseURL: apiBaseUrl,
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json'
    },
    paramsSerializer: {
        serialize: (params) => {
            const searchParams = new URLSearchParams();
            for (const key in params) {
                const value = params[key];
                if (Array.isArray(value)) {
                    value.forEach(val => searchParams.append(key, val));
                } else if (value !== undefined && value !== null && value !== '') {
                    searchParams.append(key, value);
                }
            }
            return searchParams.toString();
        }
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


        }
        return Promise.reject(error);
    }
);

export default api;