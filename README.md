# Vehicle Parking App - MAD II

This is a full-stack web application developed as part of the Modern Application Development II course (CS2006) at IIT Madras.

## Features
- Multi-user system (Admin + Users)
- Parking lot and spot management
- Spot reservation and release
- Charts, analytics, and batch jobs

## Frameworks Used
- Flask
- VueJS
- Bootstrap
- SQLite
- Redis + Celery

brew install redis
brew services start redis

cd vehicle-parking-app

cd vehicle-parking-app && cd frontend && npm run build && npm run dev
cd vehicle-parking-app && export FLASK_ENV=development && export FLASK_DEBUG=1 && python3 app.py


      "email": "admin@parking.com",
        "password": "admin123"

 cd vehicle-parking-app
source .venv/bin/activate
celery -A backend.celery_worker.celery worker --loglevel=info 
ps aux | grep 'celery'