# core/device_loader.py
import json
import os
from pathlib import Path
from core.manager_log import logger
from jsonschema import validate
import jsonschema


schema_oid = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "ip": {"type": "string"},
        
    },
    "additionalProperties": False,  # es para no aceptar mas propiedades, por default al equivocarte de key se agrega como una propiedad nueva, esto se quiere evitar.
}



class DeviceLoader:
    def __init__(self, name_file):


        dir=Path(__file__).resolve().parent
        self.file_path = os.path.join(dir,name_file)

    def load_file_devices(self):
        try:

            with open(self.file_path, "r") as file:
                data = json.load(file)
                for item in data:
                    if(not self.validateJsoDevice(item)):
                        return None
                    
                return data  

        except FileNotFoundError as e: 
            logger.error("FileNotFoundError [{}]".format(self.file_path))
            return None
        


    def validateJsoDevice(self, jsonData):
        try:
            validate(instance=jsonData, schema=schema_oid)
            return True
        
        except jsonschema.exceptions.ValidationError as e:
            logger.error("[{}] Json con formato incorrecto".format(self.file_path))
            return False
