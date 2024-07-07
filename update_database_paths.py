from peewee import *
from config import db

class Producto(Model):
    nombre = CharField()
    descripcion = TextField()
    precio = DecimalField()
    disponible = BooleanField()
    imagen = CharField()

    class Meta:
        database = db

def actualizar_rutas_imagenes():
    query = Producto.update(imagen=fn.REPLACE(Producto.imagen, '/static', '../static'))
    query.execute()

if __name__ == "__main__":
    db.connect()
    actualizar_rutas_imagenes()
    db.close()
