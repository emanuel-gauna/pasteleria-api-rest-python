from flask import Flask
from flask_login import LoginManager
from peewee import PostgresqlDatabase
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la base de datos PostgreSQL
db = PostgresqlDatabase(
    os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT', '5432')),
)

# Crear la instancia de la aplicación Flask
app = Flask(__name__)
CORS(app)
app.config.from_object('app.config.Config')

# Inicializar LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Importar las rutas
from app import routes
