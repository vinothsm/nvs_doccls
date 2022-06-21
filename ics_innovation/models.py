from django.db import models

class OnlyRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return '{} by {}'.format(self.request_id, self.created)

class OnlyFile(models.Model):
    file_id = models.AutoField(primary_key=True)
    file_path = models.CharField(max_length=500)

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
