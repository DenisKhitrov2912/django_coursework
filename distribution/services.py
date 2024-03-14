from smtplib import SMTPException

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from distribution.models import MailingSettings, Log


def send_mailling(mailing, messages, clients):
    now = timezone.localtime(timezone.now())
    for object in mailing.objects.all():
        if object.start_time <= now <= object.end_time:
            for client in clients.objects.all():
                for message in messages.objects.all():
                    try:
                        result = send_mail(
                            subject=message.title,
                            message=message.text,
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[client.email],
                            fail_silently=False
                        )
                        log = Log.objects.create(
                            time=mailing.start_time,
                            status=result,
                            server_response='OK',
                            mailing_list=object,
                            client=client
                        )
                        log.save()
                        return log
                    except SMTPException as error:
                        log = Log.objects.create(
                            time=mailing.start_time,
                            status=False,
                            server_response=error,
                            mailing_list=object,
                            client=client
                        )
                        log.save()
                    return log
        else:
            mailing.status = MailingSettings.COMPLETED
            mailing.save()
