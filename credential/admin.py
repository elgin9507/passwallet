from django.contrib import admin

from .models import Credential


@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    list_display = ("user", "cred_type", "created_at", "updated_at")
    list_select_related = ("user",)
    search_fields = ("user__email",)
    list_filter = ("cred_type",)
