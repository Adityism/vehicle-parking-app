from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.user import User
from models.reservation import Reservation
from functools import wraps

admin_bp = Blueprint('admin', __name__)

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

@admin_bp.route('/lots/<int:lot_id>/spots', methods=['GET'])
@admin_required
def list_spots(lot_id):
    spots = ParkingSpot.query.filter_by(parking_lot_id=lot_id).all()
    return jsonify([spot.to_dict() for spot in spots])

@admin_bp.route('/users', methods=['GET'])
@admin_required
def list_users():
    users = User.query.all()
    user_list = []
    for user in users:
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

@admin_bp.route('/reservations', methods=['GET'])
@admin_required
def all_reservations():
    reservations = Reservation.query.order_by(Reservation.parking_timestamp.desc()).all()
    result = []
    for r in reservations:
        user = User.query.get(r.user_id)
        spot = ParkingSpot.query.get(r.parking_spot_id)
        lot = ParkingLot.query.get(spot.parking_lot_id) if spot else None
        d = r.to_dict()
        d['user_email'] = user.email if user else None
        d['spot_number'] = spot.spot_number if spot else None
        d['lot_name'] = lot.name if lot else None
        result.append(d)
    return jsonify(result)

@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats():
    total_reservations = Reservation.query.count()
    total_revenue = db.session.query(db.func.sum(Reservation.cost)).scalar() or 0.0
    lot_counts = db.session.query(ParkingLot.name, db.func.count(Reservation.id))\
        .join(ParkingSpot, ParkingSpot.parking_lot_id == ParkingLot.id)\
        .join(Reservation, Reservation.parking_spot_id == ParkingSpot.id)\
        .group_by(ParkingLot.name).all()
    spot_counts = db.session.query(ParkingSpot.spot_number, db.func.count(Reservation.id))\
        .join(Reservation, Reservation.parking_spot_id == ParkingSpot.id)\
        .group_by(ParkingSpot.spot_number).all()
    return jsonify({
        'total_reservations': total_reservations,
        'total_revenue': round(total_revenue, 2),
        'lot_counts': [{'lot': l, 'count': c} for l, c in lot_counts],
        'spot_counts': [{'spot': s, 'count': c} for s, c in spot_counts]
    })
