const DEFAULT_CONFIG = {
  MINIO_ENDPOINT: 'https://minio.proyecto2025.linti.unlp.edu.ar', 
  MINIO_BUCKET_NAME: 'grupo44',
  MINIO_ACCESS_KEY: '2jLO3UxSs2LC1sw3bH6t',
  MINIO_SECRET_KEY: 'XvKKjeKRyfoqMRlIRB5OVCzlRGhbeYE6oryzcs2V'
}

export const MINIO_CONFIG = {
  endpoint: import.meta.env.VITE_MINIO_ENDPOINT || DEFAULT_CONFIG.MINIO_ENDPOINT,
  bucket: import.meta.env.VITE_MINIO_BUCKET || DEFAULT_CONFIG.MINIO_BUCKET_NAME,
  accessKey: import.meta.env.VITE_MINIO_ACCESS_KEY || DEFAULT_CONFIG.MINIO_ACCESS_KEY,
  secretKey: import.meta.env.VITE_MINIO_SECRET_KEY || DEFAULT_CONFIG.MINIO_SECRET_KEY
}

export function getMinioBaseUrl() {
  return `${MINIO_CONFIG.endpoint}/${MINIO_CONFIG.bucket}`
}


