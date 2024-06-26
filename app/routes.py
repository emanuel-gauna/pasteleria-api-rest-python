from flask import jsonify, request
from .models import MiModelo
from . import app

@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})

@app.route('/api/mimodelo', methods=['GET'])
def get_mimodelos():
    mimodelos = MiModelo.select()
    return jsonify([{'id': modelo.id, 'campo': modelo.campo} for modelo in mimodelos])

@app.route('/api/mimodelo', methods=['POST'])
def create_mimodelo():
    data = request.get_json()
    nuevo_modelo = MiModelo.create(campo=data['campo'])
    return jsonify({'id': nuevo_modelo.id, 'campo': nuevo_modelo.campo}), 201

if __name__ == '__main__':
    app.run()
