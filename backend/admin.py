from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.user import User
from models.reservation import Reservation
from functools import wraps

admin_bp = Blueprint('admin', __name__)

# Admin role check decorator (reuse from auth.py if possible)
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

# --- Parking Lot CRUD ---
@admin_bp.route('/lots', methods=['POST'])
@admin_required
def create_lot():
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    capacity = data.get('capacity')
    vehicle_type = data.get('vehicle_type', 'car')
    rate_per_hour = data.get('rate_per_hour', 10.0)
    if not name or not address or not capacity:
        return jsonify({'error': 'Missing required fields'}), 400
    lot = ParkingLot(name=name, address=address, capacity=capacity)
    db.session.add(lot)
    db.session.commit()
    # Auto-create spots
    for i in range(1, capacity+1):
        spot = ParkingSpot(
            spot_number=str(i),
            parking_lot_id=lot.id,
            vehicle_type=vehicle_type,
            rate_per_hour=rate_per_hour
        )
        db.session.add(spot)
    db.session.commit()
    return jsonify(lot.to_dict()), 201

@admin_bp.route('/lots', methods=['GET'])
@admin_required
def list_lots():
    lots = ParkingLot.query.all()
    return jsonify([lot.to_dict() for lot in lots])

@admin_bp.route('/lots/<int:lot_id>', methods=['GET'])
@admin_required
def get_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = ParkingSpot.query.filter_by(parking_lot_id=lot.id).all()
    lot_data = lot.to_dict()
    lot_data['spots'] = [spot.to_dict() for spot in spots]
    return jsonify(lot_data)

@admin_bp.route('/lots/<int:lot_id>', methods=['PUT'])
@admin_required
def update_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    data = request.get_json()
    lot.name = data.get('name', lot.name)
    lot.address = data.get('address', lot.address)
    lot.capacity = data.get('capacity', lot.capacity)
    db.session.commit()
    return jsonify(lot.to_dict())

@admin_bp.route('/lots/<int:lot_id>', methods=['DELETE'])
@admin_required
def delete_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    db.session.delete(lot)
    db.session.commit()
    return jsonify({'message': 'Parking lot deleted'})

# --- Parking Spot Details ---
@admin_bp.route('/lots/<int:lot_id>/spots', methods=['GET'])
@admin_required
def list_spots(lot_id):
    spots = ParkingSpot.query.filter_by(parking_lot_id=lot_id).all()
    return jsonify([spot.to_dict() for spot in spots])

# --- User List and Spot Usage ---
@admin_bp.route('/users', methods=['GET'])
@admin_required
def list_users():
    users = User.query.all()
    user_list = []
    for user in users:
        # Find active reservation (if any)
        reservation = Reservation.query.filter_by(user_id=user.id, status='active').first()
        spot_id = reservation.parking_spot_id if reservation else None
        user_list.append({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'spot_id': spot_id
        })
    return jsonify(user_list)
