# core/snmp_data_model.py

from collections import defaultdict

class SNMPDataModel:
    def __init__(self):
        # Usar defaultdict(dict) es una excelente elección aquí.
        self.data = defaultdict(dict)

    def add_value(self, device_ip, object_name, index_parts, value, object_group=None):
        # La clave principal siempre se basa en el primer índice y el WLC.
        base_index = "-".join(index_parts[:1]) + f"-{device_ip}"

        # --- OPTIMIZACIÓN: Añadir metadatos solo la primera vez ---
        # Usamos la presencia de 'wlc' como señal de que ya hemos inicializado este registro.
        if "wlc" not in self.data[base_index]:
            self.data[base_index]["wlc"] = device_ip
            self.data[base_index]["id"] = base_index
        
        if object_group:
            self.data[base_index]["category"] = object_group
        # --------------------------------------------------

        nested_keys = index_parts[1:]
        
        if not nested_keys:
            # Si no hay subíndice anidado, el valor es directo.
            self.data[base_index][object_name] = value
            return

        # Navegación para crear/encontrar el diccionario anidado correcto.
        if object_name not in self.data[base_index] or not isinstance(self.data[base_index].get(object_name), dict):
            self.data[base_index][object_name] = {}

        target = self.data[base_index][object_name]
        for key in nested_keys[:-1]:
            if key not in target or not isinstance(target.get(key), dict):
                target[key] = {}
            target = target[key]

        target[nested_keys[-1]] = value

    def get_all(self):
        # Devuelve una copia superficial para evitar modificaciones accidentales fuera de la clase.
        return dict(self.data)

    def merge(self, other_model):
        """
        Combina otro modelo de datos en este.
        Esta implementación es segura, a prueba de errores de iteración y eficiente.
        """
        # Itera sobre los items del modelo de origen.
        for base_index, values in other_model.get_all().items():
            if base_index not in self.data:
                # Si la clave base no existe, copia todos los valores directamente.
                self.data[base_index] = values
            else:
                # Si la clave existe, fusiona cada campo individualmente.
                for key, value in values.items():
                    # Fusiona diccionarios internos o sobrescribe otros valores.
                    if (key in self.data[base_index] and 
                            isinstance(value, dict) and 
                            isinstance(self.data[base_index][key], dict)):
                        self.data[base_index][key].update(value)
                    else:
                        self.data[base_index][key] = value