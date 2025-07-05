from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.user import User
from models.reservation import Reservation
from datetime import datetime
from functools import wraps

reservations_bp = Blueprint('reservations', __name__)

def user_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'user':
            return jsonify({'error': 'User access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

@reservations_bp.route('/book', methods=['POST'])
@user_required
def book_spot():
    data = request.get_json()
    lot_id = data.get('lot_id')
    vehicle_number = data.get('vehicle_number')
    if not lot_id or not vehicle_number:
        return jsonify({'error': 'Missing lot_id or vehicle_number'}), 400
    user_id = get_jwt_identity()
    # Check if user already has an active reservation
    active = Reservation.query.filter_by(user_id=user_id, status='active').first()
    if active:
        return jsonify({'error': 'You already have an active reservation'}), 400
    # Find first available spot
    spot = ParkingSpot.query.filter_by(parking_lot_id=lot_id, is_occupied=False).first()
    if not spot:
        return jsonify({'error': 'No available spots in this lot'}), 400
    spot.is_occupied = True
    reservation = Reservation(
        user_id=user_id,
        parking_spot_id=spot.id,
        vehicle_number=vehicle_number,
        start_time=datetime.utcnow(),
        status='active'
    )
    db.session.add(reservation)
    db.session.commit()
    return jsonify(reservation.to_dict()), 201

@reservations_bp.route('/release', methods=['POST'])
@user_required
def release_spot():
    data = request.get_json()
    reservation_id = data.get('reservation_id')
    if not reservation_id:
        return jsonify({'error': 'Missing reservation_id'}), 400
    user_id = get_jwt_identity()
    reservation = Reservation.query.filter_by(id=reservation_id, user_id=user_id, status='active').first()
    if not reservation:
        return jsonify({'error': 'Active reservation not found'}), 404
    reservation.end_time = datetime.utcnow()
    reservation.status = 'completed'
    reservation.calculate_cost()
    spot = ParkingSpot.query.get(reservation.parking_spot_id)
    spot.is_occupied = False
    db.session.commit()
    return jsonify(reservation.to_dict())

@reservations_bp.route('/active', methods=['GET'])
@user_required
def get_active_reservation():
    user_id = get_jwt_identity()
    reservation = Reservation.query.filter_by(user_id=user_id, status='active').first()
    if not reservation:
        return jsonify({'active': False})
    return jsonify({'active': True, 'reservation': reservation.to_dict()})

@reservations_bp.route('/history', methods=['GET'])
@user_required
def get_reservation_history():
    user_id = get_jwt_identity()
    reservations = Reservation.query.filter_by(user_id=user_id).filter(Reservation.status != 'active').order_by(Reservation.start_time.desc()).all()
    result = []
    for r in reservations:
        spot = ParkingSpot.query.get(r.parking_spot_id)
        lot = ParkingLot.query.get(spot.parking_lot_id) if spot else None
        d = r.to_dict()
        d['spot_number'] = spot.spot_number if spot else None
        d['lot_name'] = lot.name if lot else None
        result.append(d)
    return jsonify(result)
