from peewee import PostgresqlDatabase, AutoField, Model, CharField, FloatField, BooleanField, OperationalError, InterfaceError
from dotenv import load_dotenv
import os
from app.models import User, Producto

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de la base de datos PostgreSQL
db = PostgresqlDatabase(
    os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT', '5432')),
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
        if not db.is_closed():
            db.close()
        
        db.connect()

        # Crear las tablas si no existen
        db.create_tables([Producto, User])

        # Datos de productos a insertar
        productos_data = [
            # ... (tus datos de productos aquí)
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

    except (OperationalError, InterfaceError) as e:
        print(f'Error al conectar o interactuar con la base de datos: {str(e)}')

    except Exception as e:
        print(f'Error al crear la base de datos: {str(e)}')

    finally:
        # Cerrar la conexión a la base de datos
        if not db.is_closed():
            db.close()

def create_admin_user():
    try:
        if not db.is_closed():
            db.close()

        db.connect()

        with db.atomic():
            if not User.select().where(User.username == 'admin').exists():
                admin = User(username='admin', is_admin=True)
                admin.set_password('pasteleria24')  # Cambia 'admin_password' por la contraseña que prefieras
                admin.save()
        print('Usuario administrador creado correctamente.')
    
    except (OperationalError, InterfaceError) as e:
        print(f'Error al conectar o interactuar con la base de datos: {str(e)}')

    except Exception as e:
        print(f'Error al crear el usuario administrador: {str(e)}')
    finally:
        # Cerrar la conexión a la base de datos
        if not db.is_closed():
            db.close()

# Llamar a la función para crear y poblar la base de datos
if __name__ == '__main__':
    create_and_populate_database()
    create_admin_user()
