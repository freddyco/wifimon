from datetime import datetime, timedelta
from netaddr import *



def timeTicksToString(ticks):
    seconds = ticks/100
    up_time = timedelta(seconds=seconds)
    uptime_str= up_time - datetime.timedelta(microseconds=up_time.microseconds)
    return uptime_str




def hexToString(hex):
    str_mac_address= ':'.join(['%.2x' % x for x in hex.asOctets()])
    return str_mac_address




def get_rounded_timestamp():
    now = datetime.now()
    # Obtener el número de minutos y segundos
    minutes = now.minute
    # Redondear al múltiplo de 5 más cercano
    rounded_minutes = (minutes // 5) * 5
    # Crear una nueva hora con los minutos redondeados
    rounded_time = now.replace(minute=rounded_minutes, second=0, microsecond=0)
    return rounded_time.strftime("%Y%m%d_%H%M")


# def get_rounded_timestamp_to_syslog():
#     now = datetime.now()
#     # Obtener el número de minutos y segundos
#     minutes = now.minute
#     # Redondear al múltiplo de 5 más cercano
#     rounded_minutes = (minutes // 5) * 5
#     # Crear una nueva hora con los minutos redondeados
#     rounded_time = now.replace(minute=rounded_minutes, second=0, microsecond=0)
#     return rounded_time.strftime('%Y-%m-%d %H:%M')


def get_rounded_timestamp_to_syslog():
    now = datetime.now()
    # # Obtener el número de minutos y segundos
    # minutes = now.minute
    # # Redondear al múltiplo de 5 más cercano
    # rounded_minutes = (minutes // 5) * 5
    # # Crear una nueva hora con los minutos redondeados
    # rounded_time = now.replace(minute=rounded_minutes, second=0, microsecond=0)
    return now.strftime('%Y-%m-%d %H:%M')



def hex_to_ip(hex_str):
    # Elimina el prefijo "0x" si está presente
    hex_str = hex_str[2:] if hex_str.startswith("0x") else hex_str
    
    # Asegura que tenga exactamente 8 caracteres (32 bits)
    hex_str = hex_str.zfill(8)
    
    # Divide en bloques de 2 caracteres y conviértelos a enteros
    ip_parts = [str(int(hex_str[i:i+2], 16)) for i in range(0, 8, 2)]
    
    # Une los bloques con puntos
    return ".".join(ip_parts)



def oid_tail_to_mac(oid_tail):
    parts = oid_tail.split('.')
    mac_parts = parts[:6]
    return ':'.join(f"{int(p):02X}" for p in mac_parts)
