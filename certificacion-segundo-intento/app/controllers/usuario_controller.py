# app/controllers/usuario_controller.py
from flask import Blueprint, render_template, redirect, request, session, flash
from app.models.usuario import Usuario

usuario_bp = Blueprint('usuario', __name__)

# Página inicio (registro/login)
@usuario_bp.route('/')
def index():
    return render_template('index.html')

# Crear usuario (registro)
@usuario_bp.route('/register', methods=['POST'])
def crear_usuario():
    if not Usuario.validar_registro(request.form):
        return redirect('/')
    data = {
        'nombre': request.form['nombre'].strip(),
        'apellido': request.form['apellido'].strip(),
        'email': request.form['email'].strip().lower(),
        'password': request.form['password']
    }
    resultado = Usuario.guardar(data)
    if resultado:
        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
    else:
        flash('Error al crear la cuenta. Inténtalo nuevamente.', 'registro')
    return redirect('/')

# Login
@usuario_bp.route('/login', methods=['POST'])
def login_usuario():
    if not Usuario.validar_login(request.form):
        return redirect('/')
    email = request.form['email'].strip().lower()
    password = request.form['password']
    usuario = Usuario.obtener_por_email({'email': email})
    if not usuario or not usuario.verificar_password(password):
        flash('Email o contraseña incorrectos.', 'login')
        return redirect('/')
    session['user_id'] = usuario.id
    session['user_nombre'] = usuario.nombre
    flash(f'¡Bienvenido {usuario.nombre}!', 'success')
    return redirect('/dashboard')

# Logout
@usuario_bp.route('/logout')
def cerrar_sesion():
    session.clear()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect('/')
