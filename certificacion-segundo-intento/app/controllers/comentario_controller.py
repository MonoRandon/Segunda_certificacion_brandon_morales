# app/controllers/comentario_controller.py
from flask import Blueprint, request, redirect, session, flash
from app.models.comentario import Comentario
from app.models.pelicula import Pelicula

comentario_bp = Blueprint('comentario_bp', __name__)

# Ruta para agregar comentario a una película
@comentario_bp.route('/comentar/<int:pelicula_id>', methods=['POST'])
def comentar(pelicula_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para comentar.', 'error')
        return redirect('/')

    contenido = request.form.get('contenido', '').strip()
    pelicula = Pelicula.obtener_por_id({'id': pelicula_id})

    if not pelicula:
        flash('Película no encontrada.', 'error')
        return redirect('/dashboard')

    # Evita que el creador comente su propia película
    if pelicula['usuario_id'] == session['user_id']:
        flash('No puedes comentar tu propia película.', 'error')
        return redirect(f'/ver/{pelicula_id}')

    if not contenido or len(contenido) < 3:
        flash('El comentario debe tener al menos 3 caracteres.', 'error')
        return redirect(f'/ver/{pelicula_id}')

    Comentario.guardar({
        'pelicula_id': pelicula_id,
        'usuario_id': session['user_id'],
        'contenido': contenido
    })
    flash('Comentario agregado correctamente.', 'success')
    return redirect(f'/ver/{pelicula_id}')

# Ruta para eliminar comentario (solo dueño del comentario)
@comentario_bp.route('/eliminar_comentario/<int:comentario_id>', methods=['POST'])
def eliminar_comentario(comentario_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para eliminar un comentario.', 'error')
        return redirect('/')

    comentario = Comentario.obtener_por_id({'id': comentario_id})
    if not comentario:
        flash('Comentario no encontrado.', 'error')
        return redirect('/dashboard')

    # Solo el creador del comentario puede eliminarlo (requisito BONUS)
    if comentario['usuario_id'] != session['user_id']:
        flash('No tienes permiso para eliminar este comentario.', 'error')
        return redirect(f'/ver/{comentario["pelicula_id"]}')

    Comentario.eliminar({'id': comentario_id})
    flash('Comentario eliminado correctamente.', 'success')
    return redirect(f'/ver/{comentario["pelicula_id"]}')
