from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.http import require_http_methods

from autoloader import controllers


if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse, HttpResponseRedirect


require_http_methods(["GET"])
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


class Upload(View):
    http_method_names = ["get", "post"]

    def get(self, request: HttpRequest) -> HttpResponse:
        context = controllers.get_upload_data()
        
        return render(
            request,
            "autoloader/upload/submit_data.html",
            context=context,
        )
    
    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        # something = request[data]
        # controllers.upload_file(something)
        
        return redirect(
            "submit_upload_data",
            permanent=True,
            preserve_request=False,
        )


# require_http_methods(["GET"])
# def tasks_list(request: HttpRequest) -> HttpResponse:
#     context = controllers.upload_file()
#     return render(request, "autoloader/upload/execute.html", context=context)
