from .convert_to_pdf import get_converted_file
from django.http import FileResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
import requests as req
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import shutil
import os
from pathlib import Path
from .serializers import FileSerializer, RequestSerializer, FilesUploadedPerReqSerializer,FileTextSerializer
from .models import OnlyFile, FilesUploadedPerReq, OnlyRequest,FileText
from rest_framework.response import Response
import json
from django.core.files.storage import FileSystemStorage
from .extractor import get_fulltext_from_pdf
from .forms import Uploadfiles
from .models import FilesForTrainingModel,TrainedModel
import pandas as pd

env = "prod"
doc_list= []
selected_document_details={}
modal_classifications={
       'General Classification':['Clinical Reports',
                                    'Communication',
                                    'Contact Tracing',
                                    'Diagnostics',
                                    'Drug Targets',
                                    'Education',
                                    'Effect on Medical Specialties',
                                    'Forecasting & Modelling',
                                    'Health Policy',
                                    'Healthcare Workers',
                                    'Imaging',
                                    'Immunology',
                                    'Inequality',
                                    'Infection Reports',
                                    'Long Haul',
                                    'Medical Devices',
                                    'Misinformation',
                                    'Model Systems & Tools',
                                    'Molecular Biology',
                                    'Non-human',
                                    'Non-medical',
                                    'Pediatrics',
                                    'Prevalence',
                                    'Prevention',
                                    'Psychology',
                                    'Recommendations',
                                    'Risk Factors',
                                    'Surveillance',
                                    'Therapeutics',
                                    'Transmission',
                                    'Vaccines'],
        'Clinical Document Classification':['Additional Monitoring Activity [Site Handover Form]',
                                    'Checklist [Full Protocol Package (FPP)]',
                                    'DSUR Report Body',
                                    'Informed Consent Form',
                                    'Investigators Brochure',
                                    'Monitoring Visit Report',
                                    'Pre Trial Monitoring Report',
                                    'Protocol',
                                    'Ready-to-Initiate-Sites (RIS) checklist',
                                    'Study Table',
                                    'Summary of Clinical Efficacy',
                                    'Trial Initiation Monitoring Report']
   }
@api_view(["GET"])
def get_extracted_data(request):
    if env == "prod":
        req_object = OnlyRequest.objects.latest("created")
        req_id = req_object.request_id
        req_objs = FilesUploadedPerReq.objects.filter(req_id=req_id)
        serializer = FilesUploadedPerReqSerializer(req_objs, many=True)
        all_entries = json.loads(json.dumps(serializer.data))
        op = []
        modal_name=''
        for entry in all_entries:
            item = FileTextSerializer(FileText.objects.filter(file_id=entry['file_id']), many=True)
            obj = json.loads(json.dumps(item.data))[0]
            obj["model"] = req_object.entities
            obj["model_name"] = req_object.entities
            obj["file_id"] = str(entry['file_id'])
            obj["file_text"] =obj["file_text"][:500]
            modal_name=obj["model"]
            op.append(obj)
        url = "http://10.185.56.168:8053/classification"
        if modal_name not in list(modal_classifications.keys()):
             url = 'http://10.185.56.168:8051/model_prediction'
        # jjj =[{'file_id': '1234', 'file_text': 'A recent cluster of pneumonia cases in Wuhan, China, was caused by a novel betacoronavirus, the 2019 novel coronavirus (2019-nCoV). We report the epidemiological, clinical, laboratory, and radiological characteristics and treatment and clinical outcomes of these patients. All patients with suspected 2019-nCoV were admitted to a designated hospital', 'model_name': 'auto_train_model'}, {'file_id': '5678', 'file_text': 'In children, SARS-CoV-2 infection is usually asymptomatic or causes a mild illness of short duration. ', 'model_name': 'auto_train_model'}]
        resp=req.post(url,json=op)
        resp_json = resp.json()
        for _file in resp_json:
            item = FileSerializer(OnlyFile.objects.filter(file_id=_file["file_id"]), many=True)
            _file["file_name"] = json.loads(json.dumps(item.data))[0]["file_name"]
        
        modal_classifications_list= modal_classifications[modal_name]
        classification_count=dict.fromkeys(modal_classifications_list, 0)
        return Response(data={'data': resp_json,'summary':classification_count})

    if env == "dev":
        modal_name='Clinical Document Classification'
        modal_classifications_list= modal_classifications[modal_name]
        classification_count=dict.fromkeys(modal_classifications_list, 0)
        resp_json= [{'class': 'Additional Monitoring Activity [Site Handover Form]', 'confidence': 0.22228756546974182, 'error': 'Success', 'model': 'Clinical Document Classification', 'file_name': 'Document1.pdf', 'page_text': 'something'}, {'class': 'Summary of Clinical Efficacy', 'confidence': 0.8513577230114553, 'error': 'Success', 'model': 'CORONA', 'file_name': 'Document3.pdf', 'page_text': 'text of the file 2'}]
        return Response(data={'data':resp_json,'summary':classification_count})

    return Response({"data": []})

