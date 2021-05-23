from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_cryptography.fields import encrypt

from .validators import MinIntValidator

User = get_user_model()


class Credential(models.Model):
    TYPE_FTP = 1
    TYPE_SSH = 2
    TYPE_ADMIN = 3
    TYPE_EMAIL = 4

    CRED_TYPES = (
        (TYPE_FTP, _("ftp")),
        (TYPE_SSH, _("ssh")),
        (TYPE_ADMIN, _("admin")),
        (TYPE_EMAIL, _("email")),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="credentials")
    cred_type = models.PositiveSmallIntegerField(choices=CRED_TYPES)

    # ftp credential fields
    ftp_host = encrypt(models.CharField(max_length=500, blank=True, editable=False))
    ftp_username = encrypt(models.CharField(max_length=200, blank=True, editable=False))
    ftp_password = encrypt(models.CharField(max_length=500, blank=True, editable=False))
    ftp_port = encrypt(
        models.CharField(
            max_length=5, blank=True, validators=[MinIntValidator(1)], editable=False
        )
    )
    # ssh credential fields
    ssh_host = encrypt(models.CharField(max_length=500, blank=True, editable=False))
    ssh_username = encrypt(models.CharField(max_length=200, blank=True, editable=False))
    ssh_password = encrypt(models.CharField(max_length=500, blank=True, editable=False))
    ssh_port = encrypt(
        models.CharField(
            max_length=5, blank=True, validators=[MinIntValidator(1)], editable=False
        )
    )
    # admin credential fields
    admin_url = encrypt(models.URLField(blank=True, editable=False))
    admin_username = encrypt(
        models.CharField(max_length=100, blank=True, editable=False)
    )
    admin_password = encrypt(
        models.CharField(max_length=500, blank=True, editable=False)
    )
    # email credential fields
    email_name = encrypt(models.CharField(max_length=100, blank=True, editable=False))
    email_username = encrypt(
        models.CharField(max_length=100, blank=True, editable=False)
    )
    email_password = encrypt(
        models.CharField(max_length=200, blank=True, editable=False)
    )

    # date tracking fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_cred_type_display()


class CredentialLog(models.Model):
    LOG_ACTION_CREATE = 1
    LOG_ACTION_UPDATE = 2
    LOG_ACTION_DELETE = 3

    LOG_ACTION_CHOICES = (
        (LOG_ACTION_CREATE, _("create")),
        (LOG_ACTION_UPDATE, _("update")),
        (LOG_ACTION_DELETE, _("delete")),
    )

    credential = models.ForeignKey(
        "credential.Credential",
        null=True,
        on_delete=models.SET_NULL,
        related_name="logs",
    )
    action = models.SmallIntegerField(choices=LOG_ACTION_CHOICES)
    message = models.CharField(max_length=200)
    entry_added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_action_display()

    @classmethod
    def add_log(cls, credential, action, updated_fields=None):
        valid_actions = [c[0] for c in cls._meta.get_field("action").choices]
        assert action in valid_actions, "unknown action"
        if action == cls.LOG_ACTION_UPDATE:
            assert (
                updated_fields is not None
            ), "updated fields must be specified for update log"

        action_message_getter_map = {
            cls.LOG_ACTION_CREATE: lambda: "added.",
            cls.LOG_ACTION_UPDATE: lambda: f"changed {','.join(updated_fields)}.",
            cls.LOG_ACTION_DELETE: lambda: "deleted.",
        }
        print(updated_fields)
        message = action_message_getter_map[action]()

        cls.objects.create(credential=credential, action=action, message=message)
