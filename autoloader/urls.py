from django.urls import path

from autoloader import views


urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.upload, name="submit_upload_data"),
    path("upload/", views.upload, name="upload_file"),
]
