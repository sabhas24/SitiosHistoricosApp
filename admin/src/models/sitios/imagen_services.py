import os
import uuid
from io import BytesIO
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
from flask import current_app
from sqlalchemy import func
from minio import Minio
from minio.error import S3Error
from src.models.database import db
from src.models.sitios.imagen_sitio import ImagenSitio
from src.models.sitios.sitio_historico import SitioHistorico


# restriccioens
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
MAX_IMAGES_PER_SITE = 10


def init_minio():
    """Inicializa el cliente MinIO"""
    # Validar configuración
    endpoint = current_app.config.get('MINIO_ENDPOINT')
    access_key = current_app.config.get('MINIO_ACCESS_KEY')
    secret_key = current_app.config.get('MINIO_SECRET_KEY')
    secure = current_app.config.get('MINIO_SECURE', False)
    
    if not endpoint:
        raise Exception("MINIO_ENDPOINT no está configurado")
    if not access_key:
        raise Exception("MINIO_ACCESS_KEY no está configurado")
    if not secret_key:
        raise Exception("MINIO_SECRET_KEY no está configurado")
    
    return Minio(
        endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=secure,
    )


def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_unique_filename(original_filename):
    """Genera un nombre único para el archivo"""
    ext = original_filename.rsplit('.', 1)[1].lower()
    unique_id = str(uuid.uuid4())
    return f"{unique_id}.{ext}"


def upload_image_to_minio(file, filename):
    """Sube una imagen a MinIO y retorna la URL pública"""
    try:
        minio_client = init_minio()
        bucket_name = current_app.config.get('MINIO_BUCKET_NAME')
        endpoint = current_app.config.get('MINIO_ENDPOINT')
        
        if not bucket_name:
            raise Exception("MINIO_BUCKET_NAME no está configurado")
        if not endpoint:
            raise Exception("MINIO_ENDPOINT no está configurado")
        
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
        
        #prepara archivo
        file.seek(0)
        file_data = file.read()
        file_size = len(file_data)
        file_stream = BytesIO(file_data)
        
        # subida
        minio_client.put_object(
            bucket_name,
            filename,
            file_stream,
            length=file_size,
            content_type=file.mimetype
        )
        
        url_publica = f"http://{endpoint}/{bucket_name}/{filename}"
        return url_publica
        
    except S3Error as e:
        raise Exception(f"Error al subir imagen a MinIO: {e}")


def delete_image_from_minio(filename):
    """Elimina una imagen de MinIO"""
    try:
        minio_client = init_minio()
        bucket_name = current_app.config.get('MINIO_BUCKET_NAME')
        
        if not bucket_name:
            raise Exception("MINIO_BUCKET_NAME no está configurado")
        
        minio_client.remove_object(bucket_name, filename)
        return True
        
    except S3Error as e:
        raise Exception(f"Error al eliminar imagen de MinIO: {e}")


def agregar_imagen_sitio(sitio_id, file, titulo_alt, descripcion=None):
    """Agrega una nueva imagen a un sitio histórico"""

    sitio = db.session.query(SitioHistorico).get(sitio_id)
    if not sitio:
        return False, "Sitio no encontrado"
    
    if not sitio.puede_agregar_imagen:
        return False, f"Máximo {MAX_IMAGES_PER_SITE} imágenes por sitio"
    
    if not file or file.filename == '':
        return False, "No se seleccionó archivo"
    
    if not allowed_file(file.filename):
        return False, "Formato de archivo no permitido (JPG, PNG, WEBP)"
    
    if file.content_length > MAX_FILE_SIZE:
        return False, "Archivo muy grande (máximo 5 MB)"
    
    try:
        #uid
        filename = generate_unique_filename(file.filename)
    
        url_publica = upload_image_to_minio(file, filename)
        
        max_orden = db.session.query(func.max(ImagenSitio.orden)).filter(
            ImagenSitio.sitio_id == sitio_id
        ).scalar() or 0
        
        #guardar en bd
        imagen = ImagenSitio(
            sitio_id=sitio_id,
            url_publica=url_publica,
            nombre_archivo=filename,
            titulo_alt=titulo_alt,
            descripcion=descripcion,
            orden=max_orden + 1,
            es_portada=len(sitio.imagenes) == 0 # primera imagen es portada
        )
        
        db.session.add(imagen)
        db.session.commit()
        
        return True, "Imagen agregada exitosamente"
        
    except Exception as e:
        db.session.rollback()
        return False, f"Error al agregar imagen: {str(e)}"


def marcar_como_portada(imagen_id):
    """Marca una imagen como portada del sitio"""
    imagen = db.session.query(ImagenSitio).get(imagen_id)
    if not imagen:
        return False, "Imagen no encontrada"
    
    try:
        db.session.query(ImagenSitio).filter(
            ImagenSitio.sitio_id == imagen.sitio_id,
            ImagenSitio.es_portada == True
        ).update({'es_portada': False})
        
        imagen.es_portada = True
        db.session.commit()
        
        return True, "Imagen marcada como portada"
        
    except Exception as e:
        db.session.rollback()
        return False, f"Error al marcar portada: {str(e)}"


def eliminar_imagen(imagen_id):
    """Elimina una imagen del sitio"""
    imagen = db.session.query(ImagenSitio).get(imagen_id)
    if not imagen:
        return False, "Imagen no encontrada"
    
    if imagen.es_portada:
        return False, "No se puede eliminar la imagen portada. Cambie la portada primero"
    
    try:
        delete_image_from_minio(imagen.nombre_archivo)
        
        db.session.delete(imagen)
        db.session.commit()
        
        return True, "Imagen eliminada exitosamente"
        
    except Exception as e:
        db.session.rollback()
        return False, f"Error al eliminar imagen: {str(e)}"


def reordenar_imagenes(sitio_id, orden_ids):
    """Reordena las imágenes de un sitio"""
    try:
        for index, imagen_id in enumerate(orden_ids, 1):
            db.session.query(ImagenSitio).filter(
                ImagenSitio.id == imagen_id,
                ImagenSitio.sitio_id == sitio_id
            ).update({'orden': index})
        
        db.session.commit()
        return True, "Imágenes reordenadas exitosamente"
        
    except Exception as e:
        db.session.rollback()
        return False, f"Error al reordenar imágenes: {str(e)}"


def obtener_imagenes_sitio(sitio_id):
    """Obtiene todas las imágenes de un sitio ordenadas"""
    return db.session.query(ImagenSitio).filter(
        ImagenSitio.sitio_id == sitio_id
    ).order_by(ImagenSitio.orden).all()
