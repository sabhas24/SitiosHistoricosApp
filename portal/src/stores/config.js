import { defineStore } from 'pinia'
import api from '@/config/api'

export const useConfigStore = defineStore('config', {
    state: () => ({
        reviewsEnabled: true, // Default to true to avoid flashing hidden state
        loading: false,
        error: null
    }),

    actions: {
        async fetchConfig() {
            this.loading = true
            try {
                const response = await api.get('/config')
                if (response.data) {
                    this.reviewsEnabled = response.data.reviews_enabled
                }
            } catch (error) {
                console.error('Error fetching config:', error)
                this.error = error
            } finally {
                this.loading = false
            }
        }
    }
})
