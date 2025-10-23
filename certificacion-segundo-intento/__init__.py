from flask import Flask
from app.controllers.usuario_controller import usuario_bp
from app.controllers.pelicula_controller import pelicula_bp
from app.controllers.comentario_controller import comentario_bp
import os

def create_app():
    ruta_templates = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'templates')
    ruta_static = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static')
    
    app = Flask(__name__, template_folder=ruta_templates, static_folder=ruta_static)
    app.secret_key = 'clavesupermegaincreiblementesegura'
    
    # Registrar blueprints
    app.register_blueprint(usuario_bp)
    app.register_blueprint(pelicula_bp)
    app.register_blueprint(comentario_bp)

    return app
