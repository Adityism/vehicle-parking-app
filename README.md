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

cd frontend && npm run build && npm run dev
export FLASK_ENV=development && export FLASK_DEBUG=1 && python3 app.py
export $(cat .env | xargs) && celery -A backend.celery_tasks.celery worker --loglevel=info
