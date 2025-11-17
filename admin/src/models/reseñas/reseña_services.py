from datetime import datetime, timezone
from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload
from src.models.database import db
from src.models.reseñas.reseña import Reseña, EstadoReseña


def obtener_reseñas(page=1, per_page=25, filters=None):
    """Obtener lista paginada de reseñas con filtros opcionales"""
    query = db.session.query(Reseña).options(
        joinedload(Reseña.sitio), joinedload(Reseña.usuario_moderador)
    )

    if filters:
        if filters.get("estado"):
            try:
                estado_enum = EstadoReseña(filters["estado"])
                query = query.filter(Reseña.estado == estado_enum)
            except ValueError:
                pass

        if filters.get("calificacion"):
            try:
                calificacion = int(filters["calificacion"])
                if 1 <= calificacion <= 5:
                    query = query.filter(Reseña.calificacion == calificacion)
            except (ValueError, TypeError):
                pass

        if filters.get("sitio"):
            from src.models.sitios.sitio_historico import SitioHistorico

            query = query.join(SitioHistorico).filter(
                or_(
                    SitioHistorico.nombre.ilike(f"%{filters['sitio']}%"),
                    SitioHistorico.ciudad.ilike(f"%{filters['sitio']}%"),
                )
            )

        if filters.get("usuario"):
            query = query.filter(
                or_(
                    Reseña.nombre_usuario.ilike(f"%{filters['usuario']}%"),
                    Reseña.email_usuario.ilike(f"%{filters['usuario']}%"),
                )
            )

        if filters.get("fecha_desde"):
            try:
                fecha_desde = datetime.strptime(filters["fecha_desde"], "%Y-%m-%d")
                query = query.filter(Reseña.fecha_creacion >= fecha_desde)
            except ValueError:
                pass

        if filters.get("fecha_hasta"):
            try:
                fecha_hasta = datetime.strptime(filters["fecha_hasta"], "%Y-%m-%d")
                fecha_hasta = fecha_hasta.replace(hour=23, minute=59, second=59)
                query = query.filter(Reseña.fecha_creacion <= fecha_hasta)
            except ValueError:
                pass

    orden_campo = filters.get("orden_campo", "fecha") if filters else "fecha"
    orden_direccion = filters.get("orden_direccion", "desc") if filters else "desc"

    if orden_campo == "calificacion":
        if orden_direccion == "lasted":
            query = query.order_by(Reseña.calificacion.asc())
        else:
            query = query.order_by(Reseña.calificacion.desc())
    else:
        if orden_direccion == "oldest":
            query = query.order_by(Reseña.fecha_creacion.asc())
        else:
            query = query.order_by(Reseña.fecha_creacion.desc())

    # paginacion
    offset = (page - 1) * per_page
    total = query.count()
    reseñas = query.offset(offset).limit(per_page).all()
    total_pages = (total + per_page - 1) // per_page if total > 0 else 1
    has_prev = page > 1
    has_next = page < total_pages

    return {
        "reseñas": reseñas,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "has_prev": has_prev,
        "has_next": has_next,
        "prev_num": page - 1 if has_prev else None,
        "next_num": page + 1 if has_next else None,
        "filters": filters or {},
    }


def obtener_reseñas_por_usuario(idmail, page=1, per_page=25, order="lasted"):
    """Obtiene todas las reseñas de un usuario específico"""
    query = (
        db.session.query(Reseña)
        .options(joinedload(Reseña.sitio), joinedload(Reseña.usuario_moderador))
        .filter(Reseña.email_usuario == idmail)
    )

    if order == "lasted":
        query = query.order_by(Reseña.fecha_creacion.desc())
    else:
        query = query.order_by(Reseña.fecha_creacion.asc())

    offset = (page - 1) * per_page
    total = query.count()

    reseñas = query.offset(offset).limit(per_page).all()
    total_pages = (total + per_page - 1) // per_page if total > 0 else 1
    has_prev = page > 1
    has_next = page < total_pages
    return {
        "reseñas": reseñas,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": total_pages,
        "has_prev": has_prev,
        "has_next": has_next,
    }


def obtener_reseña_por_id(reseña_id, page=1, per_page=25, order="lasted"):
    return (
        db.session.query(Reseña)
        .options(joinedload(Reseña.sitio), joinedload(Reseña.usuario_moderador))
        .filter(Reseña.id == reseña_id)
        .first()
    )


