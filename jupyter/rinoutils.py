import functools

from IPython.display import display, Markdown, Latex
import json
import os.path as path


def markdown_description_formatter(info_dict):
    return Markdown("""Il seguente esperimento si basa sul dataset acquisito il **{}** presso **{}**.
ogni vetrino, elaborato con tecnica *{}*, contiene {} con colorazione **{}**.
Le immagini sono state acquisite a **{}**""".format(info_dict['data_acquisizione'],
                                                    info_dict['luogo_acquisizione'],
                                                    info_dict['tecnica'],
                                                    info_dict['contenuto_vetrini'],
                                                    info_dict['colorazione'],
                                                    info_dict['magnification_factor']))


def markdown_table_formatter(info_dict):
    table_head = r = "|  ... |  ... |\n| ------------- | ------------- |\n"
    table_body = '\n'.join([f'| {key} | {value} |' for key, value in info_dict.items()])

    return Markdown(table_head+table_body)


def display_dataset_metadata(dataset_path, formatter, info_file="metainfo.json"):
    """
    Utility function to display dynamic message in jupyter notebook cell.

    """
    file_path = path.join(dataset_path, info_file)

    if path.exists(file_path):
        with open(file_path) as jsonFile:
            display(formatter(json.load(jsonFile)))
    else:
        display((Markdown("**N report is available!** (" + info_file + " file doesn't exist)")))



