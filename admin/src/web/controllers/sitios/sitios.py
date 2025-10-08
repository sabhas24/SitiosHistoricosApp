from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, make_response
from src.models.sitios import (
    sitio_create, sitio_index, sitio_show, sitio_update, sitio_delete,
    sitio_get_coordinates, get_search_options, sitio_export_csv
)
from src.models.sitios.sitio_historico import EstadoConservacion, Categoria
from src.models.tags.tag import Tag
from src.web.handlers.auth import login_required, check
from src.models.database import db

bp = Blueprint('sitios', __name__, url_prefix='/sitios')

@bp.route('/')
@login_required
@check('site_index')
def index():
    """Listar sitios históricos con paginación y búsqueda avanzada"""
    # Obtener número de página
    page = request.args.get('page', 1, type=int)
    
    # Obtener filtros de búsqueda
    filters = {}
    
    # Búsqueda por texto
    if request.args.get('search'):
        filters['search'] = request.args.get('search').strip()
    
    # Filtros de ubicación
    if request.args.get('ciudad'):
        filters['ciudad'] = request.args.get('ciudad').strip()
    
    if request.args.get('provincia'):
        filters['provincia'] = request.args.get('provincia')
    
    # Filtros de características
    if request.args.get('categoria'):
        filters['categoria'] = request.args.get('categoria')
    
    if request.args.get('estado_conservacion'):
        filters['estado_conservacion'] = request.args.get('estado_conservacion')
    
    # Filtro por tags
    if request.args.getlist('tags'):
        filters['tags'] = request.args.getlist('tags')
    
    # Filtro de visibilidad
    visible = request.args.get('visible')
    if visible == 'true':
        filters['visible'] = True
    elif visible == 'false':
        filters['visible'] = False
    
    # Filtros de fecha
    if request.args.get('fecha_desde'):
        filters['fecha_desde'] = request.args.get('fecha_desde')
    
    if request.args.get('fecha_hasta'):
        filters['fecha_hasta'] = request.args.get('fecha_hasta')
    
    # Orden
    if request.args.get('order_by'):
        filters['order_by'] = request.args.get('order_by')
    
    if request.args.get('order_dir'):
        filters['order_dir'] = request.args.get('order_dir')
    
    # Obtener datos paginados con filtros
    pagination_data = sitio_index(page=page, per_page=25, filters=filters)
    
    # Obtener opciones para los selectores
    search_options = get_search_options()
    
    return render_template('sitios/index.html', 
                         search_options=search_options,
                         **pagination_data)

@bp.route('/nuevo')
@login_required
@check('site_new')
def nuevo():
    """Formulario para crear nuevo sitio histórico"""
    estados = [estado.value for estado in EstadoConservacion]
    categorias = [categoria.value for categoria in Categoria]
    tags_all = db.session.query(Tag).order_by(Tag.nombre).all()
    return render_template('sitios/form.html', 
                         estados=estados, 
                         categorias=categorias,
                         tags_all=tags_all,
                         action='crear')

@bp.route('/crear', methods=['POST'])
@login_required
@check('site_new')
def crear():
    """Crear nuevo sitio histórico"""
    try:
        # Obtener datos del formulario
        data = {
            'nombre': request.form.get('nombre'),
            'descripcion_breve': request.form.get('descripcion_breve'),
            'descripcion_completa': request.form.get('descripcion_completa'),
            'ciudad': request.form.get('ciudad'),
            'provincia': request.form.get('provincia'),
            'latitud': request.form.get('latitud'),
            'longitud': request.form.get('longitud'),
            'estado_conservacion': request.form.get('estado_conservacion'),
            'anio_inauguracion': request.form.get('anio_inauguracion'),
            'categoria': request.form.get('categoria'),
            'visible': request.form.get('visible') == 'on',
            'tags': request.form.getlist('tags')
        }
        
        # Validaciones básicas
        if not data['nombre'] or not data['descripcion_breve']:
            flash('Nombre y descripción breve son obligatorios', 'error')
            return redirect(url_for('sitios.nuevo'))
        
        if not data['latitud'] or not data['longitud']:
            flash('Las coordenadas son obligatorias', 'error')
            return redirect(url_for('sitios.nuevo'))
        
        # Convertir año a entero si se proporciona
        if data['anio_inauguracion']:
            try:
                data['anio_inauguracion'] = int(data['anio_inauguracion'])
            except ValueError:
                flash('El año de inauguración debe ser un número válido', 'error')
                return redirect(url_for('sitios.nuevo'))
        else:
            data['anio_inauguracion'] = None
        
        sitio = sitio_create(**data)
        flash(f'Sitio histórico "{sitio.nombre}" creado exitosamente', 'success')
        return redirect(url_for('sitios.index'))
        
    except Exception as e:
        flash(f'Error al crear el sitio histórico: {str(e)}', 'error')
        return redirect(url_for('sitios.nuevo'))

