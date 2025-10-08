from src.models.database import db
from src.models.auth.user import user  # ORM model (lowercase name kept from existing code)
from src.models.auth.role import Role
from src.models.auth.permission import Permission
from src.models.auth.permissions_enum import  permiso_valido
from werkzeug.security import generate_password_hash, check_password_hash

def permission(user_obj):
    """Return a list of permission names for the given user instance.

    Rules:
    - If user is None -> empty list.
    - Else -> permission names attached to the user's role.
    """
    if user_obj is None:
        return []
    if not getattr(user_obj, 'role', None):
        return []
    return [p.name for p in user_obj.role.permissions]

def user_new(**kwargs):
    print(" 📝Creating a new user with the following details:")
    if 'password' in kwargs:
        kwargs['password'] = generate_password_hash(kwargs['password'])
    new= user(**kwargs)
    db.session.add(new)
    db.session.commit()
    print(f" ✅ User created with ID: {new.id}")
    return new
def user_is_blocked(email):
    user_obj = db.session.query(user).filter_by(email=email).first()
    if user_obj:
        return not user_obj.enabled
    return False

def user_check_password(email, password):
    user_obj=db.session.query(user).filter_by(email=email).first()
    if user_obj and check_password_hash(user_obj.password, password):
        print(f" ✅ Password for user '{email}' is correct.")
        return True
    print(f" ❌ Password for user '{email}' is incorrect or user does not exist.")
    return False

def user_index():
    return db.session.query(user).all()

def user_update(id, **kwargs):
    print(f" 📝Updating user with ID: {id}, {kwargs}")
    user_obj = db.session.get(user, id)
    for key, value in kwargs.items():
        setattr(user_obj, key, value)
    db.session.commit()
    print(f" ✅ User updated: {user_obj}")
    return user_obj
def user_detroy(id):
    print(f" 📝Deleting user with ID: {id}")
    user_obj = db.session.get(user, id)
    if not user_obj:
        print(f" ❌ User with ID {id} not found")
        return False
    db.session.delete(user_obj)
    db.session.commit()
    print(f" ✅ User deleted")
    return True
def user_show(email):
    user_obj = db.session.query(user).filter_by(email=email).first()
    if not user_obj:
        print(f" ❌ User with email {email} not found")
        return None
    return user_obj
def email_exists(email: str) -> bool:
    user_obj = db.session.query(user).filter_by(email=email).first()
    return user_obj is not None




def user_paginate(page=1, filter_type='mail', date_order='desc'):
    """Return a paginated list of users, filtered and ordered.

    Args:
        page (int): Page number (1-based).
        filter_type (str): Filter type ( 'mail', 'role', 'active').
        date_order (str): 'asc' or 'desc' for ordering by creation date.

    Returns:
        List[user], total_count
    """
    per_page = 25
    users_query = db.session.query(user)
    
    
  
    match filter_type:
        case 'mail':
            users_query = users_query.order_by(user.name.asc())
        case 'admin':
            users_query = users_query.filter(user.role.has(name='admin')).order_by(user.id.asc())
        case 'editor':
            users_query = users_query.filter(user.role.has(name='editor')).order_by(user.id.asc())
        case 'active':
            users_query = users_query.filter(user.enabled == True).order_by(user.id.asc())
        case 'inactive':
            users_query = users_query.filter(user.enabled == False).order_by(user.id.asc()  )
    match date_order:
        case 'asc': 
            users_query = users_query.order_by(user.inserted_at.asc()) 
        case 'desc':
            users_query = users_query.order_by(user.inserted_at.desc())
        
    total = users_query.count()
    return users_query.offset((page - 1) * per_page).limit(per_page).all(), total

def user_show_id(user_id):
    user_obj = db.session.get(user, user_id)
    if not user_obj:
        print(f" ❌ User with ID {user_id} not found")
        return None
    return user_obj



def create_role(name):
    print(f" 📝Creating role: {name}")
    role = Role(name=name)
    db.session.add(role)
    db.session.commit()
    print(f" ✅ Role created with ID: {role.id} {role.name}")
    return role

def create_permission(name):
    if not permiso_valido(name):
        raise ValueError(f"❌ Permission '{name}' no permitido (debe existir en Enum Permisos)")
    existing = db.session.query(Permission).filter_by(name=name).first()
    if existing:
        print(f" ℹ️ Permission '{name}' ya existe (ID {existing.id})")
        return existing
    print(f" 📝Creating permission: {name}")
    permission = Permission(name=name)
    db.session.add(permission)
    db.session.commit()
    print(f" ✅ Permission created with ID: {permission.id}")
    return permission

def assign_permission_to_role(role_name, perm_name):
    if not permiso_valido(perm_name):
        raise ValueError(f"❌ Permission '{perm_name}' no permitido (Enum Permisos)")
    print(f" 📝Assigning permission '{perm_name}' to role '{role_name}'")
    role = db.session.query(Role).filter_by(name=role_name).first()
    if not role:
        raise ValueError(f"Rol '{role_name}' no encontrado")
    perm = db.session.query(Permission).filter_by(name=perm_name).first()
    if not perm:
        perm = create_permission(perm_name)
    if perm in role.permissions:
        print(f" ℹ️ Role '{role_name}' ya tiene '{perm_name}'")
        return False
    role.permissions.append(perm)
    db.session.commit()
    print(f" ✅ Permission '{perm_name}' assigned to role '{role_name}'")
    return True

