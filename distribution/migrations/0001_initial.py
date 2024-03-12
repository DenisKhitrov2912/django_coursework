# Generated by Django 5.0.3 on 2024-03-12 14:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('name', models.CharField(max_length=200, verbose_name='имя')),
                ('surname', models.CharField(max_length=200, verbose_name='фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=200, null=True, verbose_name='отчество')),
                ('comment', models.TextField(verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=200, verbose_name='тема письма')),
                ('message', models.TextField(verbose_name='письмо')),
            ],
            options={
                'verbose_name': 'письмо',
                'verbose_name_plural': 'письма',
            },
        ),
        migrations.CreateModel(
            name='TrySending',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_date', models.DateField(auto_now_add=True, verbose_name='дата последней попытки')),
                ('last_time', models.TimeField(auto_now_add=True, verbose_name='время последней попытки')),
                ('status', models.CharField(max_length=10, verbose_name='статус')),
                ('error_message', models.TextField(blank=True, null=True, verbose_name='сообщение об ошибке')),
            ],
            options={
                'verbose_name': 'попытка',
                'verbose_name_plural': 'попытки',
            },
        ),
        migrations.CreateModel(
            name='DistributionParams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='дата отправки')),
                ('time', models.TimeField(verbose_name='время отправки')),
                ('period', models.CharField(max_length=7, verbose_name='периодичность')),
                ('status', models.CharField(max_length=10, verbose_name='статус')),
                ('clients', models.ManyToManyField(to='distribution.clients', verbose_name='клиент')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distribution.message', verbose_name='сообщение')),
                ('try_sending', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distribution.trysending', verbose_name='попытка отправки')),
            ],
            options={
                'verbose_name': 'настройка',
                'verbose_name_plural': 'настройки',
            },
        ),
    ]