@bp.route('/<int:id>')
@login_required
@check('site_show')
def detalle(id):
    """Ver detalles de un sitio histórico"""
    sitio = sitio_show(id)
    if not sitio:
        flash('Sitio histórico no encontrado', 'error')
        return redirect(url_for('sitios.index'))
    
    # Obtener coordenadas
    latitud, longitud = sitio_get_coordinates(sitio)
    
    return render_template('sitios/detalle.html', 
                         sitio=sitio, 
                         latitud=latitud, 
                         longitud=longitud)

@bp.route('/<int:id>/editar')
@login_required
@check('site_update')
def editar(id):
    """Formulario para editar sitio histórico"""
    sitio = sitio_show(id)
    if not sitio:
        flash('Sitio histórico no encontrado', 'error')
        return redirect(url_for('sitios.index'))
    
    # Obtener coordenadas
    latitud, longitud = sitio_get_coordinates(sitio)
    
    estados = [estado.value for estado in EstadoConservacion]
    categorias = [categoria.value for categoria in Categoria]
    tags_all = db.session.query(Tag).order_by(Tag.nombre).all()
    
    return render_template('sitios/form.html', 
                         sitio=sitio,
                         latitud=latitud,
                         longitud=longitud,
                         estados=estados, 
                         categorias=categorias,
                         tags_all=tags_all,
                         action='editar')

@bp.route('/<int:id>/actualizar', methods=['POST'])
@login_required
@check('site_update')
def actualizar(id):
    """Actualizar sitio histórico"""
    try:
        # Obtener datos del formulario
        data = {
            'nombre': request.form.get('nombre'),
            'descripcion_breve': request.form.get('descripcion_breve'),
            'descripcion_completa': request.form.get('descripcion_completa'),
            'ciudad': request.form.get('ciudad'),
            'provincia': request.form.get('provincia'),
            'latitud': request.form.get('latitud'),
            'longitud': request.form.get('longitud'),
            'estado_conservacion': request.form.get('estado_conservacion'),
            'anio_inauguracion': request.form.get('anio_inauguracion'),
            'categoria': request.form.get('categoria'),
            'visible': request.form.get('visible') == 'on',
            'tags': request.form.getlist('tags')
        }
        
        # Validaciones básicas
        if not data['nombre'] or not data['descripcion_breve']:
            flash('Nombre y descripción breve son obligatorios', 'error')
            return redirect(url_for('sitios.editar', id=id))
        
        if not data['latitud'] or not data['longitud']:
            flash('Las coordenadas son obligatorias', 'error')
            return redirect(url_for('sitios.editar', id=id))
        
        # Convertir año a entero si se proporciona
        if data['anio_inauguracion']:
            try:
                data['anio_inauguracion'] = int(data['anio_inauguracion'])
            except ValueError:
                flash('El año de inauguración debe ser un número válido', 'error')
                return redirect(url_for('sitios.editar', id=id))
        else:
            data['anio_inauguracion'] = None
        
        sitio = sitio_update(id, **data)
        if sitio:
            flash(f'Sitio histórico "{sitio.nombre}" actualizado exitosamente', 'success')
            return redirect(url_for('sitios.detalle', id=id))
        else:
            flash('Sitio histórico no encontrado', 'error')
            return redirect(url_for('sitios.index'))
        
    except Exception as e:
        flash(f'Error al actualizar el sitio histórico: {str(e)}', 'error')
        return redirect(url_for('sitios.editar', id=id))

@bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@check('site_destroy')
def eliminar(id):
    """Eliminar sitio histórico"""
    try:
        if sitio_delete(id):
            flash('Sitio histórico eliminado exitosamente', 'success')
        else:
            flash('Sitio histórico no encontrado', 'error')
    except Exception as e:
        flash(f'Error al eliminar el sitio histórico: {str(e)}', 'error')
    
    return redirect(url_for('sitios.index'))

@bp.route('/exportar-csv')
@login_required
@check('site_export')
def exportar_csv():
    """Exportar sitios históricos a CSV"""
    import csv
    import io
    from datetime import datetime
    
    try:
        # Obtener los mismos filtros que en index
        filters = {}
        
        # Búsqueda por texto
        if request.args.get('search'):
            filters['search'] = request.args.get('search').strip()
        
        # Filtros de ubicación
        if request.args.get('ciudad'):
            filters['ciudad'] = request.args.get('ciudad').strip()
        
        if request.args.get('provincia'):
            filters['provincia'] = request.args.get('provincia')
        
        # Filtros de características
        if request.args.get('categoria'):
            filters['categoria'] = request.args.get('categoria')
        
        if request.args.get('estado_conservacion'):
            filters['estado_conservacion'] = request.args.get('estado_conservacion')
        
        # Filtro por tags
        if request.args.getlist('tags'):
            filters['tags'] = request.args.getlist('tags')
        
        # Filtro de visibilidad
        visible = request.args.get('visible')
        if visible == 'true':
            filters['visible'] = True
        elif visible == 'false':
            filters['visible'] = False
        
        # Filtros de fecha
        if request.args.get('fecha_desde'):
            filters['fecha_desde'] = request.args.get('fecha_desde')
        
        if request.args.get('fecha_hasta'):
            filters['fecha_hasta'] = request.args.get('fecha_hasta')
        
        # Orden
        if request.args.get('order_by'):
            filters['order_by'] = request.args.get('order_by')
        
        if request.args.get('order_dir'):
            filters['order_dir'] = request.args.get('order_dir')
        
        # Obtener sitios con filtros aplicados
        sitios = sitio_export_csv(filters)
        
        if not sitios:
            flash('No hay datos para exportar', 'warning')
            return redirect(url_for('sitios.index'))
        
        # Crear archivo CSV en memoria
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Escribir cabeceras
        writer.writerow([
            'ID',
            'Nombre',
            'Descripción Breve',
            'Ciudad',
            'Provincia',
            'Estado de Conservación',
            'Fecha de Registro',
            'Latitud',
            'Longitud',
            'Tags Asociados'
        ])
        
        # Escribir datos
        for sitio in sitios:
            # Obtener coordenadas
            latitud, longitud = sitio_get_coordinates(sitio)
            
            # Obtener tags como texto separado por punto y coma
            tags_texto = '; '.join([tag.nombre for tag in sitio.tags]) if sitio.tags else ''
            
            writer.writerow([
                sitio.id,
                sitio.nombre,
                sitio.descripcion_breve,
                sitio.ciudad,
                sitio.provincia,
                sitio.estado_conservacion.value if sitio.estado_conservacion else '',
                sitio.fecha_registro.strftime('%Y-%m-%d %H:%M:%S') if sitio.fecha_registro else '',
                f"{latitud:.6f}" if latitud else '',
                f"{longitud:.6f}" if longitud else '',
                tags_texto
            ])
        
        # Crear respuesta
        output.seek(0)
        csv_data = output.getvalue()
        output.close()
        
        # Generar nombre del archivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        filename = f'sitios_{timestamp}.csv'
        
        # Crear respuesta HTTP
        response = make_response(csv_data)
        response.headers['Content-Type'] = 'text/csv; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
        
    except Exception as e:
        flash(f'Error al exportar CSV: {str(e)}', 'error')
        return redirect(url_for('sitios.index'))