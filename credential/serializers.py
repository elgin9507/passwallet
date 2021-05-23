from rest_framework import generics, serializers

from .models import Credential, CredentialLog
from .validators import MinIntValidator


class CredentialTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = ("cred_type",)


class CredentialReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = ("user", "cred_type", "created_at", "updated_at")

    def to_representation(self, instance):
        from .utils import get_cred_type_serializer_map

        data = super().to_representation(instance)
        serializer_map = get_cred_type_serializer_map()
        serializer_class = serializer_map[instance.cred_type]
        credential_data = serializer_class(instance=instance).data

        data.update(credential_data)

        return data


class FTPCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = ("id", "ftp_host", "ftp_username", "ftp_password", "ftp_port")
        extra_kwargs = {
            "ftp_host": {"allow_blank": False, "read_only": False},
            "ftp_username": {"allow_blank": False, "read_only": False},
            "ftp_password": {"allow_blank": False, "read_only": False},
            "ftp_port": {
                "allow_blank": False,
                "read_only": False,
                "validators": [MinIntValidator(1)],
            },
        }


class SSHCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = ("id", "ssh_host", "ssh_username", "ssh_password", "ssh_port")
        extra_kwargs = {
            "ssh_host": {"allow_blank": False, "read_only": False},
            "ssh_username": {"allow_blank": False, "read_only": False},
            "ssh_password": {"allow_blank": False, "read_only": False},
            "ssh_port": {
                "allow_blank": False,
                "read_only": False,
                "validators": [MinIntValidator(1)],
            },
        }


class AdminCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = ("id", "admin_url", "admin_username", "admin_password")
        extra_kwargs = {
            "admin_url": {"allow_blank": False, "read_only": False},
            "admin_username": {"allow_blank": False, "read_only": False},
            "admin_password": {"allow_blank": False, "read_only": False},
        }


class EmailCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = ("id", "email_name", "email_username", "email_password")
        extra_kwargs = {
            "email_name": {"allow_blank": False, "read_only": False},
            "email_username": {"allow_blank": False, "read_only": False},
            "email_password": {"allow_blank": False, "read_only": False},
        }


class CredentialLogSerializer(serializers.ModelSerializer):
    action = serializers.SerializerMethodField()

    class Meta:
        model = CredentialLog
        fields = ("action", "message", "entry_added_at")

    def get_action(self, instance):
        return instance.get_action_display()
