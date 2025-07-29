from django.urls import path

from . import views

app_name = "sparkplug_avatars"

urlpatterns = [
    path(
        "upload/",
        views.UploadView.as_view(),
        name="upload",
    ),
]
