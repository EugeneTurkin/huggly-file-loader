from django.urls import include, path

from autoloader import views


# urlpatterns = [
#     path("", views.index, name="index"),
#     path("upload/", views.upload, name="submit_upload_data"),
#     path("upload/", views.upload, name="upload_file"),
# ]

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "upload/", include(
            [
                path("", views.submit_upload_data, name="submit_upload_data"),
                path("execute/", views.upload_file_by_data, name="upload_file"),
            ]
        )
    ),
]
