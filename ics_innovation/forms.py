from django import forms
from .models import EntityExtractorV1
from .extractor import get_fulltext_from_pdf
import os
from pathlib import Path

class UploadEntityExtractor(forms.ModelForm):
    class Meta:
        model = EntityExtractorV1
        fields = ["media", "entities"]

    def save(self, commit=True):
        instance = super(UploadEntityExtractor, self).save(commit=False)
        # instance.name = instance.media.file._get_name()
        instance.filepath = os.path.join(Path(__file__).parent, "static/files/"+instance.media.file._get_name())
        instance.staticpath = "files/"+instance.media.file._get_name()
        if commit:
            instance.save()
            instance.extracted_text = get_fulltext_from_pdf(instance.filepath)
        return instance
