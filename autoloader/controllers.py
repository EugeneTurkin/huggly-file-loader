from __future__ import annotations

import os

from django.conf import settings


def get_upload_data() -> dict:
    storage = [file.name for file in os.scandir(settings.STORAGE_DIR_PATH) if file.is_file()]
    context = dict(storage=storage)
    return context


def upload_file():
    ...
