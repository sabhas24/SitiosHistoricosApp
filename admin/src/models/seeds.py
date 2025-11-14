from src.models.auth import (
    create_role,
    create_permission,
    assign_permission_to_role,
    user_new,
    user_index,
)
from sqlalchemy.exc import IntegrityError

from src.models.database import db, Base
from sqlalchemy import inspect, text


ADMIN_PERMISSIONS = [
    "user_index",
    "user_show",
    "user_new",
    "user_update",
    "user_destroy",
    "user_block",
    "site_index",
    "site_new",
    "site_show",
    "site_update",
    "site_destroy",
    "site_export",
    "site_set_visibility",
    "proposal_validate",
    "review_moderate"
]


EDITOR_PERMISSIONS = [
    "site_index",
    "site_new",
    "site_show",
    "site_update",
    "site_destroy",
    "site_export",
    "site_set_visibility",
    "proposal_validate",
    "review_moderate"
]






def _ensure_tables():
    """Crea las tablas si aún no existen (idempotente)."""
    # Importar modelos para registrar metadatos
    from src.models.auth.user import user
    from src.models.auth.role import Role
    from src.models.auth.permission import Permission
    from src.models.auth.associations import role_permissions
    from src.models.sitios.sitio_historico import SitioHistorico
    from src.models.tags.tag import Tag, sitio_tag
    from src.models.reseñas.reseña import Reseña
    from src.models.favoritos.favoritos import Favorito
    from src.models.propuestas.propuesta_sitio import PropuestaSitio
    from src.models.historial.historial import HistorialSitio
    from src.models.feature_flag.feature_flag import FeatureFlag

    # Asegurar extensión PostGIS (necesaria para columnas Geometry)
    try:
        with db.engine.begin() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis_topology"))
    except Exception as e:
        print(f"⚠️  No se pudo crear la extensión PostGIS: {e}")

    inspector = inspect(db.engine)
    tables = set(inspector.get_table_names())
    # Si falta alguna tabla clave, crear todo
    required = {"roles", "permissions", "users"}
    if not required.issubset(tables):
        Base.metadata.create_all(bind=db.engine)


def run():
    
    _ensure_tables()
    
    # Crear roles
    admin_role = create_role("admin")
    editor_role = create_role("editor")
    public_role = create_role("public_user")
    
    # Permisos públicos
    PUBLIC_PERMISSIONS = [
        "site_show",
        "review_create",
        "favorite_manage",
    ]
    
    # Asignar permisos a public_user
    for perm_name in PUBLIC_PERMISSIONS:
        create_permission(perm_name)
        assign_permission_to_role("public_user", perm_name)
    
    for perm in ADMIN_PERMISSIONS:
        create_permission(perm)
        assign_permission_to_role("admin", perm)

    for perm in EDITOR_PERMISSIONS:
        create_permission(perm)
        assign_permission_to_role("editor", perm)

    from src.models.feature_flag.feature_flag_services import create_default_feature_flags
    create_default_feature_flags()
    
    # Crear sitios históricos de ejemplo primero
    print("📍 Creando sitios históricos de ejemplo...")
    try:
        crear_sitios_ejemplo()
        print("✅ Sitios históricos de ejemplo creados")
    except Exception as e:
        print(f"⚠️  Error al crear sitios de ejemplo: {e}")
    
    # Luego crear propuestas y reseñas
    from src.models.propuestas.propuesta_services import crear_propuesta_ejemplo
    from src.models.reseñas.reseña_services import crear_reseña_ejemplo
    
    try:
        crear_propuesta_ejemplo()
        print("✅ Propuesta de ejemplo creada")
    except Exception as e:
        print(f"⚠️  Error al crear propuesta de ejemplo: {e}")
    
    try:
        crear_reseñas_y_favoritos_ejemplo()
        print("✅ Reseñas y favoritos de ejemplo creados")
    except Exception as e:
        print(f"⚠️  Error al crear reseñas y favoritos de ejemplo: {e}")

    demo_users = [
        {
            "email": "admin@admin.com",
            "name": "Admin",
            "last_name": "Root",
            "password": "admin123",
            "role_id": admin_role.id,
        },
        {
            "email": "superadmin@admin.com",
            "name": "Super",
            "last_name": "Admin",
            "password": "super123",
            "role_id": admin_role.id,
            "is_super_admin": True,
        },
        {
            "email": "user@user.com",
            "name": "Usuario",
            "last_name": "Final",
            "password": "user1234",
            "role_id": editor_role.id,
        },
        {
            "email": "ana@example.com",
            "name": "Ana",
            "last_name": "López",
            "password": "demo1234",
            "role_id": editor_role.id,
        },
        {
            "email": "carlos@example.com",
            "name": "Carlos",
            "last_name": "García",
            "password": "demo1234",
            "role_id": public_role.id,
        },
    ]

    existing_emails = {u.email for u in user_index()}
    for data in demo_users:
        if data["email"] in existing_emails:
            print(f"⏭️  Usuario ya existe: {data['email']}")
            continue
        try:
            user_new(**data)
        except IntegrityError:
            db.session.rollback()
            print(f"⚠️  Conflicto al crear usuario: {data['email']}")

    print("📊 Resumen seeding:")
    print(f"  Roles: admin, editor")
    print(f"  Permisos admin: {len(ADMIN_PERMISSIONS)}")
    print(f"  Permisos editor:  {len(EDITOR_PERMISSIONS)}")
    print("  Usuarios actuales:")
    for u in user_index():
        print(f"   - {u.email} (role_id={u.role_id})")

    print("✅ Seeding completed")


