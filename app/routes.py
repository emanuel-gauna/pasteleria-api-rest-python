from flask import jsonify, request, abort, send_from_directory
from app.models import Producto, User, Carrito
from app import app, login_manager
from peewee import DoesNotExist
from flask_login import login_user, login_required, logout_user, current_user
from flask_cors import CORS

CORS(app, origins=["https://emanuel-gauna.github.io"])



@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})

# Ruta para obtener todos los productos
@app.route('/api/productos', methods=['GET'])
def get_productos():
    try:
        productos = Producto.select()
        productos_list = [
            {
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': str(producto.precio),  # Convertir a cadena para evitar problemas con JSON
                'disponible': producto.disponible,
                'imagen': f'{producto.imagen}'
            } for producto in productos
        ]
        return jsonify(productos_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener un producto por su ID
@app.route('/api/productos/<int:producto_id>', methods=['GET'])
def get_producto(producto_id):
    try:
        producto = Producto.get_by_id(producto_id)
        return jsonify({
            'id': producto.id,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'precio': str(producto.precio),  # Convertir a cadena para evitar problemas con JSON
            'disponible': producto.disponible,
            'imagen': f'{producto.imagen}'
        })
    except DoesNotExist:
        abort(404, description=f'Producto con id {producto_id} no encontrado')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para crear un nuevo producto (ruta protegida)
@app.route('/api/productos', methods=['POST'])
@login_required
def create_producto():
    data = request.get_json()
    try:
        nuevo_producto = Producto.create(
            nombre=data['nombre'],
            descripcion=data['descripcion'],
            precio=data['precio'],
            disponible=data['disponible'],
            imagen=data.get('imagen', "Captura de pantalla 2024-03-17 201208.png")  # Imagen opcional
        )
        return jsonify({'id': nuevo_producto.id}), 201
    except KeyError as e:
        return jsonify({'error': f'Falta el campo requerido: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para actualizar un producto (ruta protegida)
@app.route('/api/productos/<int:producto_id>', methods=['PUT'])
@login_required
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

# Ruta para eliminar un producto (ruta protegida)
@app.route('/api/productos/<int:producto_id>', methods=['DELETE'])
@login_required
def delete_producto(producto_id):
    try:
        producto = Producto.get_by_id(producto_id)
        producto.delete_instance()
        return jsonify({'message': f'Producto {producto_id} eliminado correctamente'}), 200
    except DoesNotExist:
        abort(404, description=f'Producto con id {producto_id} no encontrado')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#agregar productos al carrito de compras
@app.route('/api/carrito/agregar', method=['POST'])#ruta
@login_required # login requerido
def agregar_carrito(): # funcion que se ejecuta cuando se accede a la ruta
    data = request.get_json() # almacenamos los datos de la solicitud en formato json
    try: #bloque try para manejar posibles excepciones durante la ejecucion del codigo
        producto_id = data['producto_id'] #extraemos el producto_id en la variable
        cantidad = data.get('cantidad', 1) #extraemos la cantidad del producto a agregar por defecto sera 1

        producto = Producto.get_by_id(producto_id)#busca en la BD el producto con el id expecificado
        
        if not producto.disponible:#verificar si el producto esta disponible
            return jsonify({'error': 'El producto no esta disponible'}), 400 
        
        total = producto.precio * cantidad # calculo para sacar el total multiplicando el precio del producto por la cantidad indicada

        Carrito.create(#funcion de crear una nueva entrada en la tabla de carrito
            user = current_user.id, #asocia el producto al carrito del usuario autenticado por flask login
            producto = producto, #asignamos el producto de la BD
            cantidad = cantidad, #asignamos la cantidad del producto
            total = total #almacena el total calculado
        )
        return jsonify({'message': f'Producto {producto.nombre} agregado al carrito'}), 201
    #respuesta para el cliente en json
    except DoesNotExist: # si ocurre una excepcion que el producto no existe
        return jsonify({'error':f'Producto con id {producto_id} no encontrado'}), 404
    except Exception as e: #captura cualquier otra excepción devolviendo error del servidor
        return jsonify({'error': str(e)}), 500

#eliminar productos del carrito
@app.route('/api/carrito/eliminar/<int:carrito_id>', method=['POST'])#decoradores de ruta
@login_required #decorador de  login requerido
def eliminar_carrito(carrito_id):#metodo para eliminar del carrito
    try:
        carrito_item = Carrito.get_by_id(carrito_id) #de la clase carrito filtar por su id
        carrito_item.delete_instance()#elimina el registro de la base de datos
        return jsonify({'message': f'Producto eliminado del carrito'}), 200
    
    except DoesNotExist: # a menos que no exista
        return jsonify({'error': 'Producto no encontrado en el carrito'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Ruta para listar los productos en el carrito
@app.route('/api/carrito/listar', methods=['GET'])#decorador de ruta metodo "get"
@login_required # decorador de usuario autenticado 
def listar_carrito(): #funcion que se ejecuta al acceder a la ruta
    try:
        carrito_items = Carrito.select().where(Carrito.user == current_user.id)
        #selecciona los registros de la tabla carrito. donde el campo user del carrito sea igual al id del usuario actualmente autenticado
        productos = [
            {
                'producto_id': item.producto.id,
                'nombre': item.producto.nombre,
                'cantidad': item.cantidad,
                'total': item.total
            } for item in carrito_items
        ]
        return jsonify(productos), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# Ruta de inicio de sesión
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    try:
        user = User.get(User.username == username)
    except DoesNotExist:
        return jsonify({'message': 'Usuario o contraseña incorrectos'}), 401

    if user.check_password(password):
        login_user(user)
        return jsonify({'message': 'Inicio de sesión exitoso'}), 200
    else:
        return jsonify({'message': 'Usuario o contraseña incorrectos'}), 401

# Ruta de cierre de sesión
@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Sesión cerrada'}), 200

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)
