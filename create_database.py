from peewee import MySQLDatabase, AutoField, Model, CharField, FloatField, BooleanField, fn
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de la base de datos
db = MySQLDatabase(
    os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
)

# Definición del modelo Producto
class BaseModel(Model):
    class Meta:
        database = db

class Producto(BaseModel):
    id = AutoField(primary_key=True)
    nombre = CharField()
    descripcion = CharField()
    precio = FloatField()
    disponible = BooleanField()
    imagen = CharField()

    class Meta:
        table_name = 'productos'  # Nombre de la tabla en la base de datos

# Función para crear y poblar la base de datos
def create_and_populate_database():
    try:
        # Conectarse a la base de datos
        db.connect()

        # Crear las tablas si no existen
        db.create_tables([Producto])
        # Datos de productos a insertar
        productos_data = [
            {
                'nombre': "Muffins varios",
                'descripcion': "Deliciosos muffins horneados con arándanos frescos y una pizca de canela de Arándanos, banana, o Frutos Rojos, chips de chocolate y rellenos de dulce de leche (precio por unidad)",
                'precio': 600.00,
                'disponible': True,
                'imagen': "Muffins de coco y dulce de leche.jpg"
            },
            {
                'nombre': "Budín de Limón y Chocolate con  Nuez",
                'descripcion': "Budín esponjoso con el sabor cítrico de la naranja y un glaseado de azúcar, de nuez y bañado en  chocolate (precio por unidad)",
                'precio': 3000,
                'disponible': True,
                'imagen': "budin de limon y amapolas , budin de chocolate y nuez.png"
            },
            {
                'nombre': "Escones de Queso",
                'descripcion': "Escones de queso salados, para acompañar con fiambres o solos (precio por unidad)",
                'precio': 100,
                'disponible': False,
                'imagen': "scones de queso.png"
            },
            {
                'nombre': "Tarta de Manzana",
                'descripcion': "Tarta crujiente con una capa de manzanas frescas y un toque de canela, perfecta para cualquier ocasión.",
                'precio': 6000,
                'disponible': True,
                'imagen': "tarta-manzana.jpg"
            },
            {
                'nombre': "Roll de Canela",
                'descripcion': "Rolles de canela dulces con azucar negra por 6 unidades, ideales para la merienda o desayuno",
                'precio': 3500,
                'disponible': True,
                'imagen': "Roll-canela.jpg"
            },
            {
                'nombre': "Pasta Frola",
                'descripcion': "Clásica Pastaflora de dulce de membrillo, batata, y dulce de leche",
                'precio': 5000,
                'disponible': True,
                'imagen': "pastafrola.jpg"
            },
            {
                'nombre': "Medialunas",
                'descripcion': "medialunas de manteca y de grasa, ideal para desayuno y merienda (precio por docena)",
                'precio': 4000,
                'disponible': True,
                'imagen': "medialunas.jpg"
            },
            {
                'nombre': "Rosca de Reyes",
                'descripcion': "Rosca dulce tradicional decorada con frutas confitadas y azúcar glase, típica de la celebración del Día de Reyes o Pascuas.",
                'precio': 4500,
                'disponible': False,
                'imagen': "rosca-reyes.jpg"
            },
            {
                'nombre': "Cookies",
                'descripcion': "Galletas caseras dulces , crujientes por fuera y suaves por dentro, ideales para acompañar un café con chispas de chocolate. (precio por 250GR)",
                'precio': 1000,
                'disponible': True,
                'imagen': "cookies.jpg"
            },
            {
                'nombre': "Chipá",
                'descripcion': "Galletas saladas horneadas con una pizca de sal marina y hierbas frescas, perfectas para acompañar un queso.(precio por 250 gr)",
                'precio': 2000,
                'disponible': True,
                'imagen': "chipá.jpg"
            },
            {
                'nombre': "Alfajores de Maizena",
                'descripcion': "Dulces alfajores rellenos de dulce de leche y cubiertos con coco rallado (precio por unidad)",
                'precio': 250,
                'disponible': True,
                'imagen': "IMG-20240505-WA0028.jpg"
            },
            {
                'nombre': "Shots - chocotorta- cheesecake",
                'descripcion': "shots de postres dedicados para ocaciones especiales cheesecake - chocotorta - red velvet (precio por unidad)",
                'precio': 1000,
                'disponible': False,
                'imagen': "shots-chocotorta.jpg"
            },
            {
                'nombre': "Desayunos dedicados",
                'descripcion': "Desayunos dedicados para ocaciones especiales. consta de: 2 rodajas de budin marmolado, cake de manzana, porcion de torta, 2 pebetes de jyq, 3 chipacitos, 3 galletas glase, un jugo individual, infusiones varias (precio a convenir)",
                'precio': 0,
                'disponible': False,
                'imagen': "desayuno.jpg"
            },
        ]

        # Insertar cada producto en la base de datos
        for producto_data in productos_data:
            Producto.create(
                nombre=producto_data['nombre'],
                descripcion=producto_data['descripcion'],
                precio=producto_data['precio'],
                disponible=producto_data['disponible'],
                imagen=producto_data['imagen']
            )
            
        print('Base de datos creada y productos insertados correctamente.')

    except Exception as e:
        print(f'Error al crear la base de datos: {str(e)}')

    finally:
        # Cerrar la conexión a la base de datos
        db.close()

# Llamar a la función para crear y poblar la base de datos
if __name__ == '__main__':
    create_and_populate_database()