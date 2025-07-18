from django.urls import path

from autoloader import views


urlpatterns = [
    path("", views.index, name = "index"),
    path("download_start", views.index1, name = "index1"),
    path("download_file", views.download_file, name="download_file"),
    path("upload", views.upload_file_to_yandex_disk, name="upload_file_to_yandex_disk"),
    path("upload_final", views.upload_file_to_yandex_disk_final, name="upload_file_to_yandex_disk_final"),
    path("upload_final_final", views.yapload, name="yapload"),
    path("sentry-debug/", views.trigger_error)
]
