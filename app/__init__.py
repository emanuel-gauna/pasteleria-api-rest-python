#importar flask, respuesta y codificacion a json
from flask import Flask, render_template, url_for
import subprocess
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from peewee import MySQLDatabase 
from dotenv import load_dotenv
from flask_cors import CORS 
import os 

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Inicializar la aplicación Flask
app = Flask(__name__)
app.config['DEBUG'] = True

# Configurar CORS para permitir solicitudes desde cualquier origen
CORS(app, supports_credentials=True)

# Configuración de Flask-Login
app.secret_key = 'admin1234'   # Necesario para la gestión de sesiones
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Nombre de la vista de inicio de sesión

# Configuración de la base de datos MySQL utilizando peewee y variables de entorno
db = MySQLDatabase(
    os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
)

# Función para esperar a que MySQL esté listo
def wait_for_mysql():
    wait_cmd = ['wait-for-it.sh', '--host=' + os.getenv('DB_HOST'), '--port=' + os.getenv('DB_PORT'), '--timeout=60']
    subprocess.run(wait_cmd, check=True)

# Hook de Flask para esperar a que MySQL esté listo antes de cada solicitud
@app.before_request
def before_request():
    wait_for_mysql()  # Esperar a que MySQL esté listo antes de conectar

# Debug: Imprimir variables de entorno para verificación
print(os.getenv('DB_NAME'))
print(os.getenv('DB_USER'))
print(os.getenv('DB_PASSWORD'))
print(os.getenv('DB_HOST'))
print(os.getenv('DB_PORT'))

# Importar las rutas desde otro módulo
from .routes import *

# Conectar la base de datos
db.connect()

# Ejecutar la aplicación Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
