# Generated by Django 3.2.3 on 2021-05-23 07:55

import django.db.models.deletion
import django_cryptography.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cred_type', models.PositiveSmallIntegerField(choices=[(1, 'ftp'), (2, 'ssh'), (3, 'admin'), (4, 'email')])),
                ('ftp_host', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=500))),
                ('ftp_username', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=200))),
                ('ftp_password', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=500))),
                ('ftp_port', django_cryptography.fields.encrypt(models.DecimalField(decimal_places=0, max_digits=1, null=True))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credentials', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]