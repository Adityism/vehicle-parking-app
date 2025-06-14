from datetime import datetime
from . import db

class Reservation(db.Model):
    __tablename__ = 'reservations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parking_spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    total_cost = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def calculate_cost(self):
        if self.end_time and self.start_time:
            duration = (self.end_time - self.start_time).total_seconds() / 3600  # hours
            self.total_cost = round(duration * self.parking_spot.rate_per_hour, 2)
            
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'parking_spot_id': self.parking_spot_id,
            'vehicle_number': self.vehicle_number,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'total_cost': self.total_cost,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
