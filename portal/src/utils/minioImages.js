

import { getMinioBaseUrl } from '../config/minio.js'

// Use the placeholder image from MinIO
function getPlaceholderImage() {
  try {
    return `${getMinioBaseUrl()}/placeholder-image.jpg`
  } catch {
    // Fallback if MinIO config fails
    return 'https://minio.proyecto2025.linti.unlp.edu.ar/grupo44/placeholder-image.jpg'
  }
}

const DEFAULT_FALLBACK_IMAGE = getPlaceholderImage()

export function getMinioImageUrl(imagePath) {
  if (!imagePath) {
    return DEFAULT_FALLBACK_IMAGE
  }

  if (imagePath.startsWith('http')) {
    return imagePath
  }
  
  return DEFAULT_FALLBACK_IMAGE
}

export function minioImg(imagePath, fallback = DEFAULT_FALLBACK_IMAGE) {
    return getMinioImageUrl(imagePath || fallback)
}
