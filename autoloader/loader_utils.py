import os
import requests
import zipfile


class FileLoader:
    def __init__(self, file_repo, yandex_resource_meta_endp, yandex_resource_download_endp):
        self.file_repo = file_repo
        self.yandex_resource_meta_endp = yandex_resource_meta_endp
        self.yandex_resource_download_endp = yandex_resource_download_endp

    def download_from_yandex(self, link: str):
        if not (link.startswith("https://disk.yandex.ru") or link.startswith("disk.yandex.ru")):
            raise Exception("неверная ссылка. (должна быть в виде 'disk.yandex.ru...')")

        params = {"public_key": link}

        with requests.get(self.yandex_resource_meta_endp, params=params) as response:
            response.raise_for_status()
            resource_metadata = response.json()

        if resource_metadata["type"] == "file" and resource_metadata["mime_type"].split("/")[0] == "video":
            file_metadata = {
                "name": resource_metadata["name"],
                "format": resource_metadata["mime_type"].split("/")[1],
                "file": resource_metadata["file"],
            }

            dl_file_path = self.file_repo / f'{file_metadata["name"]}.{file_metadata["format"]}'
            
            with requests.get(file_metadata["file"], stream=True) as response:
                response.raise_for_status()
                with open(self.file_repo / f'{file_metadata["name"]}.{file_metadata["format"]}', 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            if not dl_file_path.exists():
                raise Exception("path to downloaded file does not exist")

        elif  resource_metadata["type"] == "dir":
            with requests.get(self.yandex_resource_download_endp, params=params) as response:
                response.raise_for_status()
                dl_link = response.json()["href"]
            with requests.get(dl_link, stream=True) as resp:
                resp.raise_for_status()
                with open(self.file_repo / f"ARCHIVED {resource_metadata["name"]}.zip", 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
            dl_file_path = self.file_repo / f"ARCHIVED {resource_metadata["name"]}.zip"
            if not dl_file_path.exists():
                raise Exception("path to downloaded file does not exist")

            with zipfile.ZipFile(dl_file_path) as zip_file:
                zip_file.extractall(path=self.file_repo / f"{resource_metadata["name"]}")
            os.remove(dl_file_path)
            dl_file_path = self.file_repo / f"{resource_metadata["name"]}"

        else:
            with requests.get(self.yandex_resource_download_endp, params=params) as response:
                response.raise_for_status()
                dl_link = response.json()["href"]
            with requests.get(dl_link, stream=True) as resp:
                resp.raise_for_status()
                with open(self.file_repo / f"{resource_metadata["name"]}.{resource_metadata["mime_type"].split("/")[1]}", 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
            dl_file_path = self.file_repo / f"{resource_metadata["name"]}.{resource_metadata["mime_type"].split("/")[1]}"
            if not dl_file_path.exists():
                raise Exception("path to downloaded file does not exist")

        return dl_file_path
