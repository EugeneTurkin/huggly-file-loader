import os
from pathlib import Path
import requests
import shutil
import zipfile

from huey.contrib.djhuey import task
from yt_dlp import YoutubeDL


@task()
def dl_vk_video(link, dir, dls):
    ydl_opts = {
        "paths": {
            "home": str(dls),
        }
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        name = Path(info["requested_downloads"][0]["filename"])
        ext = Path(info["requested_downloads"][0]["ext"])
        ptd = name.parent / f"brodude.{ext}"
        # os.rename(name, ptd)
    
    shutil.move(name, dir, copy_function=shutil.copy2)  # TODO: если в конечном пункте уже существует файл или директория с таким именем, таск упадёт с ошибкой!



@task()
def dl_yandex_dir(link, yandex_resource_meta_endp, yandex_resource_download_endp, dir, file_repo):
    params = {"public_key": link}

    with requests.get(yandex_resource_meta_endp, params=params) as response:
        response.raise_for_status()
        resource_metadata = response.json()

    if resource_metadata["type"] == "file" and os.path.split(resource_metadata["mime_type"]) == "video":
        file_metadata = {
            "name": resource_metadata["name"],
            "format": resource_metadata["mime_type"].split("/")[1],
            "file": resource_metadata["file"],
        }

        dl_file_path = file_repo / f'{file_metadata["name"]}.{file_metadata["format"]}'
        
        with requests.get(file_metadata["file"], stream=True) as response:
            response.raise_for_status()
            with open(file_repo / f'{file_metadata["name"]}.{file_metadata["format"]}', 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        if not dl_file_path.exists():
            raise Exception("path to downloaded file does not exist")

    elif  resource_metadata["type"] == "dir":
        resource_metadata["name"] = resource_metadata["name"].strip(" ")  # TODO: если исходное имя файла сожержит трейлинг пробелы, возникают проблемы с извлечением на 69 (nice) строке, подумать о валидации
        with requests.get(yandex_resource_download_endp, params=params) as response:
            response.raise_for_status()
            dl_link = response.json()["href"]
        with requests.get(dl_link, stream=True) as resp:
            resp.raise_for_status()
            with open(file_repo / f"ARCHIVED {resource_metadata["name"]}.zip", 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
        dl_file_path = file_repo / f"ARCHIVED {resource_metadata["name"]}.zip"
        if not dl_file_path.exists():
            raise Exception("path to downloaded file does not exist")

        with zipfile.ZipFile(dl_file_path) as zip_file:
            zip_file.extractall(path=file_repo / f"{resource_metadata["name"]}")
        os.remove(dl_file_path)
        dl_file_path = file_repo / f"{resource_metadata["name"]}"

    else:
        with requests.get(yandex_resource_download_endp, params=params) as response:
            response.raise_for_status()
            dl_link = response.json()["href"]
        with requests.get(dl_link, stream=True) as resp:
            resp.raise_for_status()
            with open(file_repo / f"{resource_metadata["name"]}.{resource_metadata["mime_type"].split("/")[1]}", 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
        dl_file_path = file_repo / f"{resource_metadata["name"]}.{resource_metadata["mime_type"].split("/")[1]}"
        if not dl_file_path.exists():
            raise Exception("path to downloaded file does not exist")

    shutil.move(dl_file_path, dir, copy_function=shutil.copy2)  # TODO: если в конечном пункте уже существует файл или директория с таким именем, таск упадёт с ошибкой!

    return None


@task()
def upload_to_yandex(fpath, destemail, src):
    from django.conf import settings
    from django.core.mail import send_mail

    fpath1 = f"disk:/JOB KOMIGOR/{fpath}"
    headers = {
        "Authorization": f"OAuth {settings.YANDEX_KOMIGOR_OAUTH_KEY}"
    }
    params = {
        "path": fpath1,
    }
    print(headers)
    print(params)
    l1 = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    l2 = "https://cloud-api.yandex.net/v1/disk/resources/publish"
    l3 = "https://cloud-api.yandex.net/v1/disk/resources"

    with requests.get(l1, headers=headers, params=params) as response:
        upl_link = response.json()["href"]
        print("upload link recieved")
    
    with open(src, "rb") as f:
        print("file opened")
        requests.put(upl_link, data=f)
        print("file uploaded")
    
    with requests.put(l2, headers=headers, params=params) as re:
        print("done")
    
    with requests.get(l3, headers=headers, params=params) as res:
        dl_link = res.json()["public_url"]
    
    send_mail(
        f"Ссылка -- {fpath}",
        dl_link,
        "test@komigor.com",
        recipient_list=[destemail],
        fail_silently=True,
    )
