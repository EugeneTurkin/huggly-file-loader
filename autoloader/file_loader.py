from __future__ import annotations

from abc import ABC
from pathlib import Path
from typing import TYPE_CHECKING

from django.conf import settings
import requests

from autoloader.models import UploadTask


if TYPE_CHECKING:
    from autoloader.forms import UploadData


class YandexClient:
    RESOURCE_META = "https://cloud-api.yandex.net/v1/disk/resources"
    PUBLISH = "https://cloud-api.yandex.net/v1/disk/resources/publish"
    UPLOAD = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    YANDEX_DISK_DIR = "disk:/JOB KOMIGOR/"

    def __init__(self, yandex_oauth_token):
        self._OAUTH_TOKEN = yandex_oauth_token

    def upload(self, data: dict[str, str]):
        fpath = data["source"]
        # приходится брать имя файла без расширения, т.к. загрузка файла с расширением в имени длится значительно дольше. это фича яндекс апи.
        fname = Path(fpath).stem
        
        yandex_disk_fp = self.YANDEX_DISK_DIR + fname
        headers = dict(Authorization=f"OAuth {self._OAUTH_TOKEN}")
        params = dict(path=yandex_disk_fp)

        # check whether destination is availiable and generate upload link
        with requests.get(self.UPLOAD, headers=headers, params=params) as response:
            if not response.status_code == 200:
                raise Exception("500: something wrond with yandex")  # TODO: обработать нормально, попробовать match/case
            
            upl_link = response.json().get("href")
            
        with open(fpath, "rb") as f:
            with requests.put(upl_link, data=f) as response:
                ...

        with requests.put(self.PUBLISH, headers=headers, params=params) as response:
            ...

        with requests.get(self.RESOURCE_META, headers=headers, params=params) as response:
            dl_link = response.json()["public_url"]


    def download(self):
        ...


class FileLoader:
    def __init__(self):
        self.yandex_client = YandexClient(settings.YANDEX_OAUTH_KEY)
    
    def upload(self, upload_data: UploadData):
        data = upload_data.cleaned_data
        if data.get("destination") == UploadTask.Destination.YANDEX.value:
            self.yandex_client.upload(data)
        else:
            ...
