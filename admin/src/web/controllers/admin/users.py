from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.models.auth import user
from src.models.database import db
from src.models import auth
from src.web.handlers.auth import login_required, check
from src.web.validators.user_validator import validate_user_create_data, validate_user_update_data

bp = Blueprint('admin_users', __name__, url_prefix='/admin/users')

@bp.route('/', methods=['GET'])
@login_required
@check('user_index')
def index():
    page=request.args.get('page', 1, type=int)
    users, total = auth.user_paginate(page=page)
    return render_template('admin/users/index.html', users=users, total=total, page=page)

@bp.route('/filter', methods=['POST'])
@login_required
@check('user_index') 
def filter_users():
   
    page = request.form.get('page', 1, type=int)
    filter_type = request.form.get('filter_type', 'mail')
    date_order = request.form.get('date_order', 'desc')

    users, total = auth.user_paginate(
        page=page,
        filter_type=filter_type, 
        date_order=date_order
    )
    return render_template('admin/users/components/_table.html', users=users, total=total, page=page)
                        
@bp.route('/find/<string:email>', methods=['GET'])
@login_required
@check('user_show')
def find_user(email):
    user = auth.user_show(email)
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('admin_users.index'))
    return render_template('admin/users/index.html', users=[user], total=1, page=1)
@bp.route('/nuevo', methods=['GET'])
@login_required
@check('user_new')
def create_form():
    return render_template('admin/users/form.html', user=None)

@bp.route('/nuevo', methods=['POST'])
@login_required
@check('user_new')
def create():
    
    form_data = {
        'email': request.form.get('email'),
        'name': request.form.get('name'),
        'last_name': request.form.get('last_name'),
        'role': request.form.get('role'),
        'password': request.form.get('password'),
        'confirm_password': request.form.get('confirm_password')
    }
    
    validation_errors = validate_user_create_data(form_data)
    if validation_errors:
        for error in validation_errors:
            flash(error, 'error')
        return redirect(url_for('admin_users.create_form'))
    
    
    if form_data['email'] and auth.email_exists(form_data['email']):
        flash('El email ya está en uso', 'error')
        return redirect(url_for('admin_users.create_form'))


    auth.user_new(
        email=form_data['email'], 
        name=form_data['name'], 
        last_name=form_data['last_name'],  
        password=form_data['password'], 
        role_id=form_data['role'], 
       
    )
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

   
    form_data = {
        'email': request.form.get('email'),
        'name': request.form.get('name'),
        'last_name': request.form.get('last_name'),
        'role': request.form.get('role'),
        'new_password': request.form.get('new_password'),
        'confirm_new_password': request.form.get('confirm_new_password')
    }
    
   
    validation_errors = validate_user_update_data(form_data)
    if validation_errors:
        for error in validation_errors:
            flash(error, 'error')
        return redirect(url_for('admin_users.edit_form', user_id=user_id))
    
    
    if (form_data['email'] and 
        form_data['email'] != user.email and 
        auth.email_exists(form_data['email'])):
        flash('El email ya está en uso por otro usuario', 'error')
        return redirect(url_for('admin_users.edit_form', user_id=user_id))

   
    update_data = {
        'email': form_data['email'],
        'name': form_data['name'],
        'last_name': form_data['last_name'],
        'role_id': form_data['role'],
        'is_super_admin': bool(request.form.get('is_super_admin')),
        'enabled': bool(request.form.get('enabled'))
    }
    
    
    if form_data['new_password']:
        update_data['password'] = form_data['new_password']

    auth.user_update(user.id, **update_data)
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
    if user.is_super_admin or (user.role.name == 'admin'):
        flash('Los administradores no pueden ser eliminados', 'error')
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
    if user.is_super_admin or (user.role.name == 'admin'):
        flash('Los administradores no pueden ser bloqueados', 'error')
        return redirect(url_for('admin_users.index'))
    auth.user_update(user.id, enabled=not user.enabled)
    estado = "bloqueado" if not user.enabled else "desbloqueado"
    flash(f"Usuario {estado} correctamente", "success")
    return redirect(url_for('admin_users.index'))