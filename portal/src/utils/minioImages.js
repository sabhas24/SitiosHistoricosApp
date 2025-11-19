

// import { getMinioBaseUrl } from '../config/minio.js'

const DEFAULT_FALLBACK_IMAGE = '/placeholder-image.jpg'

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
