# Generated by Django 4.1.6 on 2023-06-26 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0004_alter_token_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token',
            name='duration',
        ),
    ]
