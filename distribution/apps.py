from asyncio import sleep

from django.apps import AppConfig


class DistributionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'distribution'

    def ready(self):
        from distribution.models import MailingSettings, Client, Message
        from distribution.services import send_mailling
        sleep(2)
        send_mailling(mailing=MailingSettings, clients=Client, messages=Message)
