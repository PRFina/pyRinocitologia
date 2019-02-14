from IPython.display import display, Markdown, Latex
import json
import os.path as path

def buildMessage(jObject):
    return  """Il seguente esperimento si basa sul dataset acquisito il **{}** presso **{}**.
ogni vetrino, elaborato con tecnica *{}*, contiene {} con colorazione **{}**.
Le immagini sono state acquisite a **{}**""".format(jObject['data_acquisizione'],
                                                            jObject['luogo_acquisizione'],
                                                            jObject['tecnica'],
                                                            jObject['contenuto_vetrini'],
                                                            jObject['colorazione'],
                                                            jObject['magnification_factor'])
def displayDatasetMetadata(dataset_path):
    filePath = path.join(dataset_path, "metainfo.json")
    if path.exists(filePath):
        with open(filePath) as jsonFile:
            display(Markdown(buildMessage(json.load(jsonFile))))
    else:
        display((Markdown("** NO report (metainfo.json file) is available!**")))
