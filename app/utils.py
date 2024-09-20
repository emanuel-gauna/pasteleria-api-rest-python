from functools import wraps
from flask import jsonify, request
from flask_login import current_user

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'message': 'Por favor inicie sesión'}), 401
            if current_user.role != required_role:
                return jsonify({'message': 'No tiene permiso para acceder a esta función'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
