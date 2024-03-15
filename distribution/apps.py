from asyncio import sleep

from django.apps import AppConfig


class DistributionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'distribution'

    def ready(self):
        from distribution.services import sending_mail
        sleep(2)
        sending_mail()
