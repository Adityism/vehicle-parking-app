from datetime import datetime
from . import db

class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parking_spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=False)
    parking_timestamp = db.Column(db.DateTime, nullable=False)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    duration_minutes = db.Column(db.Integer, default=0)
    cost = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    def calculate_cost(self, rate_per_hour):
        if self.leaving_timestamp and self.parking_timestamp:
            duration = (self.leaving_timestamp - self.parking_timestamp).total_seconds() / 60
            self.duration_minutes = int(duration)
            hours = duration / 60
            self.cost = round(hours * rate_per_hour, 2)
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'parking_spot_id': self.parking_spot_id,
            'vehicle_number': self.vehicle_number,
            'parking_timestamp': self.parking_timestamp.isoformat() if self.parking_timestamp else None,
            'leaving_timestamp': self.leaving_timestamp.isoformat() if self.leaving_timestamp else None,
            'duration_minutes': self.duration_minutes,
            'cost': self.cost,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
