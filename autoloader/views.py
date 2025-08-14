from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, FormView
from django.views.decorators.http import require_http_methods

from autoloader import controllers, forms, models


if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse, HttpResponseRedirect


require_http_methods(["GET"])
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


def submit_upload_data(request):
    initial = dict(source=settings.STORAGE_DIR, notification_recipient="vesti@komigor.com")
    form = forms.UploadDataForm(initial=initial)
    
    return render(
        request=request,
        template_name="autoloader/upload/submit_data.html",
        context=dict(form=form),
    )


def execute_upload(request):
    new_task = models.Task(
        owner="admin",
        task_type="upload",
        status="in progress",
        destination="yandex",
    )
    form = forms.UploadDataForm(request.POST, instance=new_task)
    if form.is_valid():
        print("hallelujah")
    else:
        print(":(")

    return redirect("submit_upload_data", permanent=True, preserve_request=False)


# require_http_methods(["GET"])
# def tasks_list(request: HttpRequest) -> HttpResponse:
#     context = controllers.upload_file()
#     return render(request, "autoloader/upload/execute.html", context=context)
