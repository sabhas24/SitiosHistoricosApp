from src.models.auth import create_permission, create_role, assign_permission_to_role, user_new
from src.models.database import db

def run():
    print("🛠️  Seeding the database with initial data...")
    
    # 1. Crear permisos
    print("📝 Creating permissions...")
    permissions = ["lectura", "escritura"]
    
    for perm_name in permissions:
        create_permission(perm_name)
    
    # 2. Crear roles
    print("👥 Creating roles...")
    admin_role = create_role("Administrador")
    operator_role = create_role("Operador")
    user_role = create_role("Usuario")
    
    # 3. Asignar permisos a roles
    print("🔗 Assigning permissions...")
    
    # Admin: todos los permisos
    for perm_name in permissions:
        assign_permission_to_role("Administrador", perm_name)
    
    # Operador: lectura y escritura
    for perm_name in permissions:
        assign_permission_to_role("Operador", perm_name)
    
    # Usuario: solo lectura
    assign_permission_to_role("Usuario", "lectura")
    
    # 4. Crear usuarios
    print("👤 Creating users...")
    user_new(
        email="admin@patrimonioba.com",
        name="Admin",
        password="admin123",
        last_name="Sistema",
        role_id=admin_role.id
    )
    
    user_new(
        email="operador@patrimonioba.com",
        name="María",
        password="operador123",
        last_name="González",
        role_id=operator_role.id
    )
    
    user_new(
        email="usuario@patrimonioba.com",
        name="Juan",
        password="usuario123",
        last_name="Pérez",
        role_id=user_role.id
    )
    
    
