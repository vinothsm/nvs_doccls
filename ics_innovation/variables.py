from dotenv import load_dotenv
import os

load_dotenv()

env = os.getenv("env")
server_host = os.getenv("server_host")
server_port = os.getenv("server_port")

doc_list = []
selected_document_details = {}
url = server_host + ":" + server_port
urls_obj = {
    "classification": url + "/classification",
    "model_prediction": url + '/model_prediction',
    "status_check": url + '/status_check',
    "training": url + "/training"
}
modal_classifications = {
    'General Classification': [
        'Clinical Reports',
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
    'Clinical Document Classification': [
        'Additional Monitoring Activity [Site Handover Form]',
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
        'Trial Initiation Monitoring Report']}

print(urls_obj)
