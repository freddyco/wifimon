from core.nms_manager import NMSManager
import time
from core.manager_log import logger

if __name__ == '__main__':

    # Registrar tiempo de inicio en cada ciclo
    start_time=  time.perf_counter()

    ap_name_filters = [
        "CC1", "CC2", "CC3", "CC4", "CC7", "CC9", "CC0",
        "SJ1", "SJ2", "SJ3", "SJ4", "SJ5", "SJ6", "SJ7", "SJ8", "SJ9",
        "CP9", "LC1", "LC3", "LC4", "LF9", "LX1", "NC1", "OR8", "OR9",
        "SR9", "TE9", "VL1"
    ]

    ports_found = []  # List to store APs found in NMS
    nms_manager  = NMSManager("02f734d7e4badc974bfe8d7e84c88810")
    

    for ap_name in ap_name_filters:
        port_data = nms_manager.search_ap_ifAlias(ap_name)
        if port_data:
            print("voy por otro")
            ports_found.extend(port_data)

    print(ports_found)

    # Calcular tiempo que ha demorado este ciclo
    elapsed_time = time.perf_counter() - start_time
    logger.info(f"Terminado en {elapsed_time:.2f} segundos. ") 