@api_view(['GET'])
def get_latest_req(request):
    if request.method == "GET":
        req_object=OnlyRequest.objects.latest("created")
        req_id = req_object.request_id
        req_objs = FilesUploadedPerReq.objects.filter(req_id=req_id)
        serializer = FilesUploadedPerReqSerializer(req_objs, many=True)
        all_entries = json.loads(json.dumps(serializer.data))
        op = []
        for entry in all_entries:
            item = FileSerializer(OnlyFile.objects.filter(file_id=entry['file_id']), many=True)
            op.append(json.loads(json.dumps(item.data))[0])
        return Response(data={'files':op,'entities':req_object.entities})



def get_modal_details(request):
   context={}
   if request.method == "GET":
        param = request.GET
        model_name = param['modal_name']
        model_id =int(param['modal_id'])
        if model_id == -1:
            context['details_list']=modal_classifications[model_name]
        else:
            get_details=pd.DataFrame.from_records(FilesForTrainingModel.objects.filter(model_id = model_id).values())
            context['details_list']=list(set(get_details['folder_name'].tolist()))
   return JsonResponse(context)


def get_document_preview_file(request):
    context={}
    if request.method == "GET":
        param = request.GET
        document_name = param['document_name']
        context['document_path']=selected_document_details[document_name]
    return JsonResponse(context)

@api_view(["GET", "POST"])
def upload_page(request):
    if request.method == "GET":
        # delete_all_files()
        # context = {}
        get_details=pd.DataFrame.from_records(TrainedModel.objects.all().values())
        trained_model=''
        model_id=''
        if not get_details.empty:
            trained_model=get_details.iloc[-1]['model_name']
            model_id=get_details.iloc[-1]['model_id']
        context={'model_data':list(modal_classifications.keys()),'trained_model':trained_model,'model_id':model_id}
        return render(request, 'ui_document_upload.html', context=context)
    if request.method == "POST":
        file_objs = []
        modal_names=",".join(request.POST.getlist("entities"))
        for myfile in request.FILES.getlist('media'):
            # myfile = inmemory_obj.file
            fs = FileSystemStorage() #defaults to   MEDIA_ROOT 
            filename = fs.save(myfile.name.replace(" ", "_"), myfile)
            file_url = fs.url(filename)
            file_ = os.path.join(Path(__file__).parent, "static/"+filename)
            # if(".docx" in filename):
            #     file_ = get_converted_file(file_)
            #     filename = filename.replace(".docx", ".pdf")
            #     file_url = file_url.replace(".docx", ".pdf")
            file_serializer = FileSerializer(data={"file_path": file_url,'file_name':filename})
            if(file_serializer.is_valid(raise_exception=True)):
                print("valid one")
                file_obj = file_serializer.save()
                file_objs.append(file_obj)
                file_=os.path.join(Path(__file__).parent, "static/"+filename)
                file_text=get_fulltext_from_pdf(file_)
                ft_serializer=FileTextSerializer(data={'file_id':file_obj.file_id,'file_text':file_text})
                if(ft_serializer.is_valid(raise_exception=True)):
                    ft_serializer.save()
        req_serializer = RequestSerializer(data={'entities':modal_names})
        req_obj = {}
        if(req_serializer.is_valid(raise_exception=True)):
            req_obj = req_serializer.save()
        for file_obj in file_objs:
            fupr_serializer = FilesUploadedPerReqSerializer(data={
                "req_id": req_obj.request_id, "file_id": file_obj.file_id
            })
            if(fupr_serializer.is_valid(raise_exception=True)):
                fupr_serializer.save()
        # print(FilesUploadedPerReq.objects.get({"req_id": req_obj.request_id}))

        return render(request, 'ui_preview_page_d1.html', {
        })
    return Response(status=status.HTTP_400_BAD_REQUEST)

