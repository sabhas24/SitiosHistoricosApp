import { defineStore } from "pinia";
import {ref,computed} from "vue";
import api from "../config/api"
export const useAuthStore = defineStore("auth", () => {
    const user = ref(null);
    const isAuthenticated = ref(false);
    const loading = ref(false);

    const userName = computed(() => user.value ? user.value.name : "");
    const userEmail = computed(() => user.value ? user.value.email : "");
    
    function setUser(userData) {
        user.value = userData;
        isAuthenticated.value = true;
        localStorage.setItem("user", JSON.stringify(userData));
        localStorage.setItem("isAuthenticated", "true");
    }
    
    function clearUser() {
        user.value = null;
        isAuthenticated.value = false;
        localStorage.removeItem('user');
        localStorage.removeItem('isAuthenticated');
    }
    async function checkSession() {
        loading.value = true;
        try {
            const response=await api.get('/me/');
            setUser(response.data);

            return true;
         } catch (error) {
            clearUser();
            return false;
         }finally {
            loading.value = false;
         }
    
    }
    return {
        user,
        isAuthenticated,
        loading,
        userName,
        userEmail,
        setUser,
        clearUser,
        checkSession
        
    }
})