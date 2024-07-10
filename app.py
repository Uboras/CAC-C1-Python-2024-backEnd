from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from routes.user_routes import user_bp, api as user_ns
from routes.pelicula_routes import pelicula_bp, api as pelicula_ns

app = Flask(__name__)
CORS(app)

# Inicializar Flask-RESTX
api = Api(app, version='1.0', title='API de Usuarios y Películas CAC',
          description='API CRUD para usuarios y películas')

# Registrar los Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(pelicula_bp)

# Añadir Namespaces
api.add_namespace(user_ns)
api.add_namespace(pelicula_ns)

if __name__ == '__main__':
    app.run(debug=True)
# Namespace para Flask-RESTX