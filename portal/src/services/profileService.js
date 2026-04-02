import api from "../config/api";
import favoritesService from "./favoritesService";

export const profileService = {
    async getReviews(page = 1, limit = 25, order = 'latest') {
        try {
            const response = await api.get('/me/reviews', {
                params: { page, per_page: limit, order }
            });

            return {
                items: response.data.reseñas,
                totalPages: response.data.pages
            };
        } catch (error) {
            console.error("Error fetching reviews:", error);
            throw error;
        }
    },

    async getFavorites(page = 1, limit = 25, order = 'latest') {
        // Usar el servicio específico de favoritos para evitar duplicación
        return favoritesService.getFavorites(page, limit, order);
    },

    async removeFavorite(siteId) {
        return favoritesService.removeFromFavorites(siteId);
    }
};
