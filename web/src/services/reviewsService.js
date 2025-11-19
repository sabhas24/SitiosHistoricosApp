import api from '../config/api'

const reviewsService = {
    async getPublicReviews(siteId, page = 1, per_page = 10) {
        const response = await api.get(`/sites/${siteId}/reviews/public`, { params: { page, per_page } })
        return response.data
    },

    async getSiteReviewsAuth(siteId, page = 1, per_page = 10) {
        const response = await api.get(`/sites/${siteId}/reviews`, { params: { page, per_page } })
        return response.data
    },

    async getMyReview(siteId) {
        const response = await api.get(`/sites/${siteId}/reviews/me`)
        return response.data
    },

    async createReview(siteId, rating, comment) {
        const payload = { site_id: siteId, rating, comment }
        const response = await api.post(`/sites/${siteId}/reviews`, payload)
        return response.data
    },

    async updateReview(siteId, reviewId, rating, comment) {
        const payload = {}
        if (rating !== undefined) payload.rating = rating
        if (comment !== undefined) payload.comment = comment
        const response = await api.put(`/sites/${siteId}/reviews/${reviewId}`, payload)
        return response.data
    },

    async deleteReview(siteId, reviewId) {
        const response = await api.delete(`/sites/${siteId}/reviews/${reviewId}`)
        return response.data
    }
}

export default reviewsService
