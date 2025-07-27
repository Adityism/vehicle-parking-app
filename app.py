from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, jwt_required
from flask_cors import CORS, cross_origin
from backend.models import db
from backend.auth import auth_bp
from backend.admin import admin_bp
from backend.reservations import reservations_bp
from backend.celery_worker import make_celery
import os
from datetime import timedelta

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "backend", "parking.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'

db.init_app(app)
jwt = JWTManager(app)
make_celery(app)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(reservations_bp, url_prefix='/api/reservations')

@app.route('/')
def index():
   return {"message": "Vehicle Parking App API - Authentication Service"}



@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
   return jsonify({
       'status': 'error',
       'message': 'Token has expired'
   }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
   print(f"Invalid token error: {error}")
   return jsonify({
       'status': 'error',
       'message': 'Invalid token'
   }), 401

@jwt.unauthorized_loader
def unauthorized_callback(error):
   print(f"Unauthorized error: {error}")
   return jsonify({
       'status': 'error',
       'message': 'Missing token'
   }), 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5009)