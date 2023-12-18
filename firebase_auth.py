from functools import wraps
from flask import request, jsonify
from firebase_admin import auth

def check_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split('Bearer ')[1]

        if not token:
            return jsonify({'message': 'No token was provided, please login.'}), 401

        try:
            decoded_token = auth.verify_id_token(token)
            return f(decoded_token, *args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Token is invalid'}), 403

    return decorated_function