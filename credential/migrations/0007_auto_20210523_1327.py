# Generated by Django 3.2.3 on 2021-05-23 13:27

import django.db.models.deletion
import django_cryptography.fields
from django.db import migrations, models

import credential.validators


class Migration(migrations.Migration):

    dependencies = [
        ('credential', '0006_auto_20210523_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credential',
            name='admin_password',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, editable=False, max_length=500)),
        ),
        migrations.AlterField(
            model_name='credential',
            name='admin_url',
            field=django_cryptography.fields.encrypt(models.URLField(blank=True, editable=False)),
        ),
        migrations.AlterField(
            model_name='credential',
            name='admin_username',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, editable=False, max_length=100)),
        ),
        migrations.AlterField(
            model_name='credential',
            name='email_name',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, editable=False, max_length=100)),
        ),
        migrations.AlterField(
            model_name='credential',
            name='email_password',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, editable=False, max_length=200)),
        ),
        migrations.AlterField(
            model_name='credential',
            name='email_username',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, editable=False, max_length=100)),
        ),
        migrations.AlterField(
            model_name='credential',
            name='ftp_host',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, editable=False, max_length=500)),
        ),
        migrations.AlterField(
            model_name='credential',
            name='ftp_password',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, editable=False, max_length=500)),
        ),
        migrations.AlterField(
            model_name='credential',
            name='ftp_port',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, editable=False, max_length=5, validators=[credential.validators.MinIntValidator(1)])),
        ),
        migrations.AlterField(
            model_name='credential',
            name='ftp_username',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, editable=False, max_length=200)),
        ),
        migrations.AlterField(
            model_name='credential',
            name='ssh_host',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, editable=False, max_length=500)),
        ),
        migrations.AlterField(
            model_name='credential',
            name='ssh_password',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, editable=False, max_length=500)),
        ),
        migrations.AlterField(
            model_name='credential',
            name='ssh_port',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, editable=False, max_length=5, validators=[credential.validators.MinIntValidator(1)])),
        ),
        migrations.AlterField(
            model_name='credential',
            name='ssh_username',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, editable=False, max_length=200)),
        ),
        migrations.CreateModel(
            name='CredentialLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.SmallIntegerField(choices=[(1, 'create'), (2, 'update'), (3, 'delete')])),
                ('message', models.CharField(max_length=200)),
                ('entry_added_at', models.DateTimeField(auto_now_add=True)),
                ('credential', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='logs', to='credential.credential')),
            ],
        ),
    ]