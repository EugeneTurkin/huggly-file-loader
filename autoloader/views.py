from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from autoloader import forms, models


if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse, HttpResponsePermanentRedirect


@require_http_methods(["GET"])
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


@require_http_methods(["GET"])
def submit_upload_data(request):
    initial = dict(source=settings.STORAGE_DIR,
                   notification_recipient="vesti@komigor.com",
                   destination=models.UploadTask.Destination.YANDEX)
    form = forms.UploadDataForm(initial=initial)
    
    return render(
        request=request,
        template_name="autoloader/upload/submit_data.html",
        context=dict(form=form),
    )


@require_http_methods(["POST"])
def execute_upload(request: HttpRequest) -> HttpResponsePermanentRedirect:
    new_task = models.UploadTask(
        owner="admin",
        action=models.Task.Action.UPLOAD,
        status=models.Task.Status.IN_PROGRESS,
    )
    form = forms.UploadDataForm(request.POST, instance=new_task)
    

    if form.is_valid():
        try:
            form.instance.full_clean()
        except:
            print("500 internal server error")
        else:
            form.save()

    return redirect(
        "submit_upload_data",
        permanent=True,
        preserve_request=False,
    )
