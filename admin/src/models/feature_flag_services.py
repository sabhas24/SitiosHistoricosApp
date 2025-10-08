from src.models.database import db
from src.models.feature_flag import FeatureFlag
from flask import session
from sqlalchemy.exc import IntegrityError

def get_all_feature_flags():
    """Obtener todos los feature flags"""
    return db.session.query(FeatureFlag).order_by(FeatureFlag.name).all()

def get_feature_flag_by_name(name):
    """Obtener un feature flag por nombre"""
    return db.session.query(FeatureFlag).filter_by(name=name).first()

def is_feature_enabled(name):
    """Verificar si un feature flag está habilitado"""
    flag = get_feature_flag_by_name(name)
    return flag.is_enabled if flag else False

def get_maintenance_message(flag_name):
    """Obtener el mensaje de mantenimiento de un flag"""
    flag = get_feature_flag_by_name(flag_name)
    return flag.maintenance_message if flag and flag.is_enabled else None

def update_feature_flag(name, is_enabled, maintenance_message=None):
    """Actualizar un feature flag"""
    try:
        # Obtener el usuario actual
        user_email = session.get('user')
        if not user_email:
            return False, "Usuario no autenticado"
        
        flag = get_feature_flag_by_name(name)
        if not flag:
            return False, f"Feature flag '{name}' no encontrado"
        
        # Validaciones
        if is_enabled and name in ['admin_maintenance_mode', 'portal_maintenance_mode']:
            if not maintenance_message or not maintenance_message.strip():
                return False, "El mensaje de mantenimiento es obligatorio cuando se activa el modo de mantenimiento"
            
            if len(maintenance_message) > 500:
                return False, "El mensaje de mantenimiento no puede exceder 500 caracteres"
        
        # Actualizar el flag
        flag.is_enabled = is_enabled
        flag.maintenance_message = maintenance_message.strip() if maintenance_message else None
        flag.last_modified_by = user_email
        
        db.session.commit()
        
        print(f"✅ Feature flag '{name}' actualizado: {'ON' if is_enabled else 'OFF'} por {user_email}")
        return True, "Feature flag actualizado correctamente"
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error al actualizar feature flag: {str(e)}")
        return False, f"Error al actualizar: {str(e)}"

def create_default_feature_flags():
    """Crear los feature flags por defecto si no existen"""
    try:
        # Obtener usuario del sistema para la creación inicial
        system_user = "system@admin.com"
        
        default_flags = [
            {
                'name': 'admin_maintenance_mode',
                'description': 'Modo mantenimiento de administración - Deshabilita temporalmente el sitio de administración',
                'is_enabled': False,
                'maintenance_message': None,
                'last_modified_by': system_user
            },
            {
                'name': 'portal_maintenance_mode',
                'description': 'Modo mantenimiento de portal web - Deshabilita temporalmente el portal público',
                'is_enabled': False,
                'maintenance_message': None,
                'last_modified_by': system_user
            },
            {
                'name': 'reviews_enabled',
                'description': 'Permitir nuevas reseñas - Habilita/deshabilita creación y visualización de reseñas',
                'is_enabled': True,
                'maintenance_message': None,
                'last_modified_by': system_user
            }
        ]
        
        for flag_data in default_flags:
            existing_flag = get_feature_flag_by_name(flag_data['name'])
            if not existing_flag:
                flag = FeatureFlag(**flag_data)
                db.session.add(flag)
                print(f"✅ Feature flag creado: {flag_data['name']}")
        
        db.session.commit()
        return True
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error al crear feature flags por defecto: {str(e)}")
        return False

def is_admin_maintenance_active():
    """Verificar si el modo de mantenimiento de administración está activo"""
    return is_feature_enabled('admin_maintenance_mode')

def is_portal_maintenance_active():
    """Verificar si el modo de mantenimiento del portal está activo"""
    return is_feature_enabled('portal_maintenance_mode')

def are_reviews_enabled():
    """Verificar si las reseñas están habilitadas"""
    return is_feature_enabled('reviews_enabled')
