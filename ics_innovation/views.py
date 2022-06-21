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
from .serializers import FileSerializer, RequestSerializer, FilesUploadedPerReqSerializer
from .models import OnlyFile, FilesUploadedPerReq, OnlyRequest
from rest_framework.response import Response
import json


env = "dev"
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
        'SCAI Classification':['Additional Monitoring Activity [Site Handover Form]',
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
    json = []
    if env == "dev":
        json = [
        ]
    if env == "prod":
        # latest_doc = EntityExtractorV1.objects.order_by("-pk")[0]
        # url = "http://localhost:8053/entities"
        # resp = req.post(url, json={
        #     "input_text": latest_doc.extracted_text,
        #     "entities": latest_doc.entities
        # })
        # json = resp.json()
        json = []

    return Response({"data": json})

@api_view(['GET'])
def get_latest_req(request):
    if request.method == "GET":
        req_id = OnlyRequest.objects.latest("created").request_id
        req_objs = FilesUploadedPerReq.objects.filter(req_id=req_id)
        serializer = FilesUploadedPerReqSerializer(req_objs, many=True)
        all_entries = json.loads(json.dumps(serializer.data))
        op = []
        for entry in all_entries:
            item = FileSerializer(OnlyFile.objects.filter(file_id=entry['file_id']), many=True)
            op.append(json.loads(json.dumps(item.data))[0])
        return Response(data=serializer.data)



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
        delete_all_files()
        # context = {}
        context={'model_data':list(modal_classifications.keys())}
        return render(request, 'ui_document_upload.html', context=context)
    if request.method == "POST":
        print('request.method',request.method)
        request.POST._mutable = True
        request.POST.update(
            {"document": ",".join(request.POST.getlist("entities"))})
        selected_modal=request.POST.getlist("entities")[0]
        context={}
        file_objs = request.data.getlist('media')
        doc_list=[]
        selected_document_details.clear()
        for files in file_objs:
            default_storage.save('files/'+files.name, ContentFile(files.read()))
            doc_dict= {'document' :files.name, 'classification' :selected_modal}
            doc_list.append(doc_dict)
            selected_document_details[files.name]='/files/'+files.name
        context={
            "page": "preview",
            "link": list(selected_document_details.values())[0],
            "response": doc_list
        }
        return render(request, 'ui_preview_page.html', context=context)
    return Response(status=status.HTTP_400_BAD_REQUEST)

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

