from abc import ABC
from pathlib import Path

import requests


class YandexClient:
    RESOURCE_META = "https://cloud-api.yandex.net/v1/disk/resources"
    PUBLISH = "https://cloud-api.yandex.net/v1/disk/resources/publish"
    UPLOAD = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    JOB_KOMIGOR = "disk:/JOB KOMIGOR/"

    def __init__(self, yandex_oauth_token):
        self._OAUTH_TOKEN = yandex_oauth_token

    def upload(self, fpath: str | Path, fname: str):
        yandex_disk_fp = self.JOB_KOMIGOR + fname
        headers = dict(Authorization=f"OAuth {self._OAUTH_TOKEN}")
        params = dict(path=yandex_disk_fp)
        with requests.get(self.UPLOAD, headers=headers, params=params) as response:
            upl_link = response.json()["href"]
            print("upload link recieved")
    
