from flask import request, session, render_template, redirect, url_for
from src.models.feature_flag_services import (
    is_admin_maintenance_active, 
    get_maintenance_message,
    is_portal_maintenance_active
)
from src.models.auth import user_show

def check_maintenance_mode():
    """Middleware para verificar modo de mantenimiento"""
    
    # Verificar si estamos en el portal público (no implementado aún)
    if is_portal_maintenance_active():
        # Este se implementará en la etapa 2
        pass
    
    # Verificar modo de mantenimiento de administración
    if is_admin_maintenance_active():
        # Rutas excluidas del bloqueo (siempre permitidas)
        excluded_routes = ['auth.login', 'auth.authenticate', 'auth.logout', 'static']
        
        if request.endpoint in excluded_routes:
            return None  # Permitir acceso a rutas de autenticación
        
        # Obtener usuario actual
        user_email = session.get('user')
        current_user = None
        
        if user_email:
            current_user = user_show(user_email)
        
        # Permitir acceso solo a System Admins
        if not current_user or not current_user.is_super_admin:
            maintenance_message = get_maintenance_message('admin_maintenance_mode')
            return render_template(
                'maintenance.html', 
                message=maintenance_message,
                is_admin_maintenance=True
            ), 503
    
    return None  # Continuar normalmente
