from flask import Blueprint, render_template, flash, redirect, url_for
from src.web.handlers.auth import login_required, get_current_user

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/')
@login_required
def view_profile():
    """Ver perfil del usuario actual"""
    current_user = get_current_user()
    if not current_user:
        flash('Error al obtener información del usuario', 'error')
        return redirect(url_for('home'))
    
    return render_template('profile/view.html', user=current_user)
