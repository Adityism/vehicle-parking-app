from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.user import User
from models.reservation import Reservation
from functools import wraps
from redis_client import redis_client
from backend.celery_tasks import export_reservations_csv

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
    redis_client.delete('available_lots')
    return jsonify(lot.to_dict()), 201

@admin_bp.route('/lots', methods=['GET'])
@admin_required
def list_lots():
    q = request.args.get('q', '').strip()
    lots_query = ParkingLot.query
    if q:
        like_q = f"%{q}%"
        lots_query = lots_query.filter(
            (ParkingLot.name.ilike(like_q)) |
            (ParkingLot.address.ilike(like_q)) |
            (ParkingLot.address.ilike(like_q))
        )
    lots = lots_query.all()
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
    redis_client.delete('available_lots')
    return jsonify(lot.to_dict())

@admin_bp.route('/lots/<int:lot_id>', methods=['DELETE'])
@admin_required
def delete_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    db.session.delete(lot)
    db.session.commit()
    redis_client.delete('available_lots')
    return jsonify({'message': 'Parking lot deleted'})

@admin_bp.route('/lots/<int:lot_id>/spots', methods=['GET'])
@admin_required
def list_spots(lot_id):
    status = request.args.get('status', '').strip().lower()
    spots_query = ParkingSpot.query.filter_by(parking_lot_id=lot_id)
    if status == 'available':
        spots_query = spots_query.filter_by(is_occupied=False)
    elif status == 'occupied':
        spots_query = spots_query.filter_by(is_occupied=True)
    spots = spots_query.all()
    return jsonify([spot.to_dict() for spot in spots])

@admin_bp.route('/users', methods=['GET'])
@admin_required
def list_users():
    q = request.args.get('q', '').strip()
    users_query = User.query
    if q:
        like_q = f"%{q}%"
        users_query = users_query.filter(
            (User.name.ilike(like_q)) |
            (User.email.ilike(like_q))
        )
    users = users_query.all()
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

@admin_bp.route('/lots/available', methods=['GET'])
def available_lots():
    cached = redis_client.get('available_lots')
    if cached:
        return jsonify(eval(cached))
    lots = ParkingLot.query.all()
    result = [lot.to_dict() for lot in lots if lot.available_spots > 0]
    redis_client.setex('available_lots', 60, str(result))
    return jsonify(result)

@admin_bp.route('/spots/available', methods=['GET'])
def available_spots():
    cached = redis_client.get('available_spots')
    if cached:
        return jsonify(eval(cached))
    spots = ParkingSpot.query.filter_by(is_occupied=False).all()
    result = [spot.to_dict() for spot in spots]
    redis_client.setex('available_spots', 60, str(result))
    return jsonify(result)

@admin_bp.route('/export/csv', methods=['POST'])
@admin_required
def export_csv():
    export_reservations_csv.delay()
    return jsonify({"status": "export started"})
