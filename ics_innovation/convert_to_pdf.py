from lib2to3.pytree import convert
from docx2pdf import convert


def get_converted_file(filepath):
    new_filepath = filepath.replace(".docx", ".pdf")
    convert(filepath, new_filepath)
    return new_filepath
