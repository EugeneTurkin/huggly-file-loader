from django import forms
from django.conf import settings

from autoloader.models import UploadTask


# class UploadDataForm(forms.Form):
#     choose_file = forms.FilePathField(
#         required=True,
#         path=str(settings.STORAGE_DIR),
#         recursive=True,
#         allow_folders=False,
#         label="Выберите файл",
#     )
#     email = forms.EmailField(required=True, initial="vesti@gmail.com")


class UploadDataForm(forms.ModelForm):
    class Meta:
        model = UploadTask
        fields = ["source", "destination", "notification_recipient"]
