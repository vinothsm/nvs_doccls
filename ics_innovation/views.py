from sklearn.metrics import classification_report
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
            modal_name=obj["model"]
            op.append(obj)
        url = "http://10.185.56.168:8053/classification"
        resp = req.post(url, json=op)
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
        modal_name = param['modal_name']
        context['details_list']=modal_classifications[modal_name]
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
        context={'model_data':list(modal_classifications.keys())}
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