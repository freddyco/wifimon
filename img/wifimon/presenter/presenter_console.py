## my_presenter/presenter_console.py
## version original, que imprime por consola en formato legible

# from core.snmp_data_model import SNMPDataModel
# from presenter.presenter_base import PresenterBase



# class PresenterConsole(PresenterBase):
#     def export(self, model: SNMPDataModel):
#         for key, values in model.get_all().items():
#             print(f"[{key}]")
#             for k, v in values.items():
#                 print(f"  {k}: {v}")
#             print()






from core.snmp_data_model import SNMPDataModel
from presenter.presenter_base import PresenterBase
from core.manager_log import get_syslogger
from utils.helpers import get_rounded_timestamp_to_syslog
import json
from core.manager_log import logger

class PresenterConsole(PresenterBase):


    
    def export(self, model: SNMPDataModel):
        # Obtener la fecha y hora redondeada
        currentDateToRow = get_rounded_timestamp_to_syslog()
        

        logger.info(f"Desplegando: {len(model.get_all())} registros. [currentDate: {currentDateToRow}]") 
        
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
            #print(syslogMsg)  # Mostrar el mensaje en consola (para propósitos de depuración)




        