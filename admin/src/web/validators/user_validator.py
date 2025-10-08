"""
Validaciones del lado del servidor para usuarios
"""
import re
from typing import Dict, List, Optional


def validate_email(email: str) -> Optional[str]:
    """Valida formato de email"""
    if not email:
        return "El email es requerido"
    
    if len(email) > 120:
        return "El email no puede tener más de 120 caracteres"
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return "El formato del email no es válido"
    
    return None


def validate_name(name: str, field_name: str = "nombre") -> Optional[str]:
    """Valida formato de nombre o apellido"""
    if not name:
        return f"El {field_name} es requerido"
    
    name = name.strip()
    
    if len(name) < 2:
        return f"El {field_name} debe tener al menos 2 caracteres"
    
    if len(name) > 80:
        return f"El {field_name} no puede tener más de 80 caracteres"
    
    pattern = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$'
    if not re.match(pattern, name):
        return f"El {field_name} solo puede contener letras y espacios"
    
    return None


def validate_password(password: str, confirm_password: Optional[str] = None) -> Optional[str]:
    """Valida formato de contraseña"""
    if not password:
        return "La contraseña es requerida"
    
    if len(password) < 8:
        return "La contraseña debe tener al menos 8 caracteres"
    
    if len(password) > 200:
        return "La contraseña no puede tener más de 200 caracteres"
    
    # Al menos una minúscula, una mayúscula y un número
    if not re.search(r'[a-z]', password):
        return "La contraseña debe contener al menos una letra minúscula"
    
    if not re.search(r'[A-Z]', password):
        return "La contraseña debe contener al menos una letra mayúscula"
    
    if not re.search(r'\d', password):
        return "La contraseña debe contener al menos un número"
    
    # Verificar confirmación si se proporciona
    if confirm_password is not None and password != confirm_password:
        return "Las contraseñas no coinciden"
    
    return None


def validate_user_data(data: Dict) -> List[str]:
    """
    Valida todos los datos de usuario y retorna lista de errores
    
    Args:
        data: Diccionario con los datos del usuario
        
    Returns:
        Lista de mensajes de error (vacía si todo es válido)
    """
    errors = []
    
    # Validar email
    email_error = validate_email(data.get('email', ''))
    if email_error:
        errors.append(email_error)
    
    # Validar nombre
    name_error = validate_name(data.get('name', ''), 'nombre')
    if name_error:
        errors.append(name_error)
    
    # Validar apellido (opcional)
    last_name = data.get('last_name', '').strip()
    if last_name:  # Solo validar si no está vacío
        lastname_error = validate_name(last_name, 'apellido')
        if lastname_error:
            errors.append(lastname_error)
    
    # Validar contraseña (solo si se proporciona)
    password = data.get('password')
    if password:  # Para creación o cambio de contraseña
        confirm_password = data.get('confirm_password')
        password_error = validate_password(password, confirm_password)
        if password_error:
            errors.append(password_error)
    
    # Validar nueva contraseña (para edición)
    new_password = data.get('new_password')
    if new_password:
        confirm_new_password = data.get('confirm_new_password')
        new_password_error = validate_password(new_password, confirm_new_password)
        if new_password_error:
            errors.append(f"Nueva contraseña: {new_password_error}")
    
    # Validar rol
    role = data.get('role')
    if not role:
        errors.append("Debe seleccionar un rol")
    else:
        try:
            role_id = int(role)
            if role_id not in [1, 2]:  # 1=Admin, 2=Editor
                errors.append("El rol seleccionado no es válido")
        except ValueError:
            errors.append("El rol seleccionado no es válido")
    
    return errors


def validate_user_create_data(data: Dict) -> List[str]:
    """Validación específica para creación de usuario"""
    errors = validate_user_data(data)
    
   
    if not data.get('password'):
        errors.append("La contraseña es requerida para crear un usuario")
    
    return errors


def validate_user_update_data(data: Dict) -> List[str]:
    """Validación específica para actualización de usuario"""
    return validate_user_data(data)