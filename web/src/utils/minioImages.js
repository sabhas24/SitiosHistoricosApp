

import { getMinioBaseUrl } from '../config/minio.js'

const DEFAULT_FALLBACK_IMAGE = 'https://turismo.buenosaires.gob.ar/sites/turismo/files/field/image/congreso_nacional_fuente_1200.jpg'

export function getMinioImageUrl(imagePath) {
  if (!imagePath) {
    return DEFAULT_FALLBACK_IMAGE
  }

  if (imagePath.startsWith('http')) {
    return imagePath
  }
  const cleanPath = imagePath.startsWith('/') ? imagePath.substring(1) : imagePath
  return `${getMinioBaseUrl()}/${cleanPath}`
}

export function minioImg(imagePath, fallback = DEFAULT_FALLBACK_IMAGE) {
  try {
    return getMinioImageUrl(imagePath || fallback)
  } catch (error) {
    console.warn('Error loading image from MinIO:', error)
    return fallback.startsWith('http') ? fallback : getMinioImageUrl(fallback)
  }
}
