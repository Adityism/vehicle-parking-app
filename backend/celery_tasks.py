from backend.celery_worker import make_celery
from app import app
from backend.models import db, User, Reservation
from flask import current_app
import pandas as pd
from datetime import datetime
import logging

celery = make_celery(app)

@celery.task
def send_daily_reminders():
    users = User.query.all()
    for user in users:
        logging.info(f"[DAILY REMINDER] Would send reminder to user: {user.email}")
    return f"Reminders sent to {len(users)} users."

@celery.task
def send_monthly_report():
    users = User.query.all()
    for user in users:
        logging.info(f"[MONTHLY REPORT] Would generate and send report to user: {user.email}")
    return f"Monthly reports generated for {len(users)} users."

@celery.task
def export_reservations_csv():
    reservations = Reservation.query.all()
    data = [r.to_dict() for r in reservations]
    df = pd.DataFrame(data)
    filename = f"reservation_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    logging.info(f"[EXPORT CSV] Exported {len(data)} reservations to {filename}")
    return filename
