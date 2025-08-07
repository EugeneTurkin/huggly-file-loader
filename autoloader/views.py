from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.decorators.http import require_http_methods

from autoloader import controllers


if TYPE_CHECKING:
    from django.http import HttpRequest


require_http_methods(["GET"])
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


require_http_methods(["GET"])
def upload(request: HttpRequest) -> HttpResponse:
    context = controllers.upload()
    return render(request, "autoloader/upload.html", context=context)


class Files(View):
    def get(self, request):
        ...
    
    def post(self, request):
        ...
