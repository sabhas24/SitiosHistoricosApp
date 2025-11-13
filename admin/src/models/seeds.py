from src.models.auth import (
    create_role,
    create_permission,
    assign_permission_to_role,
    user_new,
    user_index,
)
from sqlalchemy.exc import IntegrityError

from src.models.database import db


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






def run():
    print("🛠️  Seeding database (paradigma: roles fijos admin/user)")

  
    admin_role = create_role("admin")
    editor_role = create_role("editor")
    user_role = create_role("user")

    for perm in ADMIN_PERMISSIONS:
        create_permission(perm)
        assign_permission_to_role("admin", perm)

    for perm in EDITOR_PERMISSIONS:
        create_permission(perm)
        assign_permission_to_role("editor", perm)

    from src.models.feature_flag.feature_flag_services import create_default_feature_flags
    create_default_feature_flags()
    from src.models.propuestas.propuesta_services import crear_propuesta_ejemplo
    from src.models.reseñas.reseña_services import crear_reseña_ejemplo
    
    try:
        crear_propuesta_ejemplo()
        print("✅ Propuesta de ejemplo creada")
    except Exception as e:
        print(f"⚠️  Error al crear propuesta de ejemplo: {e}")
    
    try:
        crear_reseña_ejemplo()
        print("✅ Reseña de ejemplo creada")
    except Exception as e:
        print(f"⚠️  Error al crear reseña de ejemplo: {e}")

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
            "password": "user123",
            "role_id": editor_role.id,
        },
        {
            "email": "ana@example.com",
            "name": "Ana",
            "last_name": "López",
            "password": "demo123",
            "role_id": editor_role.id,
        },
        {
            "email": "carlos@example.com",
            "name": "Carlos",
            "last_name": "García",
            "password": "demo123",
            "role_id": editor_role.id,
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


