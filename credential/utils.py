def get_cred_type_serializer_map():
    from .models import Credential
    from .serializers import (AdminCredentialSerializer,
                              EmailCredentialSerializer,
                              FTPCredentialSerializer, SSHCredentialSerializer)

    return {
        Credential.TYPE_FTP: FTPCredentialSerializer,
        Credential.TYPE_SSH: SSHCredentialSerializer,
        Credential.TYPE_ADMIN: AdminCredentialSerializer,
        Credential.TYPE_EMAIL: EmailCredentialSerializer,
    }
