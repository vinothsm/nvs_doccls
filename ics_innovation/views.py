from django.http import FileResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
import requests as req
import os
from pathlib import Path


diseases_list=['Influenza',
                    'Pulmonary',
                    'Asthma',
                    'Fibrosis',
                    'Non-Small-Cell Lung',
                    'Lung Neoplasms',
                    'Carcinoma',
                    'Lung Cancer',
                    'Perennial Allergic Rhinitis',
                    'Cystic Fibrosis',
                    'Common Cold']

countries=[ 'USA',
            'Switzerland',
            'India',
            'Australia',
            'Netherlands',
            'Iceland',
            'Italy',
            'United Kingdom']
env='prod'
url_ = "http://10.185.56.168:8051/attriton_model"

def render_home(request):
    return render(request, 'ui_attrition_prediction.html', {'diseases':diseases_list,'countries':countries})

@api_view(['GET','POST'])
def get_prediction(request): 
    resp_json=[{"aa_attrition": 0.44029015150669476,"assian_attrition": 0,"native_attrition": 0,"overall_attrition": 6.605375048976249,"country":'India'},
    {"aa_attrition": 0.44029015150669476,"assian_attrition": 0,"native_attrition": 0,"overall_attrition": 6.605375048976249,"country":'India'},
    {"aa_attrition": 0.44029015150669476,"assian_attrition": 0,"native_attrition": 0,"overall_attrition": 6.605375048976249,"country":'India'},
    {"aa_attrition": 0.44029015150669476,"assian_attrition": 0,"native_attrition": 0,"overall_attrition": 6.605375048976249,"country":'India'},
    {"aa_attrition": 0.44029015150669476,"assian_attrition": 0,"native_attrition": 0,"overall_attrition": 6.605375048976249,"country":'India'}
]
    inputs_values={
    "number_of_years": 5,
    "age_mean": 12,
    "planned_enrollment":25,
    "gdp_country_names":["USA","India","Switzerland","Australia","Netherlands","Iceland","United Kingdom"],
    "asian_fraction":0,
    "native_fraction":1,
    "aa_fraction":0,
    "intervention_treatment_no_of_drugs":4,
    "ae_chest_pain":0,
    "ae_respiratory_failure":0,
    "number_of_diseases":2
}
    if env=='prod':
        url = url_
        inputs_values=request.POST.dict()
        resp = req.post(url,json={'gdp_country_names':request.POST['gdp_country_names'].split(','),
          "number_of_years": int(inputs_values['number_of_years']),
        "age_mean": float(inputs_values['age_mean']),
        "planned_enrollment":int(inputs_values['planned_enrollment']),
        "asian_fraction":int(inputs_values['asian_fraction']),
        "native_fraction":int(inputs_values['native_fraction']),
        "aa_fraction":int(inputs_values['aa_fraction']),
        "intervention_treatment_no_of_drugs":int(inputs_values['intervention_treatment_no_of_drugs']),
        "ae_chest_pain":int(inputs_values['ae_chest_pain']),
        "ae_respiratory_failure":int(inputs_values['ae_respiratory_failure']),
        "number_of_diseases":int(inputs_values['number_of_diseases'])})
        resp_json = resp.json()
    return JsonResponse( {'data':resp_json})
    
    
