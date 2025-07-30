#!/bin/bash

echo "🔁 Starting Redis..."
brew services start redis

echo "📦 Setting up Python backend..."

cd vehicle-parking-app

# Create virtual environment if not exists
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip & install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=development
export FLASK_DEBUG=1

# Start Flask backend in background
echo "🚀 Starting Flask backend..."
nohup python3 app.py > backend.log 2>&1 &

# Start Celery worker silently in background
echo "⚙️  Starting Celery worker..."
nohup celery -A backend.celery_worker.celery worker --loglevel=info > celery.log 2>&1 &

echo "🌐 Setting up frontend..."

cd frontend

# Install Node dependencies if not already installed
if [ ! -d "node_modules" ]; then
  npm install
fi

# Build frontend (optional for dev)
npm run build

# Run frontend dev server
npm run dev