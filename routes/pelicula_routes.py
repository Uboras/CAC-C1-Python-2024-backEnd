from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource, fields, Namespace
from database import get_db_connection

# Definición del Blueprint para películas
pelicula_bp = Blueprint('pelicula', __name__, url_prefix='/pelicula')
api = Api(pelicula_bp)

# Modelo de película para Flask-RESTX
pelicula_model = api.model('Pelicula', {
    'id_peliculas': fields.Integer(readonly=True, description='ID de la película'),
    'nombre_peliculas': fields.String(required=True, description='Nombre de la película')
})

# Definición de los Endpoints para películas
@api.route('/peliculas')
class PeliculaList(Resource):
    @api.doc('list_peliculas')
    @api.marshal_list_with(pelicula_model)
    def get(self):
        """Lista todas las películas"""
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM peliculas;"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        cnx.close()
        return results
    

    @api.doc('create_pelicula')
    @api.expect(pelicula_model)
    @api.marshal_with(pelicula_model, code=201)
    def post(self):
        """Crea una nueva película"""
        data = request.json
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "INSERT INTO peliculas (nombre_peliculas) VALUES (%s);"
        cursor.execute(query, (data['nombre'],))
        cnx.commit()
        cursor.close()
        cnx.close()
        return data, 201

@api.route('/pelicula/<int:id>')
class Pelicula(Resource):
    @api.doc('get_pelicula')
    @api.marshal_with(pelicula_model)
    def get(self, id):
        """Obtiene detalles de una película por ID"""
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM peliculas WHERE id_peliculas = %s;"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        return result

    @api.doc('update_pelicula')
    @api.expect(pelicula_model)
    @api.marshal_with(pelicula_model)
    def put(self, id):
        """Actualiza una película por ID"""
        data = request.json
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "UPDATE peliculas SET nombre = %s WHERE id_peliculas = %s;"
        cursor.execute(query, (data['nombre'], id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return data

    @api.doc('delete_pelicula')
    def delete(self, id):
        """Elimina una película por ID"""
        try:
            cnx = get_db_connection()
            cursor = cnx.cursor(dictionary=True)
            query = "DELETE FROM peliculas WHERE id_peliculas = %s;"
            cursor.execute(query, (id,))
            cnx.commit()
            cursor.close()
            cnx.close()
            return "Película eliminada correctamente"
        except Exception as e:
            return f"Error al eliminar la película: {str(e)}"

# Namespace para Flask-RESTX
pelicula_ns = Namespace('pelicula', description='Operaciones relacionadas con películas')
