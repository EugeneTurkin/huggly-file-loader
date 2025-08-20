from abc import ABC


class YandexAPIClient(ABC):
    def __init__(self, oauth_token):
        self.oauth_token = oauth_token

    def upload(self):
        ...

    def download(self):
        ...


class YandexAPIClientV1(YandexAPIClient):
    resource_meta: str
    
