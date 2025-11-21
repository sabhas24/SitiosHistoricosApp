import api from '../config/api'

/**
 * Servicio para manejar todas las operaciones relacionadas con sitios históricos
 */
const sitiosService = {
  /**
   * Obtiene la lista de sitios con filtros y paginación
   * @param {Object} params - Parámetros de búsqueda
   * @param {number} params.page - Número de página (default: 1)
   * @param {number} params.per_page - Items por página (default: 25, max: 100)
   * @param {string} params.name - Filtrar por nombre
   * @param {string} params.description - Filtrar por descripción
   * @param {string} params.city - Filtrar por ciudad
   * @param {string} params.province - Filtrar por provincia
   * @param {string[]} params.tags - Filtrar por tags
   * @param {string} params.order_by - Campo para ordenar (fecha, rating, visits)
   * @param {number} params.lat - Latitud para búsqueda geográfica
   * @param {number} params.long - Longitud para búsqueda geográfica
   * @param {number} params.radius - Radio en km para búsqueda geográfica
   * @returns {Promise<{sitios: Array, meta: Object}>}
   */
  async getSitios(params = {}) {
    try {
      const response = await api.get('/sitios', { params })
      return response.data
    } catch (error) {
      console.error('Error al obtener sitios:', error)
      throw error
    }
  },

  /**
   * Obtiene un sitio específico por ID
   * @param {number} id - ID del sitio
   * @returns {Promise<Object>} Datos del sitio
   */
  async getSitioById(id) {
    try {
      const response = await api.get(`/sitios/${id}`)
      return response.data
    } catch (error) {
      console.error(`Error al obtener sitio ${id}:`, error)
      throw error
    }
  },

  /**
   * Obtiene sitios más visitados
   * @param {number} limit - Cantidad de sitios a retornar
   * @returns {Promise<{sitios: Array, meta: Object}>}
   */
  async getMasVisitados(limit = 8) {
    return this.getSitios({
      order_by: 'visits_desc',
      per_page: limit,
    })
  },

  /**
   * Obtiene sitios mejor puntuados
   * @param {number} limit - Cantidad de sitios a retornar
   * @returns {Promise<{sitios: Array, meta: Object}>}
   */
  async getMejorPuntuados(limit = 8) {
    return this.getSitios({
      order_by: 'rating_desc',
      per_page: limit,
    })
  },

  /**
   * Obtiene sitios recientemente agregados
   * @param {number} limit - Cantidad de sitios a retornar
   * @returns {Promise<{sitios: Array, meta: Object}>}
   */
  async getRecientes(limit = 8) {
    return this.getSitios({
      order_by: 'latest',
      per_page: limit,
    })
  },

  /**
   * Busca sitios por nombre
   * @param {string} searchQuery - Término de búsqueda
   * @param {Object} additionalParams - Parámetros adicionales
   * @returns {Promise<{sitios: Array, meta: Object}>}
   */
  async searchSitios(searchQuery, additionalParams = {}) {
    return this.getSitios({
      name: searchQuery,
      ...additionalParams,
    })
  },

  /**
   * Obtiene las opciones disponibles para filtros
   * @returns {Promise<{provincias: Array, ciudades: Array, categorias: Array, estados_conservacion: Array, tags: Array}>}
   */
  async getFilterOptions() {
    try {
      const response = await api.get('/sitios/filters')
      return response.data
    } catch (error) {
      console.error('Error al obtener opciones de filtros:', error)
      throw error
    }
  },
}

export default sitiosService
