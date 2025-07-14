import logging
import os

from django.conf import settings
from django.shortcuts import render

from autoloader.loader_utils import FileLoader


logger = logging.getLogger(__name__)

def trigger_error(request):
    division_by_zero = 1 / 0


def index(request):
    destination_path = settings.STORAGE_PATH
    
    if not os.access(destination_path, os.F_OK):
        logger.error("Путь назначения недоступен: проверьте конфигурацию и состояние хранилища")
        raise Exception("Target path is unavailiable or doesn't exist")
    if not os.access(destination_path, os.X_OK) or not os.access(destination_path, os.W_OK):
        logger.warning("Похоже, сервер приложения не обладает полными правами в указанном пути назначения!")
    else:
        logger.info("Путь назначения доступен с полными правами")
    
    existing_dirs = os.listdir(destination_path)
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


def upload_file_to_yandex_disk(request):
    network_disk = settings.STORAGE_PATH  # TODO: явно указать файл с настройками
    
    if not os.access(network_disk, os.F_OK):  # TODO: check whether Z:/ is online properly
        raise Exception("Target path is unavailiable or doesn't exist")
    
    existing_dirs = os.listdir(network_disk)
    context = {
        "existing_dirs": existing_dirs,
    }
    return render(request, "autoloader/upload.html", context)


def upload_file_to_yandex_disk_final(request):
    network_disk = settings.STORAGE_PATH  # TODO: явно указать файл с настройками
    fpath = request.POST["destdir"]
    
    existing_files = os.listdir(network_disk / fpath)
    context1 = {
        "chosen_dir": fpath,
        "existing_dirs": existing_files,
    }
    return render(request, "autoloader/upload_meta.html", context1)


def yapload(request):
    network_disk = settings.STORAGE_PATH  # TODO: явно указать файл с настройками
    src = request.POST["chosen"]
    fpath = request.POST["fpath"]
    src = network_disk / src / fpath
    destemail = request.POST["destemail"]
    from autoloader.tasks import upload_to_yandex

    upload_to_yandex(fpath, destemail, src)
    context = {
        "destdir": fpath,
        "sourcelink": destemail,
    }
    return render(
        request,
        "autoloader/download_file1.html",
        context,
    )
