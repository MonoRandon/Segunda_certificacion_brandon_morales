# app/models/pelicula.py
from app.config.mysqlconnection import MySQLConnection
from flask import flash
from datetime import datetime, date

class Pelicula:
    def __init__(self, data):
        # Inicializar atributos desde un diccionario (resultado de la DB)
        self.id = data.get('id')
        self.titulo = data.get('titulo')
        self.director = data.get('director')
        self.fecha = data.get('fecha')
        self.sinopsis = data.get('sinopsis')
        self.usuario_id = data.get('usuario_id')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    # Guardar nueva pelicula
    @classmethod
    def guardar(cls, data):
        query = """
        INSERT INTO peliculas (titulo, director, sinopsis, fecha, usuario_id)
        VALUES (%(titulo)s, %(director)s, %(sinopsis)s, %(fecha)s, %(usuario_id)s);
        """
        try:
            return MySQLConnection('certificacion_brandon_morales').query_db(query, data)
        except Exception as e:
            """ERROR AL GUARDAR PELICULA: {}""".format(e)
            return False

    # Obtener una pelicula por id (incluye datos del creador)
    @classmethod
    def obtener_por_id(cls, data):
        query = """
        SELECT a.*, u.nombre as creador_nombre, u.apellido as creador_apellido
        FROM peliculas a
        JOIN usuarios u ON a.usuario_id = u.id
        WHERE a.id = %(id)s;
        """
        resultado = MySQLConnection('certificacion_brandon_morales').query_db(query, data)
        return resultado[0] if resultado else None

    # Obtener todas las peliculas (ordenadas por fecha)
    @classmethod
    def obtener_todas(cls):
        query = """
        SELECT a.*, u.nombre as creador_nombre, u.apellido as creador_apellido
        FROM peliculas a
        JOIN usuarios u ON a.usuario_id = u.id
        ORDER BY a.fecha ASC;
        """
        resultados = MySQLConnection('certificacion_brandon_morales').query_db(query)
        return resultados if resultados else []

    # Actualizar pelicula
    @classmethod
    def actualizar(cls, data):
        query = """
        UPDATE peliculas 
        SET titulo=%(titulo)s, director=%(director)s, fecha=%(fecha)s, sinopsis=%(sinopsis)s
        WHERE id=%(id)s;
        """
        try:
            return MySQLConnection('certificacion_brandon_morales').query_db(query, data)
        except Exception as e:
            """ERROR AL ACTUALIZAR PELICULA: {}""".format(e)
            return False

    # Borrar pelicula
    @classmethod
    def borrar(cls, data):
        query = "DELETE FROM peliculas WHERE id = %(id)s;"
        return MySQLConnection('certificacion_brandon_morales').query_db(query, data)

    # Verifica si el usuario es creador de la pelicula
    @classmethod
    def es_creador(cls, usuario_id, pelicula_id):
        query = "SELECT usuario_id FROM peliculas WHERE id = %(id)s;"
        resultado = MySQLConnection('certificacion_brandon_morales').query_db(query, {'id': pelicula_id})
        if resultado:
            return resultado[0]['usuario_id'] == usuario_id
        return False

    # Validaciones: título único opcional, longitud mínima 3, etc.
    @staticmethod
    def validar_pelicula(form, check_unique=True, pelicula_id=None):
        is_valid = True

        # Título
        titulo = form.get('titulo', '').strip()
        if not titulo or len(titulo) < 3:
            flash('El título debe tener al menos 3 caracteres.', 'pelicula')
            is_valid = False
        else:
            if check_unique:
                query = "SELECT id FROM peliculas WHERE titulo = %(titulo)s;"
                existing = MySQLConnection('certificacion_brandon_morales').query_db(query, {'titulo': titulo})
                if existing:
                    if not pelicula_id or (len(existing) > 0 and existing[0]['id'] != int(pelicula_id)):
                        flash('Ya existe una película con ese título. Debe ser único.', 'pelicula')
                        is_valid = False

        # Director
        director = form.get('director', '').strip()
        if not director or len(director) < 3:
            flash('El nombre del director debe tener al menos 3 caracteres.', 'pelicula')
            is_valid = False

        # Sinopsis
        sinopsis = form.get('sinopsis', '')
        if not sinopsis or len(sinopsis.strip()) < 3:
            flash('La sinopsis debe tener al menos 3 caracteres.', 'pelicula')
            is_valid = False
        elif len(sinopsis) > 1000:
            flash('La sinopsis es demasiado larga.', 'pelicula')
            is_valid = False

        # Fecha
        if not form.get('fecha'):
            flash('La fecha es obligatoria.', 'pelicula')
            is_valid = False
        else:
            try:
                datetime.strptime(form['fecha'], '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de fecha inválido.', 'pelicula')
                is_valid = False

        return is_valid
