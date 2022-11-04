from django import forms
from .models import FilesForTrainingModel
# from .extractor import get_fulltext_from_pdf
import os
from pathlib import Path
import re


class Uploadfiles(forms.ModelForm):
    class Meta:
        model = FilesForTrainingModel
        fields = ["media", "folder_name", "model_name", 'model_id']

    def save(self, commit=True):
        instance = super(Uploadfiles, self).save(commit=False)
        instance.file_name = os.path.splitext(
            instance.media.file._get_name())[0]
        f_name = re.sub('[\\[\\]\\(\\))&]', '',
                        instance.media.file._get_name())
        # f_name= re.sub('[&]',' ',instance.media.file._get_name())
        instance.file_path = os.path.join(
            Path(__file__).parent,
            "static/files/" +
            f_name.replace(
                " ",
                "_"))
        print(instance.file_path)
        instance.is_extracted = 'False'
        instance.is_trained = 'False'
        instance.staticpath = "files/" + f_name.replace(" ", "_")
        if commit:
            instance.save()
            # instance.extracted_text = get_fulltext_from_pdf(instance.file_path)
        return instance
