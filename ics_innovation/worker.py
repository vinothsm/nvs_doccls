from .database import engine
from .extractor import get_fulltext_from_pdf
import requests as req
import dramatiq
from dramatiq.brokers.redis import RedisBroker
from .variables import urls_obj

redis_broker = RedisBroker(host="localhost", port=6379)
dramatiq.set_broker(redis_broker)


@dramatiq.actor
def text_extraction_process(model_id):
    with engine.connect() as con:
        page_load_json = {
            'model_id': model_id,
            'Folders': [],
            'name_of_the_model': ''}
        model_name = ''
        folder_names = {}
        objs = con.execute(
            "select * from ics_innovation_filesfortrainingmodel where is_extracted='{0}' and model_id ='{1}'".format(
                'False', model_id))
        for obj in objs:
            print("@" * 10)
            print(obj.file_id)
            print("#" * 10)
            model_name = obj.model_name
            extracted_text = get_fulltext_from_pdf(obj.file_path)
            con.execute(
                'update  ics_innovation_filesfortrainingmodel set extracted_text = "{0}" , is_extracted = "True" where file_id = "{1}"'.format(
                    extracted_text.replace(
                        '\"',
                        '\''),
                    obj.file_id))
            if obj.folder_name in list(folder_names.keys()):
                folder_names[obj.folder_name].append(
                    {'filename': obj.file_name, 'extracted_text': extracted_text})
            else:
                folder_names[obj.folder_name] = [
                    {'filename': obj.file_name, 'extracted_text': extracted_text}]
        for k, v in folder_names.items():
            page_load_json['Folders'].append({'foldername': k, 'files': v})
        page_load_json['name_of_the_model'] = model_name
        training_url=urls_obj["training"]
        resp = req.post(training_url, json=page_load_json)
        con.execute('update  ics_innovation_filesfortrainingmodel set is_trained = "True"  where model_id = "{0}"'.format(model_id))
        print(resp)

def start_extraction(model_id):
    text_extraction_process.send(model_id)
    # text_extraction_process(model_id)

    return {"message": "successfully submited the request", "code": 200}
