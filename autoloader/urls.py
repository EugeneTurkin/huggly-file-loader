from django.urls import path

from autoloader import views


urlpatterns = [
    path("", views.index, name = "index"),
    path("download_file", views.download_file, name="download_file"),
]
