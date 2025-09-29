from flask import session, redirect, url_for, flash
from functools import wraps
from src.models.database import db
from src.models.auth.user import user
from src.models.auth.role import Role
from src.models.auth.permission import Permission

def get_current_user():
    """Obtiene el usuario actual desde la sesión"""
    if not session.get('user'):
        return None
    
    return db.session.query(user).filter_by(email=session['user']).first()

def user_has_role(role_name):
    """Verifica si el usuario actual tiene un rol específico"""
    current_user = get_current_user()
    if not current_user:
        return False
    
    return current_user.role.name.lower() == role_name.lower()

def user_has_permission(permission_name):
    """Verifica si el usuario actual tiene un permiso específico"""
    current_user = get_current_user()
    if not current_user:
        return False
    
    # Verificar si el rol del usuario tiene el permiso
    for permission in current_user.role.permissions:
        if permission.name.lower() == permission_name.lower():
            return True
    
    return False

def is_admin():
    """Verifica si el usuario actual es administrador"""
    return user_has_role('administrador')

def is_editor():
    """Verifica si el usuario actual es editor"""
    return user_has_role('editor')

def is_editor_or_admin():
    """Verifica si el usuario actual es editor o administrador"""
    return is_editor() or is_admin()

def can_create_sitios():
    """Verifica si el usuario puede crear sitios históricos"""
    return is_editor_or_admin()

def can_edit_sitios():
    """Verifica si el usuario puede editar sitios históricos"""
    return is_editor_or_admin()

def can_delete_sitios():
    """Verifica si el usuario puede eliminar sitios históricos"""
    return is_admin()

# Decoradores para proteger rutas
def require_role(role_name):
    """Decorador que requiere un rol específico"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('user'):
                flash('Por favor, inicia sesión para acceder a esta página.', 'warning')
                return redirect(url_for('auth.login'))
            
            if not user_has_role(role_name):
                flash(f'No tienes permisos para acceder a esta página. Se requiere rol: {role_name}', 'error')
                return redirect(url_for('home'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_permission(permission_name):
    """Decorador que requiere un permiso específico"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('user'):
                flash('Por favor, inicia sesión para acceder a esta página.', 'warning')
                return redirect(url_for('auth.login'))
            
            if not user_has_permission(permission_name):
                flash(f'No tienes permisos para realizar esta acción. Se requiere: {permission_name}', 'error')
                return redirect(url_for('home'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_editor_or_admin(f):
    """Decorador que requiere ser editor o administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            flash('Por favor, inicia sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not is_editor_or_admin():
            flash('No tienes permisos para acceder a esta página. Se requiere ser Editor o Administrador.', 'error')
            return redirect(url_for('home'))
        
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    """Decorador que requiere ser administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            flash('Por favor, inicia sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not is_admin():
            flash('No tienes permisos para acceder a esta página. Se requiere ser Administrador.', 'error')
            return redirect(url_for('home'))
        
        return f(*args, **kwargs)
    return decorated_function