# Pastelería API

## Descripción
La Pastelería API es una API RESTful desarrollada en Python utilizando Flask, Peewee y MySQL. Esta API permite gestionar productos, usuarios compradores, carritos de compra y listas de favoritos de una pastelería.

## Características
- CRUD de productos
- Listado de productos
- CRUD de usuarios compradores
- Gestión de carritos de compra
- Gestión de listas de favoritos

## Requisitos

- Python 3.12.4
- Docker
- Docker Compose
- MySQL

## Configuración del entorno

### Variables de entorno

Crear un archivo `.env` en el directorio raíz del proyecto con las siguientes variables de entorno:

```plaintext
DB_NAME=pasteleria_db
DB_USER=root
DB_PASSWORD=paste2024
DB_HOST=mysql-server
DB_PORT=3306
FLASK_ENV=development
FLASK_APP=app
