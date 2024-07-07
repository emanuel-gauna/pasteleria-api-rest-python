from peewee import AutoField, Model, CharField, IntegerField, BooleanField
from . import db  # Asegúrate de importar la conexión a la base de datos adecuada

class BaseModel(Model):
    class Meta:
        database = db

class Producto(BaseModel):
    id = AutoField(primary_key=True)
    nombre = CharField()
    descripcion = CharField()
    precio = IntegerField()
    disponible = BooleanField(default=True)  # Asumiendo que por defecto está disponible
    imagen = CharField(default="../static/img/Captura de pantalla 2024-03-17 201208.png")  # Ruta de la imagen, puede ser opcional

    class Meta:
        table_name = 'productos'  # Nombre de la tabla en la base de datos
