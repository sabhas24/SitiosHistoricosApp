from math import perm
from os import abort
from flask import session, redirect, url_for, flash,abort
from functools import wraps
from src.models import auth

def is_authenticated() :
    return session.get('user') is not None

def get_current_user():
    """Obtiene el usuario actual desde la sesión"""
    user_email = session.get('user')
    if user_email:
        return auth.user_show(user_email)
    return None  

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            flash('Por favor, inicia sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
def check_permission(permission_name):
    user_email = session.get('user')
    user = auth.user_show(user_email)
    permissions = auth.permission(user)
    return user is not None and permission_name in permissions

def check(permission_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            
            if not check_permission(permission_name):
               return abort(403)  
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator