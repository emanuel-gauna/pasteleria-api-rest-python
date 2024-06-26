#importar flask, respuesta y codificacion a json
from flask import Flask
import subprocess
from peewee import MySQLDatabase 
from dotenv import load_dotenv
import os 


load_dotenv()

app = Flask(__name__) 
app.config['DEBUG'] = True

db = MySQLDatabase(
    os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
)

def wait_for_mysql():
    wait_cmd = ['wait-for-it.sh', '--host=' + os.getenv('DB_HOST'), '--port=' + os.getenv('DB_PORT'), '--timeout=30']
    subprocess.run(wait_cmd, check=True)

def before_first_request():
    wait_for_mysql()  # Esperar a que MySQL esté listo antes de conectar


print(os.getenv('DB_NAME'))
print(os.getenv('DB_USER'))
print(os.getenv('DB_PASSWORD'))
print(os.getenv('DB_HOST'))
print(os.getenv('DB_PORT'))

#importar las rutas
from .routes import *

#conectar la base de datos
db.connect()