def crear_sitios_ejemplo():
    """Crear sitios históricos de ejemplo para testing"""
    from src.models.sitios.sitio_historico import SitioHistorico, EstadoConservacion, Categoria
    from src.models.tags.tag import Tag
    
    # Verificar si ya existen sitios
    if db.session.query(SitioHistorico).count() > 0:
        print("⏭️  Ya existen sitios históricos")
        return
    
    # Crear tags
    tags_dict = {}
    for tag_nombre in ["Colonial", "Arquitectura", "Histórico", "Turístico", "Patrimonio", "Cultural"]:
        tag = db.session.query(Tag).filter_by(nombre=tag_nombre).first()
        if not tag:
            tag = Tag(nombre=tag_nombre)
            db.session.add(tag)
            db.session.flush()
        tags_dict[tag_nombre] = tag
    
    sitios_ejemplo = [
        {
            "nombre": "Cabildo de Buenos Aires",
            "descripcion_breve": "Edificio colonial que fue sede del gobierno durante la época virreinal",
            "descripcion_completa": "El Cabildo de Buenos Aires es uno de los pocos edificios coloniales que se conservan en la ciudad. Fue sede del gobierno colonial y testigo de importantes acontecimientos históricos como la Revolución de Mayo de 1810.",
            "ciudad": "Buenos Aires",
            "provincia": "Buenos Aires",
            "latitud": -34.6083,
            "longitud": -58.3725,
            "estado_conservacion": EstadoConservacion.BUENO,
            "anio_inauguracion": 1751,
            "categoria": Categoria.EDIFICIO_HISTORICO,
            "visible": True,
            "tags": [tags_dict["Colonial"], tags_dict["Histórico"], tags_dict["Turístico"]]
        },
        {
            "nombre": "Casa Rosada",
            "descripcion_breve": "Sede del Poder Ejecutivo de Argentina",
            "descripcion_completa": "La Casa Rosada es la sede del Poder Ejecutivo de la República Argentina. Su característico color rosa la hace inconfundible. Desde su balcón se han dado importantes discursos históricos.",
            "ciudad": "Buenos Aires",
            "provincia": "Buenos Aires",
            "latitud": -34.6075,
            "longitud": -58.3702,
            "estado_conservacion": EstadoConservacion.BUENO,
            "anio_inauguracion": 1898,
            "categoria": Categoria.EDIFICIO_HISTORICO,
            "visible": True,
            "tags": [tags_dict["Arquitectura"], tags_dict["Histórico"], tags_dict["Turístico"]]
        },
        {
            "nombre": "Teatro Colón",
            "descripcion_breve": "Uno de los teatros de ópera más importantes del mundo",
            "descripcion_completa": "El Teatro Colón es considerado uno de los cinco mejores teatros de ópera del mundo por su acústica excepcional y su belleza arquitectónica. Inaugurado en 1908, es un ícono cultural de Buenos Aires.",
            "ciudad": "Buenos Aires",
            "provincia": "Buenos Aires",
            "latitud": -34.6010,
            "longitud": -58.3833,
            "estado_conservacion": EstadoConservacion.BUENO,
            "anio_inauguracion": 1908,
            "categoria": Categoria.ARQUITECTURA,
            "visible": True,
            "tags": [tags_dict["Arquitectura"], tags_dict["Cultural"], tags_dict["Patrimonio"]]
        },
        {
            "nombre": "Ruinas de San Ignacio Miní",
            "descripcion_breve": "Ruinas de una antigua misión jesuítica guaraní",
            "descripcion_completa": "Las ruinas de San Ignacio Miní son los restos de una de las misiones jesuíticas guaraníes fundadas en el siglo XVII. Declaradas Patrimonio de la Humanidad por la UNESCO, son un testimonio de la evangelización en América del Sur.",
            "ciudad": "San Ignacio",
            "provincia": "Misiones",
            "latitud": -27.2678,
            "longitud": -55.5350,
            "estado_conservacion": EstadoConservacion.REGULAR,
            "anio_inauguracion": 1632,
            "categoria": Categoria.SITIO_ARQUEOLOGICO,
            "visible": True,
            "tags": [tags_dict["Histórico"], tags_dict["Patrimonio"], tags_dict["Turístico"]]
        },
        {
            "nombre": "Monumento a la Bandera",
            "descripcion_breve": "Monumento nacional en honor a la bandera argentina",
            "descripcion_completa": "El Monumento Nacional a la Bandera se encuentra en Rosario, ciudad donde Manuel Belgrano izó por primera vez la bandera argentina. Es un complejo arquitectónico que incluye una torre de 70 metros de altura.",
            "ciudad": "Rosario",
            "provincia": "Santa Fe",
            "latitud": -32.9474,
            "longitud": -60.6395,
            "estado_conservacion": EstadoConservacion.BUENO,
            "anio_inauguracion": 1957,
            "categoria": Categoria.MONUMENTO,
            "visible": True,
            "tags": [tags_dict["Histórico"], tags_dict["Turístico"], tags_dict["Patrimonio"]]
        }
    ]
    
    for sitio_data in sitios_ejemplo:
        tags = sitio_data.pop('tags')
        latitud = sitio_data.pop('latitud')
        longitud = sitio_data.pop('longitud')
        
        # Crear el punto geográfico con SRID=4326
        sitio = SitioHistorico(
            **sitio_data,
            ubicacion=f'SRID=4326;POINT({longitud} {latitud})'
        )
        sitio.tags = tags
        db.session.add(sitio)
    
    db.session.commit()
    print(f"✅ Creados {len(sitios_ejemplo)} sitios históricos de ejemplo")


