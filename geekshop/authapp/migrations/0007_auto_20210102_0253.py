# Generated by Django 3.1.4 on 2021-01-01 21:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_auto_20210102_0143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 3, 21, 53, 51, 566120, tzinfo=utc), verbose_name='актуальность ключа'),
        ),
    ]
