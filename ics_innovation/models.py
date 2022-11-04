from django.db import models


class OnlyRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    entities = models.TextField(null=True)

    def __str__(self) -> str:
        return '{} by {}'.format(self.request_id, self.created)


class OnlyFile(models.Model):
    file_id = models.AutoField(primary_key=True)
    file_path = models.CharField(max_length=500)
    file_name = models.CharField(max_length=500, null=True)

    def __str__(self) -> str:
        return '{} by {}'.format(self.file_id, self.file_path)


class FilesUploadedPerReq(models.Model):
    req_id = models.ForeignKey(OnlyRequest, on_delete=models.CASCADE)
    file_id = models.ForeignKey(OnlyFile, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return '{} by {}'.format(self.req_id, self.file_id)


class FileText(models.Model):
    file_id = models.ForeignKey(OnlyFile, on_delete=models.CASCADE)
    file_text = models.TextField()

    def __str__(self) -> str:
        return '{} by {}'.format(self.file_id, self.file_text)


class TrainedModel(models.Model):
    model_name = models.CharField(max_length=500, null=True)
    model_id = models.AutoField(primary_key=True)

    def __str__(self) -> str:
        return super().__str__()


class FilesForTrainingModel(models.Model):
    file_id = models.AutoField(primary_key=True)
    file_path = models.CharField(null=False, max_length=100)
    file_name = models.CharField(null=False, max_length=100)
    media = models.FileField(null=False, blank=True, upload_to="files")
    extracted_text = models.TextField(null=True)
    staticpath = models.CharField(null=True, max_length=100)
    folder_name = models.CharField(null=True, max_length=100)
    model_name = models.CharField(null=True, max_length=100)
    model_id = models.IntegerField(default=-1)
    is_trained = models.CharField(max_length=100, default='False')
    is_extracted = models.CharField(max_length=100, default='False')

    def __str__(self) -> str:
        return super().__str__()
