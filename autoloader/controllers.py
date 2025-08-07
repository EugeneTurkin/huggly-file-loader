from __future__ import annotations

import os

from django.conf import settings


def upload() -> dict:
    storage = [file.name for file in os.scandir(settings.STORAGE_DIR_PATH) if file.is_file()]
    context = dict(storage=storage)
    return context
