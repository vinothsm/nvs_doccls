from .models import OnlyFile
from .models import OnlyRequest, FilesUploadedPerReq
from rest_framework import serializers

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlyFile
        fields = "__all__"

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlyRequest
        fields = "__all__"

class FilesUploadedPerReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilesUploadedPerReq
        fields = "__all__"
