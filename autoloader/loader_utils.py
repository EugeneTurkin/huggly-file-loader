import requests


class FileLoader:
    def __init__(self, file_repo, yandex_resource_meta_endp):
        self.file_repo = file_repo
        self.yandex_resource_meta_endp = yandex_resource_meta_endp

    def download_from_yandex(self, link: str):
        if link.startswith("https://disk.yandex.ru"):
            params = {"public_key": link}
            with requests.get(self.yandex_resource_meta_endp, params=params, stream=True) as response:
                response.raise_for_status()
                parsed_response = response.json()
        else:
            raise Exception("link isn't yandex or formatted worng")
        
        if parsed_response["type"] == "file":
            if parsed_response["mime_type"] == "video/mp4":
                resource_metadata = {
                    "name": parsed_response["name"],
                    "format": "mp4",
                    "file": parsed_response["file"],
                }

        dl_file_path = self.file_repo / f'{resource_metadata["name"]}.{resource_metadata["format"]}'
        with requests.get(resource_metadata["file"], stream=True) as response:
            response.raise_for_status()
            with open(self.file_repo / f'{resource_metadata["name"]}.{resource_metadata["format"]}', 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        if dl_file_path.exists():
            return dl_file_path
        else:
            raise Exception("path to downloaded file does not exist")
