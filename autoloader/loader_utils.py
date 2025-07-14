import autoloader.tasks as tasks


class FileLoader:
    def __init__(self, file_repo, yandex_resource_meta_endp, yandex_resource_download_endp):
        self.file_repo = file_repo
        self.yandex_resource_meta_endp = yandex_resource_meta_endp
        self.yandex_resource_download_endp = yandex_resource_download_endp

    def download(self, link: str, dir: str):
        if link.startswith(("https://disk.yandex.ru", "disk.yandex.ru")):
            tasks.dl_yandex_dir(link, self.yandex_resource_meta_endp, self.yandex_resource_download_endp, dir, self.file_repo)
        elif link.startswith(("https://vk.com", "https://vkvideo.ru")):
            tasks.dl_vk_video(link, dir, self.file_repo)
