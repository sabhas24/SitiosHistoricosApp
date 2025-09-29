from src.models.auth import create_permission, create_role, assign_permission_to_role, user_new
from src.models.database import db

def run():
    print("🛠️  Seeding the database with initial data...")
    
    # 1. Crear permisos
    print("📝 Creating permissions...")
    permissions = ["lectura", "escritura", "eliminacion"]
    
    for perm_name in permissions:
        create_permission(perm_name)
    
    # 2. Crear roles
    print("👥 Creating roles...")
    user_role = create_role("usuario publico")
    editor_role = create_role("editor") 
    admin_role = create_role("administrador")
    
    # 3. Asignar permisos a roles
    print("🔗 Assigning permissions...")
    
    # Administrador: todos los permisos
    for perm_name in permissions:
        assign_permission_to_role("administrador", perm_name)
    
    # Editor: lectura y escritura (no eliminación)
    assign_permission_to_role("editor", "lectura")
    assign_permission_to_role("editor", "escritura")
    
    # Usuario público: solo lectura
    assign_permission_to_role("usuario publico", "lectura")
    
    # 4. Crear usuarios de prueba
    print("👤 Creating users...")
    
    # Administrador
    user_new(
        email="admin@admin.com",
        name="Admin",
        password="admin123",
        last_name="Sistema",
        role_id=admin_role.id
    )
    
    # Editor
    user_new(
        email="editor@editor.com",
        name="María",
        password="editor123",
        last_name="González",
        role_id=editor_role.id
    )
    
    # Usuario público
    user_new(
        email="user@user.com",
        name="Juan",
        password="user123",
        last_name="Pérez",
        role_id=user_role.id
    )
    
    
