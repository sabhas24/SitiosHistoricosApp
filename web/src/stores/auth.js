import { defineStore } from "pinia";
import {ref,computed} from "vue";

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

    function loadUserFromStorage() {
        const storedUser = localStorage.getItem('user');
        const storedAuth = localStorage.getItem('isAuthenticated');
        
        if (storedUser && storedAuth === 'true') {
            user.value = JSON.parse(storedUser);
            isAuthenticated.value = true;
        }
    }

    
    loadUserFromStorage();
   
    return {
        user,
        isAuthenticated,
        loading,
        userName,
        userEmail,
        setUser,
        clearUser,
        loadUserFromStorage
    }
})