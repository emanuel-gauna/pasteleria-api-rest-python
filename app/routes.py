from flask import jsonify, request, abort
from .models import Producto
from . import app
from peewee import DoesNotExist  # Importa la excepción DoesNotExist desde peewee

@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})

# Ruta para obtener todos los productos
@app.route('/api/productos', methods=['GET'])
def get_productos():
    try:
        productos = Producto.select()
        productos_list = [{'id': producto.id, 'nombre': producto.nombre, 'descripcion': producto.descripcion, 'precio': producto.precio, 'disponible': producto.disponible, 'imagen': producto.imagen} for producto in productos]
        return jsonify(productos_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener un producto por su ID
@app.route('/api/productos/<int:producto_id>', methods=['GET'])
def get_producto(producto_id):
    try:
        producto = Producto.get_by_id(producto_id)
        return jsonify({'id': producto.id, 'nombre': producto.nombre, 'descripcion': producto.descripcion,
                        'precio': producto.precio, 'disponible': producto.disponible, 'imagen': producto.imagen})
    except DoesNotExist:
        abort(404, description=f'Producto con id {producto_id} no encontrado')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para crear un nuevo producto
@app.route('/api/productos', methods=['POST'])
def create_producto():
    data = request.get_json()
    try:
        nuevo_producto = Producto.create(
            nombre=data['nombre'],
            descripcion=data['descripcion'],
            precio=data['precio'],
            disponible=data['disponible'],
            imagen=data.get('imagen', "../static/img/Captura de pantalla 2024-03-17 201208.png")  # imagen es opcional, utiliza una imagen por defecto si no se proporciona
        )
        return jsonify({'id': nuevo_producto.id}), 201
    except KeyError as e:
        return jsonify({'error': f'Falta el campo requerido: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para actualizar un producto
@app.route('/api/productos/<int:producto_id>', methods=['PUT'])
def update_producto(producto_id):
    data = request.get_json()
    try:
        producto = Producto.get_by_id(producto_id)
        producto.nombre = data.get('nombre', producto.nombre)
        producto.descripcion = data.get('descripcion', producto.descripcion)
        producto.precio = data.get('precio', producto.precio)
        producto.disponible = data.get('disponible', producto.disponible)
        producto.imagen = data.get('imagen', producto.imagen)
        producto.save()
        return jsonify({'message': f'Producto {producto_id} actualizado correctamente'}), 200
    except DoesNotExist:
        abort(404, description=f'Producto con id {producto_id} no encontrado')
    except KeyError as e:
        return jsonify({'error': f'Falta el campo requerido: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar un producto
@app.route('/api/productos/<int:producto_id>', methods=['DELETE'])
def delete_producto(producto_id):
    try:
        producto = Producto.get_by_id(producto_id)
        producto.delete_instance()
        return jsonify({'message': f'Producto {producto_id} eliminado correctamente'}), 200
    except DoesNotExist:
        abort(404, description=f'Producto con id {producto_id} no encontrado')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
