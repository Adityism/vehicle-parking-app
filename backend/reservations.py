from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db
from backend.models.parking_lot import ParkingLot
from backend.models.parking_spot import ParkingSpot
from backend.models.user import User
from backend.models.reservation import Reservation
from datetime import datetime
from functools import wraps
from backend.redis_client import redis_client
from flask_cors import cross_origin

reservations_bp = Blueprint('reservations', __name__)

@reservations_bp.route('/lots', methods=['GET'])
@cross_origin(supports_credentials=True)
def available_lots():
    cached = redis_client.get('available_lots')
    if cached:
        return jsonify(eval(cached))
    lots = ParkingLot.query.all()
    result = []
    for lot in lots:
        lot_dict = lot.to_dict()
        if lot_dict['available_spots'] > 0:
            result.append(lot_dict)
    redis_client.setex('available_lots', 60, str(result))
    return jsonify(result)

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
@cross_origin(supports_credentials=True)
@user_required
def book_spot():
    data = request.get_json()
    lot_id = data.get('lot_id')
    vehicle_number = data.get('vehicle_number')
    if not lot_id or not vehicle_number:
        return jsonify({'error': 'Missing lot_id or vehicle_number'}), 400
    user_id = get_jwt_identity()
    active = Reservation.query.filter_by(user_id=user_id, status='active').first()
    if active:
        return jsonify({'error': 'You already have an active reservation'}), 400
    spot = ParkingSpot.query.filter_by(parking_lot_id=lot_id, is_occupied=False).first()
    if not spot:
        return jsonify({'error': 'No available spots in this lot'}), 400
    spot.is_occupied = True
    reservation = Reservation(
        user_id=user_id,
        parking_spot_id=spot.id,
        vehicle_number=vehicle_number,
        parking_timestamp=datetime.utcnow(),
        status='active'
    )
    db.session.add(reservation)
    db.session.commit()
    redis_client.delete('available_spots')
    redis_client.delete('available_lots')
    return jsonify(reservation.to_dict()), 201

@reservations_bp.route('/release', methods=['POST'])
@cross_origin(supports_credentials=True)
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
    reservation.leaving_timestamp = datetime.utcnow()
    reservation.status = 'completed'
    spot = ParkingSpot.query.get(reservation.parking_spot_id)
    lot = ParkingLot.query.get(spot.parking_lot_id)
    reservation.calculate_cost(spot.rate_per_hour)
    spot.is_occupied = False
    db.session.commit()
    redis_client.delete('available_spots')
    redis_client.delete('available_lots')
    return jsonify(reservation.to_dict())

@reservations_bp.route('/active', methods=['GET'])
@cross_origin(supports_credentials=True)
@user_required
def get_active_reservation():
    user_id = get_jwt_identity()
    reservation = Reservation.query.filter_by(user_id=user_id, status='active').first()
    if not reservation:
        return jsonify({'active': False})
    spot = ParkingSpot.query.get(reservation.parking_spot_id)
    lot = ParkingLot.query.get(spot.parking_lot_id) if spot else None
    reservation_data = reservation.to_dict()
    reservation_data['spot_number'] = spot.spot_number if spot else None
    reservation_data['lot_name'] = lot.name if lot else None
    return jsonify({'active': True, 'reservation': reservation_data})

@reservations_bp.route('/history', methods=['GET'])
@cross_origin(supports_credentials=True)
@user_required
def get_reservation_history():
    user_id = get_jwt_identity()
    reservations = Reservation.query.filter_by(user_id=user_id).filter(Reservation.leaving_timestamp != None).order_by(Reservation.parking_timestamp.desc()).all()
    result = []
    for r in reservations:
        spot = ParkingSpot.query.get(r.parking_spot_id)
        lot = ParkingLot.query.get(spot.parking_lot_id) if spot else None
        d = r.to_dict()
        d['spot_number'] = spot.spot_number if spot else None
        d['lot_name'] = lot.name if lot else None
        result.append(d)
    return jsonify(result)

@reservations_bp.route('/export', methods=['POST'])
@cross_origin(supports_credentials=True)
@user_required
def export_csv():
    from backend.celery_tasks import export_reservations_csv
    user_id = get_jwt_identity()
    export_reservations_csv.delay(user_id)
    return jsonify({"status": "export started"})

@reservations_bp.route('/summary', methods=['GET'])
@cross_origin(supports_credentials=True)
@user_required
def get_summary():
    user_id = get_jwt_identity()
    # Total amount spent on parking
    total_spent = db.session.query(db.func.sum(Reservation.cost)).filter_by(user_id=user_id, status='completed').scalar() or 0.0

    # Total hours parked
    total_duration_minutes = db.session.query(db.func.sum(Reservation.duration_minutes)).filter_by(user_id=user_id, status='completed').scalar() or 0
    total_hours = round(total_duration_minutes / 60, 2)

    # Number of bookings per month
    bookings_per_month = db.session.query(
        db.func.strftime('%Y-%m', Reservation.parking_timestamp),
        db.func.count(Reservation.id)
    ).filter_by(user_id=user_id, status='completed').group_by(db.func.strftime('%Y-%m', Reservation.parking_timestamp)).order_by(db.func.strftime('%Y-%m', Reservation.parking_timestamp)).all()

    # Most visited lots
    most_visited_lots = db.session.query(
        ParkingLot.name,
        db.func.count(Reservation.id)
    ).select_from(Reservation).join(ParkingSpot, Reservation.parking_spot_id == ParkingSpot.id).join(ParkingLot, ParkingSpot.parking_lot_id == ParkingLot.id).filter(Reservation.user_id == user_id, Reservation.status == 'completed').group_by(ParkingLot.name).order_by(db.func.count(Reservation.id).desc()).limit(5).all()

    return jsonify({
        'total_spent': total_spent,
        'total_hours': total_hours,
        'bookings_per_month': dict(bookings_per_month),
        'most_visited_lots': dict(most_visited_lots)
    })
