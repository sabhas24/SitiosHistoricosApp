import api from "@/config/api";
export const profileService = {
    async getReviews(page = 1, limit = 25, order = 'desc') {
        try {
            const response = await api.get('/me/reviews', {
                params: { page, per_page: limit, order }
            });

            return {
                items: response.data.data,
                totalPages: Math.ceil(response.data.meta.total / limit)
            };
        } catch (error) {
            console.error("Error fetching reviews:", error);
            throw error;
        }
    },

    async getFavorites(page = 1, limit = 25, order = 'desc') {
        try {
            const response = await api.get('/me/favoritos', {
                params: { page, per_page: limit, order }
            });
            const items = response.data.favoritos.map(f => ({
                id: f.sitio.id,
                name: f.sitio.nombre,
                image: f.sitio.imagen,
                location: f.sitio.ciudad,
                rating: f.sitio.calificacion_promedio
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