from flask import Blueprint, request, jsonify, abort, render_template, session, redirect, url_for, flash
from src.models.tag import Tag
from src.models.database import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, desc
from src.web.handlers.auth import login_required, check

bp = Blueprint('tags', __name__, url_prefix='/tags')

# Los permisos ahora se manejan con el decorador @check

@bp.route('', methods=['GET'])
@login_required
def list_tags():
    page = int(request.args.get('page', 1))
    per_page = 25
    search = request.args.get('search', '').strip()
    order = request.args.get('order', 'nombre')
    direction = request.args.get('direction', 'asc')

    query = db.session.query(Tag)
    if search:
        query = query.filter(Tag.nombre.ilike(f'%{search}%'))
    if order == 'nombre':
        query = query.order_by(asc(Tag.nombre) if direction == 'asc' else desc(Tag.nombre))
    elif order == 'created_at':
        query = query.order_by(asc(Tag.created_at) if direction == 'asc' else desc(Tag.created_at))

    total = query.count()
    tags = query.offset((page - 1) * per_page).limit(per_page).all()
    pages = (total + per_page - 1) // per_page
    return render_template('tags/index.html', tags=tags, total=total, page=page, pages=pages)

@bp.route('/nuevo')
@login_required
@check('tag_new')
def nuevo():
    return render_template('tags/form.html', action='crear', tag=None)

@bp.route('/crear', methods=['POST'])
@login_required
@check('tag_new')
def crear():
    nombre = request.form.get('nombre', '').strip()
    if not nombre or len(nombre) < 3 or len(nombre) > 50:
        flash('El nombre debe tener entre 3 y 50 caracteres.', 'danger')
        return render_template('tags/form.html', action='crear', tag=None)
    
    # Verificar unicidad case-insensitive
    existing = db.session.query(Tag).filter(Tag.nombre.ilike(nombre)).first()
    if existing:
        flash('Ya existe una etiqueta con ese nombre (sin distinguir mayúsculas/minúsculas).', 'danger')
        return render_template('tags/form.html', action='crear', tag=None)
    
    tag = Tag(nombre)
    db.session.add(tag)
    try:
        db.session.commit()
        flash('Etiqueta creada correctamente.', 'success')
        return redirect(url_for('tags.list_tags'))
    except IntegrityError:
        db.session.rollback()
        flash('El nombre o slug ya existe.', 'danger')
        return render_template('tags/form.html', action='crear', tag=None)

@bp.route('/<int:tag_id>/editar')
@login_required
@check('tag_update')
def editar(tag_id):
    tag = db.session.get(Tag, tag_id)
    if not tag:
        flash('Etiqueta no encontrada.', 'danger')
        return redirect(url_for('tags.list_tags'))
    return render_template('tags/form.html', action='editar', tag=tag)

@bp.route('/<int:tag_id>/actualizar', methods=['POST'])
@login_required
@check('tag_update')
def actualizar(tag_id):
    tag = db.session.get(Tag, tag_id)
    if not tag:
        flash('Etiqueta no encontrada.', 'danger')
        return redirect(url_for('tags.list_tags'))
    nombre = request.form.get('nombre', '').strip()
    if not nombre or len(nombre) < 3 or len(nombre) > 50:
        flash('El nombre debe tener entre 3 y 50 caracteres.', 'danger')
        return render_template('tags/form.html', action='editar', tag=tag)
    
    # Verificar unicidad case-insensitive (excluyendo el tag actual)
    existing = db.session.query(Tag).filter(
        Tag.nombre.ilike(nombre),
        Tag.id != tag_id
    ).first()
    if existing:
        flash('Ya existe otra etiqueta con ese nombre (sin distinguir mayúsculas/minúsculas).', 'danger')
        return render_template('tags/form.html', action='editar', tag=tag)
    
    tag.nombre = nombre
    tag.slug = Tag.generate_slug(nombre)
    try:
        db.session.commit()
        flash('Etiqueta actualizada correctamente.', 'success')
        return redirect(url_for('tags.list_tags'))
    except IntegrityError:
        db.session.rollback()
        flash('El nombre o slug ya existe.', 'danger')
        return render_template('tags/form.html', action='editar', tag=tag)

@bp.route('/<int:tag_id>', methods=['DELETE'])
@login_required
@check('tag_destroy')
def delete_tag(tag_id):
    tag = db.session.get(Tag, tag_id)
    if not tag:
        return jsonify({'error': 'Tag no encontrado.'}), 404
    if tag.sitios:
        return jsonify({'error': 'No se puede eliminar el tag porque está asignado a uno o más sitios.'}), 400
    db.session.delete(tag)
    db.session.commit()
    return jsonify({'result': 'Tag eliminado.'})

@bp.route('/<int:tag_id>/ver')
@login_required
def ver(tag_id):
    tag = db.session.get(Tag, tag_id)
    if not tag:
        flash('Etiqueta no encontrada.', 'danger')
        return redirect(url_for('tags.list_tags'))
    return render_template('tags/detalle.html', tag=tag)

@bp.route('/<int:tag_id>/borrar', methods=['POST'])
@login_required
@check('tag_destroy')
def borrar(tag_id):
    tag = db.session.get(Tag, tag_id)
    if not tag:
        flash('Etiqueta no encontrada.', 'danger')
        return redirect(url_for('tags.list_tags'))
    if tag.sitios:
        flash('No se puede eliminar el tag porque está asignado a uno o más sitios.', 'danger')
        return redirect(url_for('tags.list_tags'))
    db.session.delete(tag)
    db.session.commit()
    flash('Etiqueta eliminada correctamente.', 'success')
    return redirect(url_for('tags.list_tags'))
