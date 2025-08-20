from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from autoloader import forms, models
from autoloader.file_loader import FileLoader


if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse, HttpResponsePermanentRedirect


@require_http_methods(["GET"])
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


@require_http_methods(["GET"])
def submit_upload_data(request: HttpRequest) -> HttpResponse:
    initial = dict(source=settings.STORAGE_DIR,
                   notification_recipient="vesti@komigor.com",
                   destination=models.UploadTask.Destination.YANDEX.value)
    form = forms.UploadData(initial=initial)
    
    return render(
        request=request,
        template_name="autoloader/upload/submit_data.html",
        context=dict(form=form),
    )


@require_http_methods(["POST"])
def execute_upload(request: HttpRequest) -> HttpResponsePermanentRedirect:
    file_loader = FileLoader()
    partial_upload_data = models.UploadTask(
        owner="admin",
        action=models.Task.Action.UPLOAD.value,
        status=models.Task.Status.IN_PROGRESS.value,
    )
    upload_data = forms.UploadData(request.POST, instance=partial_upload_data)
    
    if upload_data.is_valid():
        try:
            upload_data.instance.full_clean()
        except:
            raise Exception("500 internal server error: input validation failed")
        else:
            upload_data.save()
            file_loader.upload(upload_data)

    return redirect(
        "submit_upload_data",
        permanent=True,
        preserve_request=False,
    )
