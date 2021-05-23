from django.urls import path

from . import views

app_name = "credential"

urlpatterns = [
    path("cred-types/", views.CredentialTypesView.as_view(), name="cred_types"),
    path("add_credential/", views.AddCredentialView.as_view(), name="add_credential"),
    path("credentials/", views.CredentialListView.as_view(), name="credential_list"),
    path(
        "credential/<int:id>/",
        views.CredentialRetrieveUpdateDestroyView.as_view(),
        name="credential_retrieve_update_delete",
    ),
    path(
        "credential/<int:id>/history/",
        views.CredentialHistoryView.as_view(),
        name="history",
    ),
]
