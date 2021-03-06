# Generated by Django 3.2.3 on 2021-05-23 08:40

import django_cryptography.fields
from django.db import migrations, models

import credential.validators


class Migration(migrations.Migration):

    dependencies = [
        ('credential', '0004_auto_20210523_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credential',
            name='ftp_port',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, default=1, max_length=5, validators=[credential.validators.MinIntValidator(1)])),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='credential',
            name='ssh_port',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, default=1, max_length=5, validators=[credential.validators.MinIntValidator(1)])),
            preserve_default=False,
        ),
    ]
