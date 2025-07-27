from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, decode_token
from .models import db
from .models.user import User
from datetime import timedelta
from functools import wraps
import jwt

auth_bp = Blueprint('auth', __name__)

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        # Convert string user_id to integer for database lookup
        user_id_int = int(user_id) if user_id else None
        user = User.query.get(user_id_int)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing email or password'}), 400
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    access_token = create_access_token(
        identity=str(user.id),  # Convert to string
        expires_delta=timedelta(hours=24)
    )
    print(f"Login successful for user {user.email} (ID: {user.id}, Role: {user.role})")
    print(f"Generated token: {access_token[:50]}...")
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role
        }
    }), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['email', 'password', 'name']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    user = User(
        email=data['email'],
        name=data['name'],
        role='user'
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(
        identity=str(user.id),  # Convert to string
        expires_delta=timedelta(hours=24)
    )
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role
        }
    }), 201

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        print(f"Request headers: {dict(request.headers)}")
        print(f"Authorization header: {request.headers.get('Authorization')}")
        user_id = get_jwt_identity()
        print(f"JWT identity (user_id): {user_id}")
        print(f"JWT identity type: {type(user_id)}")
        # Convert string user_id back to integer for database lookup
        user_id_int = int(user_id) if user_id else None
        user = User.query.get(user_id_int)
        if not user:
            print(f"User not found for ID: {user_id_int}")
            return jsonify({'error': 'User not found'}), 404
        print(f"User found: {user.email}, role: {user.role}")
        return jsonify({
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role
        }), 200
    except Exception as e:
        print(f"Error in get_current_user: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Token validation failed'}), 401

@auth_bp.route('/test-token', methods=['POST'])
def test_token():
    data = request.get_json()
    token = data.get('token')
    if not token:
        return jsonify({'error': 'No token provided'}), 400
    
    try:
        # Try to decode with PyJWT directly
        from flask import current_app
        decoded = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        print(f"PyJWT decode successful: {decoded}")
        return jsonify({'decoded': decoded}), 200
    except Exception as e:
        print(f"PyJWT decode failed: {e}")
        return jsonify({'error': str(e)}), 400
