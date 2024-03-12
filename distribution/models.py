from django.utils import timezone
from django.db import models
from django.core.mail import send_mail
import smtplib


NULLABLE = {'blank': True, 'null': True}


class Clients(models.Model):

    email = models.EmailField(verbose_name='email')
    name = models.CharField(max_length=200, verbose_name='имя')
    surname = models.CharField(max_length=200, verbose_name='фамилия')
    patronymic = models.CharField(max_length=200, verbose_name='отчество', **NULLABLE)
    comment = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return f"{self.email}, {self.name}, {self.surname}"

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    theme = models.CharField(max_length=200, verbose_name='тема письма')
    message = models.TextField(verbose_name='письмо')

    def __str__(self):
        return f"{self.theme}"

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'


class DistributionParams(models.Model):

    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    PERIOD_CHOICES = [
        (DAILY, 'Раз в день'),
        (WEEKLY, 'Раз в неделю'),
        (MONTHLY, 'Раз в месяц'),
    ]
    DEFAULT_PERIOD = DAILY

    CREATED = 'created'
    STARTED = 'started'
    COMPLETED = 'completed'

    date = models.DateField(verbose_name='дата начала отправки')
    date_end = models.DateField(verbose_name='дата конца отправки')
    time = models.TimeField(verbose_name='время начала отправки')
    time_end = models.TimeField(verbose_name='время конца отправки')
    period = models.CharField(max_length=7, verbose_name='периодичность')
    status = models.CharField(max_length=10, verbose_name='статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение')
    clients = models.ManyToManyField(Clients, verbose_name='клиент')
    try_sending = models.ForeignKey('TrySending', on_delete=models.CASCADE, verbose_name='попытка отправки')

    def __str__(self):
        return f"{self.date}, {self.time}, {self.period}, {self.status}"

    def save(self, *args, **kwargs):
        if self.date_end > self.date > timezone.now().date() and self.time_end > self.time > timezone.now().time():
            self.status = self.STARTED
        if self.date < timezone.now().date() and self.time < timezone.now().time():
            self.status = self.CREATED
        if self.try_sending.status == 'SUCCESS':
            self.status = self.COMPLETED
        super(DistributionParams, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'настройка'
        verbose_name_plural = 'настройки'


class TrySending(models.Model):
    SUCCESS = 'Success'
    UNSUCCESS = 'Failed'
    DEFAULT_STATUS = SUCCESS
    last_date = models.DateField(auto_now_add=True, verbose_name='дата последней попытки')
    last_time = models.TimeField(auto_now_add=True, verbose_name='время последней попытки')
    status = models.CharField(max_length=10, verbose_name='статус')
    error_message = models.TextField(verbose_name='сообщение об ошибке', **NULLABLE)

    def __str__(self):
        return f"{self.last_date}, {self.last_time}, {self.status}, {self.answer}"

    def save(self, *args, **kwargs):
        mailing = DistributionParams.objects.get(pk=1)
        objects = DistributionParams.objects.all()
        try:
            send_mail(subject=Message.theme, recipient_list=[mail for mail in objects.clients.email], from_email='example@ya.ru', message=Message.message, fail_silently=False)
            attempt = TrySending(mailing=mailing, status='Success')
            attempt.save()
        except smtplib.SMTPException as e:
            attempt = TrySending(mailing=mailing, status='Failed', error_message=str(e))
            attempt.save()

    class Meta:
        verbose_name = 'попытка'
        verbose_name_plural = 'попытки'