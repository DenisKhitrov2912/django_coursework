from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command


def sending_mail():
    """Вызов кастомной команды рассылки"""
    call_command('sending_mail')


def start():
    """Старт рассылки с интервалом проверки"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(sending_mail, 'interval', minutes=0.1)
    scheduler.start()


start()
