from autoloader.tasks import dl_yandex_dir


class FileLoader:
    def __init__(self, file_repo, yandex_resource_meta_endp, yandex_resource_download_endp):
        self.file_repo = file_repo
        self.yandex_resource_meta_endp = yandex_resource_meta_endp
        self.yandex_resource_download_endp = yandex_resource_download_endp

    def download_from_yandex(self, link: str, dir: str):
        if not link.startswith(("https://disk.yandex.ru", "disk.yandex.ru")):
            raise Exception("неверная ссылка. (должна быть в виде 'disk.yandex.ru...')")


        dl_yandex_dir(link, self.yandex_resource_meta_endp, self.yandex_resource_download_endp, dir, self.file_repo)
        
        return None
