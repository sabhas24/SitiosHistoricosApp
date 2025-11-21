import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "../config/api"
export const useAuthStore = defineStore("auth", () => {
    const user = ref(JSON.parse(localStorage.getItem("user")) || null);
    const isAuthenticated = ref(localStorage.getItem("isAuthenticated") === "true");
    const loading = ref(false);

    const userName = computed(() => user.value ? user.value.name : "");
    const userEmail = computed(() => user.value ? user.value.email : "");
    const userProfilePicture = computed(() => user.value ? user.value.profile_picture : "");

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
            const response = await api.get('/me/');
            setUser(response.data);

            return true;
        } catch (error) {
            console.log('AuthStore - checkSession error:', error);
            clearUser();
            return false;
        } finally {
            loading.value = false;
        }

    }
    return {
        user,
        isAuthenticated,
        loading,
        userName,
        userEmail,
        userProfilePicture,
        setUser,
        clearUser,
        checkSession

    }
})