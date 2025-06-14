from datetime import datetime
from . import db

class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'
    
    id = db.Column(db.Integer, primary_key=True)
    spot_number = db.Column(db.String(10), nullable=False)
    parking_lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False)
    vehicle_type = db.Column(db.String(20), nullable=False)  # car, bike, etc.
    rate_per_hour = db.Column(db.Float, nullable=False)
    is_occupied = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    reservations = db.relationship('Reservation', backref='parking_spot', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'spot_number': self.spot_number,
            'parking_lot_id': self.parking_lot_id,
            'vehicle_type': self.vehicle_type,
            'rate_per_hour': self.rate_per_hour,
            'is_occupied': self.is_occupied,
            'created_at': self.created_at.isoformat()
        }
