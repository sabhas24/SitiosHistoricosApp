from flask import Blueprint, url_for
from flask import render_template,request,redirect,flash,session
from flask_session import Session
from src.models.auth import  user_check_password
from src.web.handlers.auth import  login_required

bp=Blueprint  ('auth', __name__, url_prefix='/auth')

@bp.get('/')
def login():
    return render_template('auth/login.html')
 
@bp.post('/authenticate')
def authenticate():
    params=request.form
    if user_check_password(params.get('username'), params.get('password')):
        flash('Usuario autenticado con éxito!', 'success')
        session['user'] = params.get('username')
        return redirect(url_for('home'))
    else:
        flash('Usuario o contraseña incorrectos', 'error')
        return redirect(url_for('auth.login'))

@bp.get('/logout')
@login_required
def logout():
    if session.get('user'):
        session.pop('user')
        session.clear()
        flash('Sesión cerrada con éxito', 'success')
    else:
        flash('No hay sesión activa', 'info')   
    return redirect(url_for('auth.login'))


