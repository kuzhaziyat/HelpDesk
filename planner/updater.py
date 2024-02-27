from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .sender_tg_message import mailing_by_timer

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(mailing_by_timer, 'cron', hour=22, minute='*/35',)
    scheduler.start()