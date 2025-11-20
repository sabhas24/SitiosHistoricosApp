from flask import session, redirect, url_for, flash, abort, current_app
from functools import wraps
from src.models import auth

def is_authenticated():
    print(f"Checking session. Session data: {dict(session)}")
    if not session.get('user'):
        return False
    return True

def get_current_user():
    user_email = session.get('user')
    if user_email:
        return auth.user_show(user_email)
    return None  

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            session.clear()
            flash('Tu sesión ha expirado. Por favor, inicia sesión nuevamente.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
def check_permission(permission_name):
    user_email = session.get('user')
    user = auth.user_show(user_email)
    if user.is_super_admin:
        return True
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

def get_session_info():
    if not session.get('user'):
        return None
        
    lifetime = current_app.config.get('PERMANENT_SESSION_LIFETIME')
    if lifetime and session.permanent:
        hours = lifetime.total_seconds() / 3600
        return {
            'user': session.get('user'),
            'expires_in_hours': hours,
            'permanent': session.permanent
        }
    
    return {
        'user': session.get('user'),
        'permanent': session.permanent
    }