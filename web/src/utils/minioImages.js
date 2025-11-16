

import { getMinioBaseUrl } from '../config/minio.js'

export function getMinioImageUrl(imagePath) {
  if (!imagePath) {
    return `${getMinioBaseUrl()}/placeholder-image.jpg`
  }
  
  if (imagePath.startsWith('http')) {
    return imagePath
  }
  const cleanPath = imagePath.startsWith('/') ? imagePath.substring(1) : imagePath
  
  return `${getMinioBaseUrl()}/${cleanPath}`
}

export function minioImg(imagePath, fallback = 'placeholder-image.jpg') {
  try {
    return getMinioImageUrl(imagePath || fallback)
  } catch (error) {
    console.warn('Error loading image from MinIO:', error)
    return getMinioImageUrl(fallback)
  }
}