def get_preview(request):
    return render(request, 'ui_preview_page_d1.html', {})

def delete_all_files():
    file_folder_path=os.path.join(Path(__file__).parent, "static/files/")
    folder_exists=os.path.isdir(file_folder_path)
    if folder_exists:
        shutil.rmtree(file_folder_path)

@api_view(['GET', 'POST'])
def get_form(request):
    if request.method == "POST":
        urls_list = []
        file_objs = []
        for myfile in request.FILES.getlist('media'):
            # myfile = inmemory_obj.file
            fs = FileSystemStorage() #defaults to   MEDIA_ROOT  
            filename = fs.save(myfile.name, myfile)
            file_url = fs.url(filename)
            urls_list.append(file_url)
            print(file_url)
            file_serializer = FileSerializer(data={"file_path": file_url})
            if(file_serializer.is_valid(raise_exception=True)):
                print("valid one")
                file_obj = file_serializer.save()
                file_objs.append(file_obj)
                print(file_obj)
        req_serializer = RequestSerializer(data={})
        req_obj = {}
        if(req_serializer.is_valid(raise_exception=True)):
            req_obj = req_serializer.save()
        for file_obj in file_objs:
            fupr_serializer = FilesUploadedPerReqSerializer(data={
                "req_id": req_obj.request_id, "file_id": file_obj.file_id
            })
            if(fupr_serializer.is_valid(raise_exception=True)):
                fupr_serializer.save()
        # print(FilesUploadedPerReq.objects.get({"req_id": req_obj.request_id}))

        return render(request, 'form.html', {
            'urls': urls_list
        })
    return render(request, "form.html", {"urls": []})

# def get_document_preview_file(request):
#     context={}
#     if request.method == "GET":
#         param = request.GET
#         document_name = param['document_name']
#         context['document_path']=selected_document_details[document_name]
#     return JsonResponse(context)

@api_view(['GET', 'POST'])

def train_model(request):
    return render(request, 'ui_upload_document_types.html', {})


@api_view(['GET', 'POST'])

def model_status(request):
    return render(request, 'model_progress.html', {})


@api_view(["GET", "POST"])
def upload_files_for_training_model(request):
    if request.method == "GET":
        context = {}
        return render(request, 'ui_upload_document_types.html', context=context)
    if request.method == "POST":
        # import pdb;pdb.set_trace()
        request.POST._mutable = True
        folder_name=request.POST.getlist('folder_name')
        model_name=request.POST.getlist('model_name')[0]
        tm = TrainedModel(model_name=model_name)
        tm.save()
        counts=request.POST.getlist('count')
        count_file=0
        file_index=0
        training_url='http://10.185.56.168:8051/training'
        files_=request.FILES.getlist('media')
        page_load_json={
                    'name_of_the_model' :model_name,
                    "Folders" :[]
                    }
        for  file in files_:
            request.POST.setlist('folder_name',[folder_name[file_index]])
            request.POST.setlist('model_id',[tm.model_id])
            request.FILES.setlist('media',[file])
            form = Uploadfiles(request.POST, request.FILES)
            if form.is_valid():
                form = form.save()
                form.save()
                count_file=count_file+1
                if count_file == int(counts[file_index]):
                    count_file = 0
                    file_index =file_index+1
        folders=[]
        page_load_json['model_id'] = tm.model_id
        for class_name in folder_name:
            get_details=pd.DataFrame.from_records(FilesForTrainingModel.objects.filter(model_name__exact = model_name).exclude(is_trained = True).filter(folder_name__exact = class_name).values())
            get_details=get_details.rename(columns={"file_name": "filename"})
            files_json=json.loads(get_details[[ 'filename', 'extracted_text']].to_json(orient='records'))
            folders.append({'foldername':class_name,'files':files_json})
        page_load_json['Folders']=folders
        resp = req.post(training_url, json=page_load_json)
        FilesForTrainingModel.objects.filter(model_name__exact = model_name).exclude(is_trained = True).update(is_trained = True)
        return render(request, 'model_progress.html', context={})
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def status_check(request):
    resp = req.get('http://10.185.56.168:8051/status_check')
    print('resp.text',resp.text)
    return JsonResponse({'msg':resp.text})
