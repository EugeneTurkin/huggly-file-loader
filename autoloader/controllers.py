from __future__ import annotations

import os

from django.conf import settings

from autoloader.forms import UploadDataForm


# def get_upload_data() -> dict:
#     storage = [file.name for file in os.scandir(settings.STORAGE_DIR) if file.is_file()]
#     context = dict(storage=storage)
#     return context

def get_upload_data() -> dict:
    return dict(form=UploadDataForm)

def upload_file():
    ...
