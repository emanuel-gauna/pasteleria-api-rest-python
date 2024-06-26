#importar orm peewee la base de datos, el modelo, los campos
from peewee import  Model, CharField 
from . import db

class BaseModel(Model):
    class Meta:
        database = db

class MiModelo(BaseModel):
    campo = CharField()