def obtener_reseñas_por_sitio(sitio_id, page=1, per_page=25):
    """Obtiene reseñas APROBADAS de un sitio (para API pública)"""
    query = (
        db.session.query(Reseña)
        .options(joinedload(Reseña.sitio), joinedload(Reseña.usuario_moderador))
        .filter(
            and_(
                Reseña.sitio_id == sitio_id,
                Reseña.estado == EstadoReseña.APROBADA,  # Solo reseñas aprobadas
            )
        )
    )

    query = query.order_by(Reseña.fecha_creacion.desc())
    offset = (page - 1) * per_page
    total = query.count()

    reseñas = query.offset(offset).limit(per_page).all()
    total_pages = (total + per_page - 1) // per_page if total > 0 else 1
    has_prev = page > 1
    has_next = page < total_pages
    return {
        "reseñas": reseñas,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": total_pages,
        "has_prev": has_prev,
        "has_next": has_next,
    }


def aprobar_reseña(reseña_id, usuario_moderador_id):
    reseña = obtener_reseña_por_id(reseña_id)

    if not reseña or not reseña.puede_ser_moderada:
        return False, "Reseña no encontrada o ya procesada"

    try:
        reseña.estado = EstadoReseña.APROBADA
        reseña.fecha_moderacion = datetime.now(timezone.utc)
        reseña.usuario_moderador_id = usuario_moderador_id
        reseña.motivo_rechazo = None

        db.session.commit()
        return True, "Reseña aprobada exitosamente"
    except Exception as e:
        db.session.rollback()
        return False, f"Error al aprobar reseña: {str(e)}"


def create_reseña(comentario, calificacion, sitio_id, email_usuario, nombre_usuario):
    reseña = Reseña(
        comentario=comentario,
        calificacion=calificacion,
        sitio_id=sitio_id,
        email_usuario=email_usuario,
        nombre_usuario=nombre_usuario,
    )

    db.session.add(reseña)
    db.session.commit()

    return reseña


def rechazar_reseña(reseña_id, usuario_moderador_id, motivo_rechazo):
    reseña = obtener_reseña_por_id(reseña_id)

    if not reseña or not reseña.puede_ser_moderada:
        return False, "Reseña no encontrada o ya procesada"

    try:
        reseña.estado = EstadoReseña.RECHAZADA
        reseña.fecha_moderacion = datetime.now(timezone.utc)
        reseña.usuario_moderador_id = usuario_moderador_id
        reseña.motivo_rechazo = motivo_rechazo

        db.session.commit()

        return True, "Reseña rechazada exitosamente"

    except Exception as e:
        db.session.rollback()
        return False, f"Error al rechazar reseña: {str(e)}"


def eliminar_reseña(reseña_id):
    reseña = obtener_reseña_por_id(reseña_id)

    if not reseña:
        return False, "Reseña no encontrada"

    try:
        db.session.delete(reseña)
        db.session.commit()
        return True, "Reseña eliminada exitosamente"
    except Exception as e:
        db.session.rollback()
        return False, f"Error al eliminar reseña: {str(e)}"


def obtener_estadisticas_reseñas():
    total = db.session.query(Reseña).count()
    pendientes = (
        db.session.query(Reseña).filter(Reseña.estado == EstadoReseña.PENDIENTE).count()
    )
    aprobadas = (
        db.session.query(Reseña).filter(Reseña.estado == EstadoReseña.APROBADA).count()
    )
    rechazadas = (
        db.session.query(Reseña).filter(Reseña.estado == EstadoReseña.RECHAZADA).count()
    )

    from sqlalchemy import func

    promedio_calificacion = (
        db.session.query(func.avg(Reseña.calificacion))
        .filter(Reseña.estado == EstadoReseña.APROBADA)
        .scalar()
    )

    return {
        "total": total,
        "pendientes": pendientes,
        "aprobadas": aprobadas,
        "rechazadas": rechazadas,
        "promedio_calificacion": (
            round(promedio_calificacion, 2) if promedio_calificacion else 0
        ),
    }


def crear_reseña_ejemplo():
    from src.models.sitios.sitio_historico import SitioHistorico

    sitio = db.session.query(SitioHistorico).first()

    if not sitio:
        return None

    reseña = Reseña(
        comentario="no me gusto.",
        calificacion=2,
        sitio_id=sitio.id,
        email_usuario="visitante@example.com",
        nombre_usuario="María García",
    )

    db.session.add(reseña)
    db.session.commit()
    return reseña
