# app/models/usuario.py
from app.config.mysqlconnection import MySQLConnection
from flask import flash
import bcrypt
import re

class Usuario:
    def __init__(self, data):
        self.id = data.get('id')
        self.nombre = data.get('nombre')
        self.apellido = data.get('apellido')
        self.email = data.get('email')
        self.password = data.get('password')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    # Guardar usuario (registro)
    @classmethod
    def guardar(cls, data):
        password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        query = """
        INSERT INTO usuarios (nombre, apellido, email, password) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);
        """
        data_con_hash = {
            'nombre': data['nombre'],
            'apellido': data['apellido'],
            'email': data['email'],
            'password': password_hash
        }
        try:
            return MySQLConnection('certificacion_brandon_morales').query_db(query, data_con_hash)
        except Exception as e:
            """ERROR AL GUARDAR USUARIO: {}""".format(e)
            return False

    # Obtener por email (para login)
    @classmethod
    def obtener_por_email(cls, data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = MySQLConnection('certificacion_brandon_morales').query_db(query, data)
        return cls(resultado[0]) if resultado else None

    # Obtener por id
    @classmethod
    def obtener_por_id(cls, data):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        resultado = MySQLConnection('certificacion_brandon_morales').query_db(query, data)
        return cls(resultado[0]) if resultado else None

    # Actualizar usuario
    @classmethod
    def actualizar(cls, data):
        query = "UPDATE usuarios SET nombre=%(nombre)s, apellido=%(apellido)s, email=%(email)s WHERE id=%(id)s;"
        return MySQLConnection('certificacion_brandon_morales').query_db(query, data)

    # Borrar usuario
    @classmethod
    def borrar(cls, data):
        query = "DELETE FROM usuarios WHERE id = %(id)s;"
        return MySQLConnection('certificacion_brandon_morales').query_db(query, data)

    # Validaciones registro
    @classmethod
    def validar_registro(cls, form):
        is_valid = True
        if not form.get('nombre') or len(form['nombre'].strip()) < 2:
            flash('El nombre debe tener al menos 2 caracteres.', 'registro')
            is_valid = False
        if not form.get('apellido') or len(form['apellido'].strip()) < 2:
            flash('El apellido debe tener al menos 2 caracteres.', 'registro')
            is_valid = False
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not form.get('email') or not re.match(email_regex, form['email']):
            flash('El formato del email no es válido.', 'registro')
            is_valid = False
        else:
            if cls.obtener_por_email({'email': form['email']}):
                flash('Este email ya está registrado.', 'registro')
                is_valid = False
        if not form.get('password') or len(form['password']) < 8:
            flash('La contraseña debe tener al menos 8 caracteres.', 'registro')
            is_valid = False
        if form.get('password') != form.get('confirmar'):
            flash('Las contraseñas no coinciden.', 'registro')
            is_valid = False
        return is_valid

    # Validaciones login
    @classmethod
    def validar_login(cls, form):
        is_valid = True
        if not form.get('email'):
            flash('El email es obligatorio.', 'login')
            is_valid = False
        if not form.get('password'):
            flash('La contraseña es obligatoria.', 'login')
            is_valid = False
        return is_valid

    # Verificar contraseña
    def verificar_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
