from flask import Blueprint, url_for
from flask import render_template,request,redirect,flash
from flask_session import Session
from src.models.auth import  user_check_password
bp=Blueprint  ('auth', __name__, url_prefix='/auth')

@bp.get('/')
def login():
    return render_template('auth/login.html')

@bp.get('/logout')
def logout():
    pass


@bp.post('/authenticate')
def authenticate():
    params=request.form
    if user_check_password(params.get('username'), params.get('password')):
        flash('Usuario autenticado con éxito!', 'success')
        Session['user'] = params.get('username')
        return redirect(url_for('layout'))
    else:
        flash('Usuario o contraseña incorrectos', 'error')
        return redirect(url_for('auth.login'))