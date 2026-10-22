# core/arg_parser.py
import os
import argparse
from core.manager_log import logger
import logging

def parser_args():

    # Variables de entorno
    env_vars = {
        'snmp_community': os.getenv('snmp_community'),
        'snmp_port': int(os.getenv('snmp_port', 161)),
        'time_repeat': os.getenv('time_repeat', 300),
        'syslog_host': os.getenv('syslog_host'),
        'syslog_port': int(os.getenv('syslog_port', 1514)),
        'nms_token': os.getenv('nms_token'),
        'debug': os.getenv('debug', 'false').lower() == 'true',
        'presenters': os.getenv('presenters')
    }


    parser = argparse.ArgumentParser(
        description="Opciones de ejecución del script:",
        allow_abbrev=False  # <--- Esto impide abreviaciones como "-presenter"
        )

    parser.add_argument('-snmp_c', dest='snmp_c',
                        default=env_vars['snmp_community'],
                        help='Nombre de la comunidad SNMP')

    parser.add_argument('-snmp_p', dest='snmp_p', type=int,
                        default=env_vars['snmp_port'],
                        help='Puerto SNMP (default 161)')
    

    parser.add_argument('-time', dest='time',  type=int,
                        default=env_vars['time_repeat'],
                        help='Segundos para repetir consulta snmp (default 300)')

    parser.add_argument('-debug', dest='debug', action='store_true',
                        default=env_vars['debug'],
                        help='Activa el modo debug')

    parser.add_argument('-syslog_h', dest='syslog_h',
                        default=env_vars['syslog_host'],
                        help='IP Servidor Syslog')

    parser.add_argument('-syslog_p', dest='syslog_p', type=int,
                        default=env_vars['syslog_port'],
                        help='Puerto Servidor Syslog (default 1514)')

    parser.add_argument('-presenters', dest='presenters', type=str,
                        default=env_vars['presenters'],
                        help='Lista separada por coma de presentadores: console,csv,syslog')

    parser.add_argument('-nms_token', dest='nms_token',
                        default=env_vars['nms_token'],
                        help='Token de acceso a LibreNMS')


    args, unknown = parser.parse_known_args()

    if unknown:
        logger.warning(f"Argumentos no reconocidos: {' '.join(unknown)}")

    # Configurar nivel de logging
    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)
    logger.debug(f"Argumentos: {args} ") 

    # Validar snmp_c obligatorio
    if not args.snmp_c:
        logger.error("No ha especificado la comunidad SNMP (-snmp_c), debe ingresarla.")
        return False

    # Validar presenters obligatorio
    if not args.presenters:
        logger.error("No ha especificado forma de presentación de los datos (-presenters console/syslog/csv), debe ingresarla.")
        return False

    # Parsear presenters a lista limpia
    args.presenters = [p.strip().lower() for p in args.presenters.split(',') if p.strip()]


    return args