from django.core.mail import send_mail
from distribution.models import

def send_dist():
    # ваша логика отправки email-рассылки
    send_mail(
        'Subject here',
        'Here is the message.',
        'from@example.com',
        ['to@example.com'],
        fail_silently=False,
    )