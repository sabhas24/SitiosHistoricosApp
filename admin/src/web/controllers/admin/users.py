from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.models.database import db
from src.models import auth
from src.web.handlers.auth import login_required, check

bp = Blueprint('admin_users', __name__, url_prefix='/admin/users')

@bp.route('/', methods=['GET'])
@login_required
@check('user_index')
def index():
    users= auth.user_index()
    page=request.args.get('page', 1, type=int)
    usersVista= users[(page-1)*25 : page*25]  
    return render_template('admin/users/index.html', users=usersVista, page=page)
@bp.route('/nuevo', methods=['GET'])
@login_required
@check('user_new')
def create_form():
    return render_template('admin/users/form.html', user=None)
@bp.route('/nuevo', methods=['POST'])
@login_required
@check('user_new')
def create():
    email=request.form.get('email')
    name=request.form.get('name')
    last_name=request.form.get('last_name')
    role=request.form.get('role')
    is_super_admin= bool(request.form.get('is_super_admin'))
    password=request.form.get('password')
    if not email or not name or not password:
        flash('Todos los campos son obligatorios', 'error')
        return redirect(url_for('admin_users.create_form'))
    
    
    if auth.email_exists(email):
        flash('El email ya está en uso', 'error')
        return redirect(url_for('admin_users.create_form'))

    auth.user_new(email=email, name=name, last_name=last_name,  password=password, role_id=role, is_super_admin=is_super_admin)
    flash('Usuario creado exitosamente', 'success')
    return redirect(url_for('admin_users.index'))

@bp.route('/<int:user_id>/editar', methods=['GET'])
@login_required
@check('user_update')
def edit_form(user_id):
    user = db.session.get(auth.user, user_id)
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('admin_users.index'))
    return render_template('admin/users/form.html', user=user)

@bp.route('/<int:user_id>/editar', methods=['POST'])
@login_required
@check('user_update')
def edit(user_id):
    user = db.session.get(auth.user, user_id)
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('admin_users.index'))

    email = request.form.get('email')
    name = request.form.get('name')
    last_name = request.form.get('last_name')
    role = request.form.get('role')
    is_super_admin = bool(request.form.get('is_super_admin'))
    enabled = bool(request.form.get('enabled'))

    auth.user_update(user.id, email=email, name=name, last_name=last_name, role_id=role, is_super_admin=is_super_admin, enabled=enabled)
    flash('Usuario actualizado exitosamente', 'success')
    return redirect(url_for('admin_users.index'))

@bp.route('/<int:user_id>/eliminar', methods=['POST'])
@login_required
@check('user_destroy')
def delete(user_id):
    user = db.session.get(auth.user, user_id)
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('admin_users.index'))
   
    auth.user_detroy(user.id)
    flash("Usuario eliminado correctamente", "success")
    return redirect(url_for('admin_users.index'))

@bp.route('/<int:user_id>/bloquear', methods=['POST'])
@login_required
@check('user_block')
def block(user_id):
    user = db.session.get(auth.user, user_id)
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('admin_users.index'))
    auth.user_update(user.id, enabled=not user.enabled)
    estado = "bloqueado" if not user.enabled else "desbloqueado"
    flash(f"Usuario {estado} correctamente", "success")
    return redirect(url_for('admin_users.index'))