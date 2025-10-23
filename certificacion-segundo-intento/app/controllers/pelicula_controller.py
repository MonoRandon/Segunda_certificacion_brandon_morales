# app/controllers/pelicula_controller.py
from flask import Blueprint, render_template, redirect, request, session, flash
from app.models.pelicula import Pelicula
from app.models.usuario import Usuario
from app.models.comentario import Comentario
from datetime import date

pelicula_bp = Blueprint('peliculas', __name__)

# Dashboard con listado de películas
@pelicula_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página.', 'error')
        return redirect('/')
    
    usuario_actual = Usuario.obtener_por_id({'id': session['user_id']})
    peliculas = Pelicula.obtener_todas()
    # marcar si el usuario actual es creador de cada película
    for pelicula in peliculas:
        pelicula['es_creador'] = pelicula['usuario_id'] == session['user_id']
    return render_template('dashboard.html', usuario=usuario_actual, peliculas=peliculas)

# Formulario para crear nueva película (solo sesión)

@pelicula_bp.route('/nueva/pelicula')
def nueva_pelicula():
    if 'usuario_id' not in session:
        return redirect('/logout')
    return render_template('nueva_pelicula.html', fecha_actual=date.today().isoformat())


# Crear película (POST)
@pelicula_bp.route('/crear', methods=['POST'])
def crear_pelicula():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para realizar esta acción.', 'error')
        return redirect('/')
    form = request.form
    # Validar (incluye título único)
    if not Pelicula.validar_pelicula(form, check_unique=True):
        # Mantener datos llenados por usuario (sinopsis no se restablece)
        return render_template('agregar_pelicula.html', form_data=form)
    data = {
        'titulo': form['titulo'].strip(),
        'director': form['director'].strip(),
        'sinopsis': form['sinopsis'].strip(),
        'fecha': form['fecha'],
        'usuario_id': session['user_id']
    }
    resultado = Pelicula.guardar(data)
    if resultado:
        flash('Película creada exitosamente.', 'success')
        return redirect('/dashboard')
    else:
        flash('Error al crear la película. Inténtalo nuevamente.', 'error')
        return render_template('agregar_pelicula.html', form_data=form)

# Ver página individual de película, con comentarios
@pelicula_bp.route('/ver/<int:pelicula_id>')
def ver_pelicula(pelicula_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para ver los detalles de la película.', 'error')
        return redirect('/')

    pelicula = Pelicula.obtener_por_id({'id': pelicula_id})
    if not pelicula:
        flash('Película no encontrada.', 'error')
        return redirect('/dashboard')

    usuario_actual = Usuario.obtener_por_id({'id': session['user_id']})
    comentarios = Comentario.obtener_por_pelicula(pelicula_id)  # ya ordenados DESC por fecha
    pelicula['es_creador'] = pelicula['usuario_id'] == session['user_id']

    return render_template('ver_pelicula.html', pelicula=pelicula, usuario=usuario_actual, comentarios=comentarios)

# Form editar (solo creador)
@pelicula_bp.route('/editar/<int:pelicula_id>')
def editar_pelicula_form(pelicula_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página.', 'error')
        return redirect('/')
    if not Pelicula.es_creador(session['user_id'], pelicula_id):
        flash('Solo el creador de la película puede editarla.', 'error')
        return redirect('/dashboard')
    pelicula = Pelicula.obtener_por_id({'id': pelicula_id})
    if not pelicula:
        flash('Película no encontrada.', 'error')
        return redirect('/dashboard')
    return render_template('editar_pelicula.html', pelicula=pelicula, form_data=None)

# Actualizar película (POST)
@pelicula_bp.route('/actualizar/<int:pelicula_id>', methods=['POST'])
def actualizar_pelicula(pelicula_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para realizar esta acción.', 'error')
        return redirect('/')
    if not Pelicula.es_creador(session['user_id'], pelicula_id):
        flash('Solo el creador de la película puede editarla.', 'error')
        return redirect('/dashboard')

    form = request.form
    # pasar pelicula_id para permitir mantener mismo título si no cambia
    if not Pelicula.validar_pelicula(form, check_unique=True, pelicula_id=pelicula_id):
        pelicula = Pelicula.obtener_por_id({'id': pelicula_id})
        return render_template('editar_pelicula.html', pelicula=pelicula, form_data=form)

    data = {
        'id': pelicula_id,
        'titulo': form.get('titulo').strip(),
        'director': form.get('director').strip(),
        'sinopsis': form.get('sinopsis').strip(),
        'fecha': form.get('fecha')
    }
    resultado = Pelicula.actualizar(data)
    if resultado:
        flash('Película actualizada exitosamente.', 'success')
    else:
        flash('Error al actualizar la película.', 'error')
    return redirect('/dashboard')

# Borrar película (POST) — solo creador
@pelicula_bp.route('/borrar/<int:pelicula_id>', methods=['POST'])
def borrar_pelicula(pelicula_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para realizar esta acción.', 'error')
        return redirect('/')
    if not Pelicula.es_creador(session['user_id'], pelicula_id):
        flash('Solo el creador de la película puede eliminarla.', 'error')
        return redirect('/dashboard')
    resultado = Pelicula.borrar({'id': pelicula_id})
    if resultado:
        flash('Película eliminada exitosamente.', 'success')
    else:
        flash('Error al eliminar la película.', 'error')
    return redirect('/dashboard')
