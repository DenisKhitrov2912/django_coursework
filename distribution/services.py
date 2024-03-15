from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command


def sending_mail():
    call_command('sending_mail')


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(sending_mail, 'interval', minutes=10)
    scheduler.start()


start()
