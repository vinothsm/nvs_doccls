from django.http import FileResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .forms import UploadEntityExtractor
from .models import EntityExtractorV1
import requests as req
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import shutil
import os
from pathlib import Path


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
            {
                'entity': 'BRAND',
                'expected_values': [
                    {'end_pos': 513, 'start_pos': 503, 'type': 'BRAND', 'value': 'Ioana Nita'}, {'end_pos': 594, 'start_pos': 574, 'type': 'BRAND', 'value': 'Grigore Alexandrescu'}]}, {'entity': 'FORM', 'expected_values': [{'end_pos': 68, 'start_pos': 62, 'type': 'FORM', 'value': 'Tablet'}, {'end_pos': 106, 'start_pos': 90, 'type': 'FORM', 'value': 'Powder for fever'}, {'end_pos': 187, 'start_pos': 186, 'type': 'FORM', 'value': '.'}, {'end_pos': 243, 'start_pos': 242, 'type': 'FORM', 'value': '.'}, {'end_pos': 367, 'start_pos': 366, 'type': 'FORM', 'value': '.'}, {'end_pos': 397, 'start_pos': 396, 'type': 'FORM', 'value': '.'}, {'end_pos': 539, 'start_pos': 514, 'type': 'FORM', 'value': 'Senior Regulatory Affairs'}]}, {'entity': 'STRENGTH', 'expected_values': [{'end_pos': 48, 'start_pos': 40, 'type': 'STRENGTH', 'value': '500mg/mL'}, {'end_pos': 61, 'start_pos': 53, 'type': 'STRENGTH', 'value': '100mg/mL'}, {'end_pos': 122, 'start_pos': 121, 'type': 'STRENGTH', 'value': '-'}, {'end_pos': 126, 'start_pos': 122, 'type': 'STRENGTH', 'value': '1000'}, {'end_pos': 127, 'start_pos': 126, 'type': 'STRENGTH', 'value': '-'}, {'end_pos': 131, 'start_pos': 127, 'type': 'STRENGTH', 'value': '1000'}]}, {'entity': 'NAME', 'expected_values': [{'end_pos': 122, 'start_pos': 117, 'type': 'NAME', 'value': 'A200-'}, {'end_pos': 501, 'start_pos': 492, 'type': 'NAME', 'value': 'John Cena'}, {'end_pos': 513, 'start_pos': 503, 'type': 'NAME', 'value': 'Ioana Nita'}]}, {'entity': 'ADDRESS', 'expected_values': [{'end_pos': 573, 'start_pos': 522, 'type': 'ADDRESS', 'value': 'Regulatory Affairs Associate Metropolis Center, Str'}]}, {'entity': 'SUBJID', 'expected_values': [{'end_pos': 131, 'start_pos': 117, 'type': 'SUBJID', 'value': 'A200-1000-1000'}]}, {'entity': 'AGE', 'expected_values': [{'end_pos': 390, 'start_pos': 388, 'type': 'AGE', 'value': '25'}]}, {'entity': 'DATE', 'expected_values': [{'end_pos': 366, 'start_pos': 353, 'type': 'DATE', 'value': '2nd June 2022'}]}, {'entity': 'COUNTRY', 'expected_values': [{'end_pos': 632, 'start_pos': 625, 'type': 'COUNTRY', 'value': 'Romania'}]}, {'entity': 'EMAIL', 'expected_values': [{'end_pos': 286, 'start_pos': 266, 'type': 'EMAIL', 'value': 'patient123@email.com'}]}, {'entity': 'HEIGHT', 'expected_values': [{'end_pos': 242, 'start_pos': 236, 'type': 'HEIGHT', 'value': '182 cm'}]}, {'entity': 'MEDICAL HISTORY', 'expected_values': [{'end_pos': 446, 'start_pos': 441, 'type': 'MEDICAL HISTORY', 'value': 'fever'}, {'end_pos': 463, 'start_pos': 451, 'type': 'MEDICAL HISTORY', 'value': 'hypertension'}, {'end_pos': 439, 'start_pos': 435, 'type': 'MEDICAL HISTORY', 'value': 'cold'}, {'end_pos': 508, 'start_pos': 503, 'type': 'MEDICAL HISTORY', 'value': 'Ioana'}, {'end_pos': 531, 'start_pos': 514, 'type': 'MEDICAL HISTORY', 'value': 'Senior Regulatory'}, {'end_pos': 463, 'start_pos': 451, 'type': 'MEDICAL HISTORY', 'value': 'hypertension'}, {'end_pos': 446, 'start_pos': 441, 'type': 'MEDICAL HISTORY', 'value': 'fever'}]}, {'entity': 'PHONE', 'expected_values': [{'end_pos': 325, 'start_pos': 310, 'type': 'PHONE', 'value': ' +91-8876291892'}, {'end_pos': 677, 'start_pos': 660, 'type': 'PHONE', 'value': ' +40 37 26 22 399'}, {'end_pos': 655, 'start_pos': 638, 'type': 'PHONE', 'value': ' +40 31 22 53 000'}, {'end_pos': 325, 'start_pos': 311, 'type': 'PHONE', 'value': '+91-8876291892'}]},
            {'entity': 'SITEID', 'expected_values': [{'end_pos': 126, 'start_pos': 122, 'type': 'SITEID', 'value': '1000'}, {
                'end_pos': 131, 'start_pos': 127, 'type': 'SITEID', 'value': '1000'}]},
            {
                'entity': 'WEIGHT', 'expected_values': [
                    {'end_pos': 221, 'start_pos': 216,
                    'type': 'WEIGHT', 'value': '23 kg'}
                ]
            }
        ]
    if env == "prod":
        latest_doc = EntityExtractorV1.objects.order_by("-pk")[0]
        url = "http://localhost:8051/entities"
        resp = req.post(url, json={
            "input_text": latest_doc.extracted_text,
            "entities": latest_doc.entities
        })
        json = resp.json()

    return Response({"data": json})

