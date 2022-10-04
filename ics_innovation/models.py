from django.db import models

class OnlyRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    entities=models.TextField(null=True)

    def __str__(self) -> str:
        return '{} by {}'.format(self.request_id, self.created)

class OnlyFile(models.Model):
    file_id = models.AutoField(primary_key=True)
    file_path = models.CharField(max_length=500)
    file_name=models.CharField(max_length=500,null=True)

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
    model_id = models.AutoField(primary_key=True)
    model_name=models.CharField(max_length=500,null=True)
    def __str__(self) -> str:
        return '{} by {}'.format(self.model_id, self.model_name)

class DocClassForTrainingModel(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name=models.CharField(max_length=500,null=True)  
    def __str__(self) -> str:
        return '{} by {}'.format(self.class_id, self.class_name) 

class FilesUploadedForTrainingModel(models.Model):
    file_id = models.AutoField(primary_key=True)
    file_name=models.CharField(max_length=500,null=True)
    def __str__(self) -> str:
        return '{} by {}'.format(self.file_id, self.file_name)  

class ModelsFoldersFiles(models.Model):
    file_id = models.ForeignKey(FilesUploadedForTrainingModel, on_delete=models.CASCADE)
    class_id = models.ForeignKey(DocClassForTrainingModel, on_delete=models.CASCADE)
    model_id = models.ForeignKey(TrainedModel, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return '{} {} by {}'.format(self.file_id, self.class_id,self.model_id)
    
class ModelsStatus(models.Model):
    model_id = models.ForeignKey(TrainedModel, on_delete=models.CASCADE)
    status = models.IntegerField()
    def __str__(self) -> str:
        return '{} {} by {}'.format(self.model_id,self.status)