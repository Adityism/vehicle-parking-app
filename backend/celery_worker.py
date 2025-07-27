from celery import Celery
from flask import Flask, current_app
import os

# Define celery globally and tell it where to find tasks
celery = Celery(
    'vehicle-parking-app', # Use a unique name for your app
    broker=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
    backend=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
    include=['backend.celery_tasks'] # Explicitly include the tasks module
)

def make_celery(app: Flask):
    # Configure celery with app settings
    celery.conf.update(app.config)

    # Set up the context task
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery