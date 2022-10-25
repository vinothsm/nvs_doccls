from flask import Flask, jsonify, make_response
import database as sql
from extractor import get_fulltext_from_pdf


app = Flask(__name__)


def text_extraction_process():
    # db = sql.get_db()
    with sql.engine.connect() as con:
        objs = con.execute("select * from ics_innovation_filefortrainingmodel where is_extracted='False'")
        for obj in objs:
            print(obj)
            extracted_text = get_fulltext_from_pdf(obj.file_path)




@app.route("/extract-data")
def extract_data():
    return make_response(jsonify({"message": "Hello"}), 200)
