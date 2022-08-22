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
    inputs={
    "Number_of_Years": 0.3,
    "Age_mean": 59.5,
    "Planned_Enrollment":163,
    "GDP_Country_name":"India",
    "Asian_fraction":0,
    "Native_fraction":0,
    "AA_fraction":1,
    "Intervention_Treatment_no_of_drugs":["Budesonide","Single low dose cyclophosphamide"],
    "AE_chest_pain":0,
    "AE_respiratory_failure":0,
    "Number_of_Diseases":["Influenza","Pulmonary","Asthma"]
    }
    # if env=='prod':
    #     # op_dict={'Number_of_Years':3, 'Age_mean':59.5, 'Planned_Enrollment': 163, 'GDP_Country_name':'India', 'Asian_fraction':8, 'Native_fraction':8, "AA_fraction":1, 'Intervention_Treatment_no_of_drugs': ['Budesonide', 'Single low-dose cyclophosphanide'], 'AE_chest_pain':8, 'AE_respiratory_failure':8, 'Number_of_Diseases': ['Influenza', 'Pulmonary', 'Asthna']}
    #     url = url_
    #     resp = req.post(url,json=inputs)
    #     print(resp.json)
        # resp_json = resp.json()
    return JsonResponse( {'data':resp_json})
    
    
