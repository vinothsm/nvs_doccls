import database as sql
from extractor import get_fulltext_from_pdf
import requests as req
import dramatiq

@dramatiq.actor
def text_extraction_process(model_id):
    start_time = time.time()
    with sql.engine.connect() as con:
        page_load_json={'model_id':model_id,'Folders':[],'name_of_the_model':''}
        model_name = ''
        folder_names = {}
        objs = con.execute("select * from ics_innovation_filesfortrainingmodel where is_extracted='{0}' and model_id ='{1}'".format('False',model_id))
        for obj in objs:
            print("%"*10)
            print(obj)
            print("$"*10)
            model_name = obj.model_name
            extracted_text = get_fulltext_from_pdf(obj.file_path)
            con.execute('update  ics_innovation_filesfortrainingmodel set extracted_text = "{0}" , is_extracted = "True" where file_id = "{1}"'.format(extracted_text.replace('\"','\''),obj.file_id))
            if obj.folder_name in list(folder_names.keys()):
                folder_names[obj.folder_name].append({'filename':obj.file_name,'extracted_text':extracted_text})
            else:
                folder_names[obj.folder_name] = [{'filename':obj.file_name,'extracted_text':extracted_text}]
        for k,v in folder_names.items():
            page_load_json['Folders'].append({'foldername':k,'files':v})
        page_load_json['name_of_the_model'] = model_name
        # training_url='http://10.185.56.168:8051/training'
        # resp = req.post(training_url, json=page_load_json)
        # con.execute('update  ics_innovation_filesfortrainingmodel set is_trained = "True"  where model_id = "{0}"'.format(model_id))
        # print(resp)
    end_time = time.time()
    print("Time taken to execute text_extraction_process...", (end_time - start_time))


def start_extraction(model_id):
    text_extraction_process.send(model_id)