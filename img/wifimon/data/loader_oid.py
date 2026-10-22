# core/oid_loader.py
import json
import os
from pathlib import Path
from core.manager_log import logger
from jsonschema import validate
import jsonschema

schema_oid = {
    "type": "object",
    "properties": {
        "oids": {
            "type": "object",
            "patternProperties": {
                "^[a-zA-Z0-9_]+$": {  # Para aceptar cualquier clave de categoría (como "general", "interface", etc.)
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "oid": {"type": "string"}
                        },
                        "required": ["name", "oid"],
                        "additionalProperties": False
                    }
                }
            },
            "additionalProperties": False
        }
    },
    "required": ["oids"],
    "additionalProperties": False
}





class OIDLoader:
    def __init__(self, name_file):
        dir=Path(__file__).resolve().parent
        self.file_path = os.path.join(dir, name_file)


    def load_file_oids(self, category=None):
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                if not self.validateJsonOID(data):
                    return None

                if category:
                    return self.get_oids_by_category(data, category)
                else:
                    return data  # devolvemos el JSON completo para acceder a todas las categorías

        except FileNotFoundError:
            logger.error(f"FileNotFoundError [{self.file_path}]")
            return None





    def validateJsonOID(self, jsonData):
        try:
            validate(instance=jsonData, schema=schema_oid)
            return True
        except jsonschema.exceptions.ValidationError as e:

            logger.error("[{}] Json con formato incorrecto".format(self.file_path))
            return False



    def get_oids_by_category(self, data, category):

        """Devuelve los OIDs según la categoría solicitada"""
        return data["oids"].get(category, [])
    

    def get_all_oids(self, data):
        """Devuelve todos los OIDs de cualquier categoría presente dentro de 'oids'."""
        all_oids = []
        oids_dict = data.get("oids", {})

        for items in oids_dict.values():
            all_oids.extend(items)

        return all_oids


    def get_all_oids_by_category(self, data):
        """Devuelve todos los OIDs organizados por categoría"""
        
        return data.get("oids", {})
    



