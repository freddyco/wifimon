from core.snmp_data_model import SNMPDataModel
from presenter.presenter_base import PresenterBase
from core.manager_log import get_syslogger
from utils.helpers import get_rounded_timestamp_to_syslog
import json
from core.manager_log import logger

class PresenterSyslog(PresenterBase):

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.syslogger = get_syslogger("metrics_ap", self.host, self.port)
    
    def export(self, model: SNMPDataModel):
        # Obtener la fecha y hora redondeada
        currentDateToRow = get_rounded_timestamp_to_syslog()
        

        logger.info(f"Enviando a syslog: {len(model.get_all())} registros. [currentDate: {currentDateToRow}]") 
        
        for key, values in model.get_all().items():
            # Añadir la fecha de registro
            values['currentDate'] = currentDateToRow
            
            # Crear un nuevo diccionario para almacenar los datos "planos"
            flat_values = {}
            for k, v in values.items():
                if isinstance(v, dict):  # Si el valor es un diccionario, lo separamos
                    for subk, subv in v.items():
                        flat_values[f"{k}.{subk}"] = subv
                else:
                    flat_values[k] = v

            # Convertir el diccionario plano a JSON para enviar como syslog
            syslogMsg = json.dumps(flat_values)
            self.syslogger.info(syslogMsg)  # Descomenta esto para enviar el mensaje al syslog
            #print(syslogMsg)  # Mostrar el mensaje en consola (para propósitos de depuración)




        
