from django.urls import include, path
from django.views.decorators.http import require_http_methods

from autoloader import views


urlpatterns = [
    path("", views.index, name="index"),
    path(
        "upload/", include(
            [
                path("", views.submit_upload_data, name="submit_upload_data"),
                path("/execute", views.execute_upload, name="execute_upload"),
            ]
        )
    ),
]