@api_view(["GET"])
def get_extracted_text(request):
    latest_doc = EntityExtractorV1.objects.order_by("-pk")[0]
    return Response(latest_doc.extracted_text)


# @api_view(["GET", "POST"])
# def upload_page(request):

#     if request.method == "GET":
#         # context = {}
#         context={'model_data':['Document Sensitivity Classification','BERT Classification','SCAI Classification'
#     ]}
#         return render(request, 'ui_document_upload.html', context=context)
#     if request.method == "POST":
#         print('request.method',request.method)
#         request.POST._mutable = True
#         request.POST.update(
#             {"document": ",".join(request.POST.getlist("entities"))})
#         form = UploadEntityExtractor(request.POST, request.FILES)
#         if form.is_valid():
#             form = form.save()
#             form.save()
#             json = [
#                 {
#                     'entity': 'BRAND',
#                     'expected_values': [
#                         {'end_pos': 513, 'start_pos': 503, 'type': 'BRAND', 'value': 'Ioana Nita'}, {'end_pos': 594, 'start_pos': 574, 'type': 'BRAND', 'value': 'Grigore Alexandrescu'}]}, {'entity': 'FORM', 'expected_values': [{'end_pos': 68, 'start_pos': 62, 'type': 'FORM', 'value': 'Tablet'}, {'end_pos': 106, 'start_pos': 90, 'type': 'FORM', 'value': 'Powder for fever'}, {'end_pos': 187, 'start_pos': 186, 'type': 'FORM', 'value': '.'}, {'end_pos': 243, 'start_pos': 242, 'type': 'FORM', 'value': '.'}, {'end_pos': 367, 'start_pos': 366, 'type': 'FORM', 'value': '.'}, {'end_pos': 397, 'start_pos': 396, 'type': 'FORM', 'value': '.'}, {'end_pos': 539, 'start_pos': 514, 'type': 'FORM', 'value': 'Senior Regulatory Affairs'}]}, {'entity': 'STRENGTH', 'expected_values': [{'end_pos': 48, 'start_pos': 40, 'type': 'STRENGTH', 'value': '500mg/mL'}, {'end_pos': 61, 'start_pos': 53, 'type': 'STRENGTH', 'value': '100mg/mL'}, {'end_pos': 122, 'start_pos': 121, 'type': 'STRENGTH', 'value': '-'}, {'end_pos': 126, 'start_pos': 122, 'type': 'STRENGTH', 'value': '1000'}, {'end_pos': 127, 'start_pos': 126, 'type': 'STRENGTH', 'value': '-'}, {'end_pos': 131, 'start_pos': 127, 'type': 'STRENGTH', 'value': '1000'}]}, {'entity': 'NAME', 'expected_values': [{'end_pos': 122, 'start_pos': 117, 'type': 'NAME', 'value': 'A200-'}, {'end_pos': 501, 'start_pos': 492, 'type': 'NAME', 'value': 'John Cena'}, {'end_pos': 513, 'start_pos': 503, 'type': 'NAME', 'value': 'Ioana Nita'}]}, {'entity': 'ADDRESS', 'expected_values': [{'end_pos': 573, 'start_pos': 522, 'type': 'ADDRESS', 'value': 'Regulatory Affairs Associate Metropolis Center, Str'}]}, {'entity': 'SUBJID', 'expected_values': [{'end_pos': 131, 'start_pos': 117, 'type': 'SUBJID', 'value': 'A200-1000-1000'}]}, {'entity': 'AGE', 'expected_values': [{'end_pos': 390, 'start_pos': 388, 'type': 'AGE', 'value': '25'}]}, {'entity': 'DATE', 'expected_values': [{'end_pos': 366, 'start_pos': 353, 'type': 'DATE', 'value': '2nd June 2022'}]}, {'entity': 'COUNTRY', 'expected_values': [{'end_pos': 632, 'start_pos': 625, 'type': 'COUNTRY', 'value': 'Romania'}]}, {'entity': 'EMAIL', 'expected_values': [{'end_pos': 286, 'start_pos': 266, 'type': 'EMAIL', 'value': 'patient123@email.com'}]}, {'entity': 'HEIGHT', 'expected_values': [{'end_pos': 242, 'start_pos': 236, 'type': 'HEIGHT', 'value': '182 cm'}]}, {'entity': 'MEDICAL HISTORY', 'expected_values': [{'end_pos': 446, 'start_pos': 441, 'type': 'MEDICAL HISTORY', 'value': 'fever'}, {'end_pos': 463, 'start_pos': 451, 'type': 'MEDICAL HISTORY', 'value': 'hypertension'}, {'end_pos': 439, 'start_pos': 435, 'type': 'MEDICAL HISTORY', 'value': 'cold'}, {'end_pos': 508, 'start_pos': 503, 'type': 'MEDICAL HISTORY', 'value': 'Ioana'}, {'end_pos': 531, 'start_pos': 514, 'type': 'MEDICAL HISTORY', 'value': 'Senior Regulatory'}, {'end_pos': 463, 'start_pos': 451, 'type': 'MEDICAL HISTORY', 'value': 'hypertension'}, {'end_pos': 446, 'start_pos': 441, 'type': 'MEDICAL HISTORY', 'value': 'fever'}]}, {'entity': 'PHONE', 'expected_values': [{'end_pos': 325, 'start_pos': 310, 'type': 'PHONE', 'value': ' +91-8876291892'}, {'end_pos': 677, 'start_pos': 660, 'type': 'PHONE', 'value': ' +40 37 26 22 399'}, {'end_pos': 655, 'start_pos': 638, 'type': 'PHONE', 'value': ' +40 31 22 53 000'}, {'end_pos': 325, 'start_pos': 311, 'type': 'PHONE', 'value': '+91-8876291892'}]},
#                 {'entity': 'SITEID', 'expected_values': [{'end_pos': 126, 'start_pos': 122, 'type': 'SITEID', 'value': '1000'}, {
#                     'end_pos': 131, 'start_pos': 127, 'type': 'SITEID', 'value': '1000'}]},
#                 {
#                     'entity': 'WEIGHT', 'expected_values': [
#                         {'end_pos': 221, 'start_pos': 216,
#                          'type': 'WEIGHT', 'value': '23 kg'}
#                     ]
#                 }
#             ]
#             context = {
#                 "page": "preview",
#                 "response": json,
#                 "staticpath": form.staticpath,
#                 "extracted_text": form.extracted_text

#             }
#             return render(request, 'ui_preview_page.html', context=context)
#     return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def review_page(request):
    latest_doc = EntityExtractorV1.objects.order_by("-pk")[0]
    context = {
        "staticpath": latest_doc.staticpath
    }
    return render(request, 'ui_review.html', context=context)



@api_view(["GET", "POST"])
def doc_upload_page(request):
    context={'model_data':list(modal_classifications.keys())}
    if request.method == "GET":
        return render(request, 'ui_document_upload.html', context=context)
    if request.method == "POST":
        return render(request, 'ui_document_upload.html', context=context)


def doc_preview_page(request):
    context={
        "page": "preview",
        "link": list(selected_document_details.values())[0],
        "response": [
            {"document": "document1", "classification": "extracted value"},
            {"document": "document2", "classification": "extracted value"},
            {"document": "document3", "classification": "extracted value"},
        ]
    }
    return render(request, 'ui_preview_page.html', context=context)


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
