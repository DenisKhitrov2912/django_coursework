# Generated by Django 4.2 on 2024-03-27 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_content_manager',
        ),
    ]
