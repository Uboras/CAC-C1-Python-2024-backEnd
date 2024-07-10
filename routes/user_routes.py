from flask import Blueprint, request,jsonify
from flask_restx import Api, Resource, fields, Namespace
from database import get_db_connection

# Definición del Blueprint para usuarios
user_bp = Blueprint('user', __name__, url_prefix='/user')
api = Api(user_bp)
# Namespace para Flask-RESTX
user_ns = Namespace('user', description='Operaciones relacionadas con usuarios')

# Modelo de usuario para Flask-RESTX
user_model = api.model('User', {
    'id_user': fields.Integer(readonly=True, description='ID del usuario'),
    'nombre': fields.String(required=True, description='Nombre del usuario'),
    'contrasena': fields.String(required=True, description='Contraseña del usuario')
})

@api.route('/users')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """Lista todos los usuarios"""
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM user;"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        cnx.close()
        return results

    @api.doc('create_user')
    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Crea un nuevo usuario"""
        data = request.json
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "INSERT INTO user (nombre, contrasena) VALUES (%s, %s);"
        cursor.execute(query, (data['nombre'], data['contrasena']))
        cnx.commit()
        cursor.close()
        cnx.close()
        return data, 201

@api.route('/user/<string:nombre>')
class UserByName(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_model)
    def get(self, nombre):
        """Encuentra un usuario por nombre"""
        try:
            cnx = get_db_connection()
            cursor = cnx.cursor(dictionary=True)
            query = "SELECT * FROM user WHERE nombre = %s;"
            cursor.execute(query, (nombre,))
            result = cursor.fetchall()
            cursor.close()
            cnx.close()
            return result
        except Exception as e:
            return f"Error al encontrar el usuario: {str(e)}"

@api.route('/user/<int:id>')
class UserByID(Resource):
    @api.doc('delete_user')
    def delete(self, id):
        """Elimina un usuario por ID"""
        try:
            cnx = get_db_connection()
            cursor = cnx.cursor(dictionary=True)
            query = "DELETE FROM user WHERE id_user = %s;"
            cursor.execute(query, (id,))
            cnx.commit()
            cursor.close()
            cnx.close()
            return "Usuario eliminado correctamente"
        except Exception as e:
            return f"Error al eliminar el usuario: {str(e)}"

