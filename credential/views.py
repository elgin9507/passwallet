from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics, status, views
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Credential, CredentialLog
from .serializers import (
    AdminCredentialSerializer,
    CredentialLogSerializer,
    CredentialReadSerializer,
    CredentialTypeSerializer,
    EmailCredentialSerializer,
    FTPCredentialSerializer,
    SSHCredentialSerializer,
)
from .utils import get_cred_type_serializer_map

CRED_TYPE_SERIALIZER_MAP = get_cred_type_serializer_map()


class CredentialTypesView(views.APIView):
    def get(self, request):
        cred_types = dict(Credential._meta.get_field("cred_type").choices)

        return Response(data=cred_types, status=status.HTTP_200_OK)


class AddCredentialView(views.APIView):
    def post(self, request, *args, **kwargs):
        type_serializer = CredentialTypeSerializer(data=request.data)
        type_serializer.is_valid(raise_exception=True)
        credential_type = type_serializer.validated_data["cred_type"]
        cred_serializer_class = CRED_TYPE_SERIALIZER_MAP[credential_type]
        cred_serializer = cred_serializer_class(data=request.data)
        cred_serializer.is_valid(raise_exception=True)
        instance = cred_serializer.save(user=request.user, cred_type=credential_type)
        self.email_user(instance)
        CredentialLog.add_log(instance, CredentialLog.LOG_ACTION_CREATE)
        response_data = CredentialReadSerializer(instance=instance).data

        return Response(data=response_data, status=status.HTTP_201_CREATED)

    def email_user(self, new_credential):
        message = (
            f"You have successfully added new {new_credential.get_cred_type_display()}"
        )

        send_mail(
            subject="New credential",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.request.user.email],
            fail_silently=True,
        )


class CredentialListView(generics.ListAPIView):
    serializer_class = CredentialReadSerializer

    def get_queryset(self):
        return self.request.user.credentials.all()


class CredentialRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "id"

    def get_queryset(self):
        return self.request.user.credentials.all()

    def get_serializer_class(self):
        cred = self.get_object()
        cred_type = cred.cred_type
        serializer_class = CRED_TYPE_SERIALIZER_MAP[cred_type]

        return serializer_class

    def perform_update(self, serializer):
        super().perform_update(serializer)
        instance = serializer.instance
        self.email_user(instance, "update")
        CredentialLog.add_log(
            instance,
            CredentialLog.LOG_ACTION_UPDATE,
            list(serializer.validated_data.keys()),
        )

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self.email_user(instance, "delete")
        CredentialLog.add_log(instance, CredentialLog.LOG_ACTION_DELETE)

    def email_user(self, instance, action):
        cred_type = instance.get_cred_type_display()
        if action == "update":
            subject = "Credential update"
            message = f"You have successfully updated your {cred_type} credential"
        elif action == "delete":
            subject = "Credential delete"
            message = f"You have successfully deleted your {cred_type} credential"
        else:
            raise ValueError("unknown action")

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.request.user.email],
            fail_silently=True,
        )


class CredentialHistoryView(generics.ListAPIView):
    serializer_class = CredentialLogSerializer

    def get_queryset(self):
        cred = self.get_credential()
        logs = cred.logs.all()

        return logs

    def get_credential(self):
        qs = self.request.user.credentials.all()
        cred = get_object_or_404(qs, pk=self.kwargs["id"])

        return cred
