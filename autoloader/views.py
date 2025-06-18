import os

from django.conf import settings
from django.shortcuts import render

from autoloader.loader_utils import FileLoader


def index(request):
    network_disk = settings.STORAGE_PATH  # TODO: явно указать файл с настройками
    
    if not os.access(network_disk, os.F_OK):  # TODO: check whether Z:/ is online properly
        raise Exception("Target path is unavailiable or doesn't exist")
    
    existing_dirs = os.listdir(network_disk)
    context_index = {
        "existing_dirs": existing_dirs,
    }
    return render(request, "autoloader/index.html", context_index)


def download_file(request):
    network_disk = settings.STORAGE_PATH
    file_loader = FileLoader(
        file_repo=settings.DOWNLOADS_PATH,
        yandex_resource_download_endp=settings.YANDEX_RESOURCE_DOWNLOAD_ENDP,
        yandex_resource_meta_endp=settings.YANDEX_RESOURCE_METADATA_ENDP,
    )
    sourcelink = request.POST["sourcelink"]
    destdir = network_disk / request.POST["destdir"]
    context_download_file = {
        "sourcelink": sourcelink,
        "destdir": destdir,
    }
    
    file_loader.download(link=sourcelink, dir=destdir)
    
    return render(
        request,
        "autoloader/download_file.html",
        context_download_file,
    )
