import os
from celery.schedules import crontab

class Config:
    CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_BEAT_SCHEDULE = {
        'send-daily-reminders': {
            'task': 'backend.celery_tasks.send_daily_reminders',
            'schedule': crontab(hour=9, minute=0),
            'options': {'expires': 60*60}
        },
        'send-monthly-report': {
            'task': 'backend.celery_tasks.send_monthly_report',
            'schedule': crontab(minute=0, hour=10, day_of_month=1),
            'options': {'expires': 60*60*2}
        }
    }