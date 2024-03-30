from django.core.management.base import BaseCommand
import smtplib
from datetime import datetime, timedelta
import pytz
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from distribution.models import MailingSettings, Log, Client, Message


class Command(BaseCommand):
    """Команда на запуск рассылки"""
    help = 'send_of_mail'
    name = 'sending_mail'

    def handle(self, *args, **options):
        try:
            zone = pytz.timezone(settings.TIME_ZONE)
            current_datetime = datetime.now(zone)
            for mailing in MailingSettings.objects.all():
                if mailing.end_time < current_datetime:
                    mailing.status = MailingSettings.COMPLETED
                    mailing.save()
            mailings = MailingSettings.objects.filter(start_time__lte=current_datetime).filter(
                end_time__gte=current_datetime).filter(
                status__in=[MailingSettings.CREATED])

            for mailing in mailings:
                mailing.status = MailingSettings.STARTED
                try:
                    send_mail(
                        subject=Message.objects.get(pk=mailing.id).title,
                        message=Message.objects.get(pk=mailing.id).text,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email for client in mailing.clients.all()],
                        fail_silently=False
                    )
                    server_response = 'ok'
                    status = True
                except smtplib.SMTPException as e:
                    server_response = str(e)
                    status = False
                finally:
                    for client in mailing.clients.all():
                        log = Log.objects.create(
                            time=timezone.localtime(timezone.now()),
                            status=status,
                            server_response=server_response,
                            mailing_list=mailing,
                            client=client
                        )
                        log.save()
                if mailing.periodicity == MailingSettings.DAILY:
                    mailing.start_time += timedelta(days=1)
                elif mailing.periodicity == MailingSettings.WEEKLY:
                    mailing.start_time += timedelta(days=7)
                elif mailing.periodicity == MailingSettings.MONTHLY:
                    mailing.start_time += timedelta(days=30)
                mailing.status = MailingSettings.CREATED
                mailing.save()
        except Exception:
            pass
