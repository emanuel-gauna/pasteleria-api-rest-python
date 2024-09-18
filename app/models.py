from peewee import AutoField, Model, CharField, DecimalField, BooleanField, ForeignKeyField, IntegerField,FloatField, DateTimeField
from datetime import datetime
from app import db  # Asegúrate de importar la conexión a la base de datos adecuada
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class BaseModel(Model):
    class Meta:
        database = db

class Producto(BaseModel):
    id = AutoField(primary_key=True)
    nombre = CharField(max_length=255)
    descripcion = CharField(max_length=1000)
    precio = DecimalField(max_digits=10, decimal_places=2)  # Usar DecimalField para precios
    disponible = BooleanField(default=True)
    imagen = CharField(default="/Captura de pantalla 2024-03-17 201208.png")

    class Meta:
        table_name = 'productos'

class User(BaseModel, UserMixin):
    id = AutoField(primary_key=True)
    username = CharField(max_length=128)
    password_hash = CharField(max_length=256)  # Aumentar el tamaño para hashes largos
    is_admin = BooleanField(default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.save()  # Guardar después de establecer la contraseña

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    class Meta:
        table_name = 'users'

class Carrito(Model):
    user = ForeignKeyField(User, backref='carritos', on_delete='CASCADE')
    producto = ForeignKeyField(Producto, backref='carritos', on_delete='CASCADE')
    cantidad = IntegerField(default=1)
    total = FloatField()
    fecha_creacion = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'carrito'

