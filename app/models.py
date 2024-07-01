#importar orm peewee la base de datos, el modelo, los campos
from peewee import  Model, CharField, IntegerField, BooleanField 
from . import db

class BaseModel(Model):
    class Meta:
        database = db

class Producto(BaseModel):
    id = IntegerField(primary_key=True)
    nombre = CharField()
    descripcion = CharField()
    precio = IntegerField()
    disponible = BooleanField(default=True)  # Asumiendo que por defecto está disponible
    imagen = CharField(default="/path/to/default/image")  # Ruta de la imagen, puede ser opcional
