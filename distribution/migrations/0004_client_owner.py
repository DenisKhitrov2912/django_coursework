# Generated by Django 4.2 on 2024-03-28 09:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('distribution', '0003_alter_mailingsettings_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owner_client', to=settings.AUTH_USER_MODEL, verbose_name='владелец'),
        ),
    ]
