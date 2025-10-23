# app/models/comentario.py
from app.config.mysqlconnection import MySQLConnection

class Comentario:
    db = 'certificacion_brandon_morales'

    # Obtener comentarios para una pelicula (más recientes primero)
    @staticmethod
    def obtener_por_pelicula(pelicula_id):
        query = """
        SELECT c.id, c.contenido, c.usuario_id, c.pelicula_id, c.fecha_creacion,
               u.nombre AS usuario_nombre, u.apellido AS usuario_apellido
        FROM comentarios c
        JOIN usuarios u ON c.usuario_id = u.id
        WHERE c.pelicula_id = %(pelicula_id)s
        ORDER BY c.fecha_creacion DESC;
        """
        data = {'pelicula_id': pelicula_id}
        resultados = MySQLConnection(Comentario.db).query_db(query, data)
        return resultados if resultados else []

    # Obtener todos los comentarios (para páginas administrativas o listado general)
    @staticmethod
    def obtener_todos():
        query = """
        SELECT c.id, c.contenido, c.usuario_id, c.pelicula_id, c.fecha_creacion,
               u.nombre AS usuario_nombre, u.apellido AS usuario_apellido,
               p.titulo AS pelicula_titulo
        FROM comentarios c
        JOIN usuarios u ON c.usuario_id = u.id
        JOIN peliculas p ON c.pelicula_id = p.id
        ORDER BY c.fecha_creacion DESC;
        """
        resultados = MySQLConnection(Comentario.db).query_db(query)
        return resultados if resultados else []

    # Guardar nuevo comentario (espera pelicula_id, usuario_id, contenido)
    @staticmethod
    def guardar(data):
        query = """
        INSERT INTO comentarios (pelicula_id, usuario_id, contenido)
        VALUES (%(pelicula_id)s, %(usuario_id)s, %(contenido)s);
        """
        return MySQLConnection(Comentario.db).query_db(query, data)

    # Obtener por id
    @staticmethod
    def obtener_por_id(data):
        query = """
        SELECT c.id, c.contenido, c.usuario_id, c.pelicula_id, c.fecha_creacion,
               u.nombre AS usuario_nombre, u.apellido AS usuario_apellido
        FROM comentarios c
        JOIN usuarios u ON c.usuario_id = u.id
        WHERE c.id = %(id)s;
        """
        resultados = MySQLConnection(Comentario.db).query_db(query, data)
        return resultados[0] if resultados else None

    # Eliminar comentario por id
    @staticmethod
    def eliminar(data):
        query = "DELETE FROM comentarios WHERE id = %(id)s;"
        return MySQLConnection(Comentario.db).query_db(query, data)

    # Verifica si un comentario pertenece a un usuario (bool)
    @staticmethod
    def pertenece_a(comentario_id, usuario_id):
        query = "SELECT id FROM comentarios WHERE id = %(id)s AND usuario_id = %(usuario_id)s;"
        row = MySQLConnection(Comentario.db).query_db(query, {'id': comentario_id, 'usuario_id': usuario_id})
        return bool(row)
