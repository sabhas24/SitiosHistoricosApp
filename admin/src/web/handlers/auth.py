from flask import session, redirect, url_for, flash
from functools import wraps

def is_authenticated() :
    return session.get('user') is not None  

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            flash('Por favor, inicia sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function