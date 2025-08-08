from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from autoloader import controllers


if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse, HttpResponseRedirect


require_http_methods(["GET"])
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


require_http_methods(["GET"])
def submit_upload_data(request: HttpRequest) -> HttpResponse:
    context = controllers.get_upload_data()
    return render(request, "autoloader/upload/submit_data.html", context=context)


require_http_methods(["POST"])
def upload_file_by_data(request: HttpRequest) -> HttpResponseRedirect:
    context = controllers.upload_file()
    return redirect(
        "autoloader/upload/execute.html",
        context=context,
    )


require_http_methods(["GET"])
def tasks_list(request: HttpRequest) -> HttpResponse:
    context = controllers.upload_file()
    return render(request, "autoloader/upload/execute.html", context=context)