def crear_reseñas_y_favoritos_ejemplo():
    """Crear reseñas y favoritos de ejemplo para testing"""
    from src.models.reseñas.reseña import Reseña
    from src.models.favoritos.favoritos import Favorito
    from src.models.sitios.sitio_historico import SitioHistorico
    from src.models.auth.user import user
    
    # Obtener sitios y usuarios
    sitios = db.session.query(SitioHistorico).limit(3).all()
    usuarios = db.session.query(user).filter(user.email.in_(['user@user.com', 'ana@example.com', 'carlos@example.com'])).all()
    
    if not sitios:
        print("⚠️  No hay sitios para crear reseñas")
        return
    
    # Crear reseñas de ejemplo
    reseñas_ejemplo = [
        {
            "comentario": "Lugar increíble, muy bien conservado. La visita guiada fue excelente y aprendimos mucho sobre la historia.",
            "calificacion": 5,
            "sitio_id": sitios[0].id,
            "email_usuario": "visitante1@example.com",
            "nombre_usuario": "María García"
        },
        {
            "comentario": "Interesante desde el punto de vista histórico, pero le falta mantenimiento en algunas áreas.",
            "calificacion": 3,
            "sitio_id": sitios[0].id,
            "email_usuario": "visitante2@example.com",
            "nombre_usuario": "Juan Pérez"
        },
    ]
    
    if len(sitios) > 1:
        reseñas_ejemplo.extend([
            {
                "comentario": "Un lugar emblemático que todos deberían visitar. La arquitectura es impresionante.",
                "calificacion": 5,
                "sitio_id": sitios[1].id,
                "email_usuario": "turista@example.com",
                "nombre_usuario": "Laura Fernández"
            },
            {
                "comentario": "Muy lindo, pero hay mucha gente. Recomiendo ir temprano.",
                "calificacion": 4,
                "sitio_id": sitios[1].id,
                "email_usuario": "viajero@example.com",
                "nombre_usuario": "Carlos Rodríguez"
            }
        ])
    
    for reseña_data in reseñas_ejemplo:
        reseña = Reseña(**reseña_data)
        db.session.add(reseña)
    
    # Crear favoritos de ejemplo
    if usuarios and sitios:
        try:
            # Usuario 1 tiene 2 favoritos
            if len(usuarios) > 0 and len(sitios) > 0:
                fav1 = Favorito(user_id=usuarios[0].id, sitio_id=sitios[0].id)
                db.session.add(fav1)
                if len(sitios) > 1:
                    fav2 = Favorito(user_id=usuarios[0].id, sitio_id=sitios[1].id)
                    db.session.add(fav2)
            
            # Usuario 2 tiene 1 favorito
            if len(usuarios) > 1 and len(sitios) > 1:
                fav3 = Favorito(user_id=usuarios[1].id, sitio_id=sitios[1].id)
                db.session.add(fav3)
            
            # Usuario 3 tiene 1 favorito
            if len(usuarios) > 2 and len(sitios) > 2:
                fav4 = Favorito(user_id=usuarios[2].id, sitio_id=sitios[2].id)
                db.session.add(fav4)
        except Exception as e:
            print(f"⚠️  Error al crear favoritos: {e}")
    
    db.session.commit()
    print(f"✅ Creadas {len(reseñas_ejemplo)} reseñas de ejemplo")
    print("✅ Creados favoritos de ejemplo")


