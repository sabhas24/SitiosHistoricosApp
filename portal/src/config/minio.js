const DEFAULT_CONFIG = {
  MINIO_ENDPOINT: 'http://192.168.100.219:9000',
  MINIO_BUCKET_NAME: 'grupo44',
  MINIO_ACCESS_KEY: 'minioadmin',
  MINIO_SECRET_KEY: 'minioadmin'
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


