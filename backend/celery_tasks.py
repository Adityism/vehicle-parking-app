from backend.celery_worker import make_celery
from app import app
from backend.models import db
from backend.models.user import User
from backend.models.reservation import Reservation
from flask import current_app
import pandas as pd
from datetime import datetime
import logging
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os


load_dotenv()

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
def export_reservations_csv(user_id):
    with app.app_context():
        user = User.query.get(user_id)
        if not user:
            logging.error(f"[EXPORT CSV] User with ID {user_id} not found.")
            return "User not found"

        reservations = Reservation.query.filter_by(user_id=user_id).all()
        data = [r.to_dict() for r in reservations]
        df = pd.DataFrame(data)
        filename = f"reservation_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(os.getcwd(), filename) # Save in current working directory
        df.to_csv(filepath, index=False)
        logging.info(f"[EXPORT CSV] Exported {len(data)} reservations to {filename}")

        # Email sending logic
        sender_email = os.getenv('EMAIL_USER')
        sender_password = os.getenv('EMAIL_PASS')
        receiver_email = user.email

        msg = EmailMessage()
        msg['Subject'] = "Your Parking History CSV Export"
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg.set_content("Your CSV export is attached.")

        with open(filepath, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(filepath)
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender_email, sender_password)
                smtp.send_message(msg)
            logging.info(f"[EXPORT CSV] Sent CSV to {receiver_email}")
        except Exception as e:
            logging.error(f"[EXPORT CSV] Failed to send email to {receiver_email}: {e}")

        # Clean up the generated CSV file
        os.remove(filepath)

        return filename
