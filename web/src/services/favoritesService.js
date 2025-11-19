import api from "../config/api";

export const favoritesService = {
    /**
     * Agregar un sitio a favoritos
     * @param {number} siteId - ID del sitio
     * @returns {Promise} Promesa que se resuelve cuando se agrega a favoritos
     */
    async addToFavorites(siteId) {
        try {
            const response = await api.put(`/sites/${siteId}/favorite`);
            return response.data;
        } catch (error) {
            console.error("Error adding to favorites:", error);
            throw error;
        }
    },

    /**
     * Eliminar un sitio de favoritos
     * @param {number} siteId - ID del sitio
     * @returns {Promise} Promesa que se resuelve cuando se elimina de favoritos
     */
    async removeFromFavorites(siteId) {
        try {
            const response = await api.delete(`/sites/${siteId}/favorite`);
            return response.data;
        } catch (error) {
            console.error("Error removing from favorites:", error);
            throw error;
        }
    },

    /**
     * Verificar si un sitio está en favoritos
     * @param {number} siteId - ID del sitio
     * @returns {Promise<boolean>} True si está en favoritos, false si no
     */
    async isFavorite(siteId) {
        try {
            const response = await api.get('/me/favoritos');
            const favorites = response.data.favoritos || [];
            return favorites.some(fav => fav.sitio && fav.sitio.id === siteId);
        } catch (error) {
            console.error("Error checking favorite status:", error);
            return false;
        }
    },

    /**
     * Obtener todos los favoritos del usuario
     * @param {number} page - Página actual
     * @param {number} limit - Cantidad de elementos por página
     * @param {string} order - Orden de los elementos
     * @returns {Promise} Lista de favoritos
     */
    async getFavorites(page = 1, limit = 25, order = 'latest') {
        try {
            const response = await api.get('/me/favoritos', {
                params: { page, per_page: limit, order }
            });

            const items = response.data.favoritos.map(f => ({
                id: f.sitio.id,
                name: f.sitio.nombre,
                image: f.sitio.imagen_principal,
                location: f.sitio.ciudad,
                rating: f.sitio.calificacion_promedio || 0
            }));

            return {
                items: items,
                totalPages: response.data.total_pages
            };
        } catch (error) {
            console.error("Error fetching favorites:", error);
            throw error;
        }
    }
};

export default favoritesService;
