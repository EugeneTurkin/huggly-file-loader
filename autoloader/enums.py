from enum import Enum


class YandexDiskAPI(Enum):
    RESOURCE_META = "https://cloud-api.yandex.net/v1/disk/resources"
    PUBLISH = "https://cloud-api.yandex.net/v1/disk/resources/publish"
    UPLOAD = "https://cloud-api.yandex.net/v1/disk/resources/upload"


class YandexDiskFolder(Enum):
    JOB_KOMIGOR = "disk:/JOB KOMIGOR/"
