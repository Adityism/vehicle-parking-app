from celery import Celery
from flask import Flask
from backend.models import db
import os

def make_celery(app: Flask):
    celery = Celery(
        app.import_name,
        broker=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
        backend=os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

if __name__ == '__main__':
    from app import app
    celery = make_celery(app)
    celery.start()
