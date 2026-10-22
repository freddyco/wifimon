# main.py

import time
from typing import List
from services.device_service import DeviceService
from services.oid_service import OIDService
from services.snmp_service import SNMPService
from services.nms_service import NMSService
from services.data_analyzer import DataAnalyzer
from presenter.presenter_csv import PresenterCSV
from presenter.presenter_console import PresenterConsole
from presenter.presenter_syslog import PresenterSyslog
from presenter.presenter_base import PresenterBase
from core.snmp_data_model import SNMPDataModel
from core.manager_log import logger
from core.arg_parser import parser_args  # <<< NUEVO: Importar parser_args

FILE_DEVICES = 'devices.json'
FILE_OIDS = 'oids.json'
#CATEGORY_OIDS = ["bsnAPTable", "bsnAPIfStatsTable"] # for test_1
#CATEGORY_OIDS = ["bsnMobileStationTable"] # for test_2

#CATEGORY_OIDS = ["bsnAPTable", "bsnAPIfTable", "ciscoLwappApTable"] # for csv
CATEGORY_OIDS = ["bsnAPTable", "bsnAPIfTable", "ciscoLwappApTable", "bsnDot11EssTable", "bsnAPIfLoadTable", "bsnAPIfStatsTable"] # for console, syslog





def exportar_datos(model: SNMPDataModel, presentadores: List[PresenterBase]):

    for presenter in presentadores:
        try:
            presenter.export(model)

        except Exception as e:
            logger.error(f"Error exportando con {presenter.__class__.__name__}: {e}")



def main_loop():

    args = parser_args()

    if not args:
        return

    # Cargar Devices (dispositivos/controladores)
    devices = DeviceService(FILE_DEVICES).load_devices()
    if not devices:
        logger.warning("No hay dispositivos a consultar.")
        return

    # Cargar OIDs
    oids_por_categoria = OIDService(FILE_OIDS).load_all_by_category()
    if not oids_por_categoria:
        logger.warning("No hay OIDs a consultar")
        return

    snmp_service = SNMPService(CATEGORY_OIDS, community=args.snmp_c, port=args.snmp_p)
    nms_service  = NMSService(args.nms_token)
    data_analyzer = DataAnalyzer()


    presentadores = []

    # Verifica si 'console' está en los presentadores
    if 'console' in args.presenters:
        presentadores.append(PresenterConsole())

    # Verifica si 'csv' está en los presentadores
    if 'csv' in args.presenters:
        presentadores.append(PresenterCSV())

    # Verifica si 'syslog' está en los presentadores y si syslog_h está definido
    if 'syslog' in args.presenters:
        if args.syslog_h:
            presentadores.append(PresenterSyslog(host=args.syslog_h, port=args.syslog_p))
        else:
            logger.warning("Syslog seleccionado pero no hay servidor, debe ingresarlo (-syslog_h).")




    while True:

        # Registrar tiempo de inicio en cada ciclo
        start_time=  time.perf_counter()

        # Consultar datos por snmp
        model = snmp_service.query_all_devices(devices, oids_por_categoria, start_time)

        # Analizar los datos snmp de APs, revisa reinicios/reasociaciones/NoisePower
        data_analyzer.analyze(model)

        # Busca datos de APs en NMS, revisa trafico en la puerta del switch 
        ap_notFound, ap_nameDuplicate = nms_service.query_all_ports(model)


        # Exporta los datos a los presentadores especificados (syslog, csv, console)
        exportar_datos(model, presentadores)

        # Calcular tiempo que ha demorado este ciclo
        elapsed_time = time.perf_counter() - start_time

        logger.debug(f"Envio terminado en {elapsed_time:.2f} segundos. ") 

        # Calcular tiempo restante para cumplir con el intervalo
        time_to_sleep = max(0, args.time - elapsed_time)

        logger.info(f"Ciclo completado. Esperando {time_to_sleep:.2f} segundos. [{args.time}  -  {elapsed_time:.2f}]") 

        # Pausa antes de la siguiente iteracion
        time.sleep(time_to_sleep)


if __name__ == '__main__':
    main_loop()

