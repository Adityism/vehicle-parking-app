from flask import Flask
from models import db
from models.user import User
import os

def init_db():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "parking.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(email='admin@parking.com').first()
        if not admin:
            admin = User(
                email='admin@parking.com',
                name='System Administrator',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Default admin user created successfully!")
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
