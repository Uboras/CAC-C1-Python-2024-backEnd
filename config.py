from dotenv import load_dotenv
import os

# Cargar las variables de entorno del archivo .env
load_dotenv()

DATABASE_CONFIG = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME')
}


