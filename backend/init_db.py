from flask import Flask
from models import db
from models.user import User
import os

def init_db():
    app = Flask(__name__)
    
    # Configure SQLite database
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "parking.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(email='admin@parking.com').first()
        if not admin:
            # Create default admin user
            admin = User(
                email='admin@parking.com',
                name='System Administrator',
                role='admin'
            )
            admin.set_password('admin123')  # Set a default password
            db.session.add(admin)
            db.session.commit()
            print("Default admin user created successfully!")
        
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
