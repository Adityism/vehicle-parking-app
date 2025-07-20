from datetime import datetime
from . import db

class ParkingLot(db.Model):
    __tablename__ = 'parking_lots'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    spots = db.relationship('ParkingSpot', backref='parking_lot', lazy=True, cascade='all, delete-orphan')
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'capacity': self.capacity,
            'created_at': self.created_at.isoformat(),
            'available_spots': sum(1 for spot in self.spots if not spot.is_occupied)
        }
