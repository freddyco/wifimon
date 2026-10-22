import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.manager_log import logger



class NMSManager:
    def __init__(self, api_token, max_workers=10):
        self.api_token = api_token
        self.base_url = 'https://nms.noc.uc.cl/api/v0/'
        self.headers = {
            'X-Auth-Token': self.api_token,
            'Content-Type': 'application/json',
            'accept': 'application/json',
        }
        

        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504, 408])
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount('https://', adapter)
        
        # Parametro para controlar el numero maximo de hilos
        self.max_workers = max_workers

    def search_fdb(self, mac_Tofind):
        #url = f'{self.base_url}ports/search/ifAlias/{ap_name}?columns=port_id%2Cdevice_id%2CifAlias%2CifPhysAddress%2CifName%2CifAdminStatus%2CifOperStatus%2CifDuplex%2CifSpeed%2CifInErrors%2CifInErrors_rate%2CifOutErrors%2CifOutErrors_rate%2CifInOctets_rate%2CifOutOctets_rate'
        url = f'{self.base_url}resources/fdb/{mac_Tofind}'
        #url = f'{self.base_url}fdb/'

        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            #print (response.json())
            return response.json().get('ports_fdb', [])  # Devuelve la lista de interfaces o vacÃ­a
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error en la solicitud search_fdb: {e}")
            return None

    
    
    def search_ap_ifAlias(self, ap_name):
        url = f'{self.base_url}ports/search/ifAlias/{ap_name}?columns=port_id%2Cdevice_id%2CifAlias%2CifPhysAddress%2CifName%2CifAdminStatus%2CifOperStatus%2CifDuplex%2CifSpeed%2CifInErrors%2CifInErrors_rate%2CifOutErrors%2CifOutErrors_rate%2CifInOctets_rate%2CifOutOctets_rate'
        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json().get('ports', [])  # Devuelve la lista de interfaces o vacÃ­a
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error en la solicitud para AP {ap_name}: {e}")
            return None

    # def get_port_details(self, port_id):
    #     url = f'{self.base_url}ports/{port_id}'
    #     try:
    #         response = self.session.get(url, headers=self.headers, timeout=10)
    #         response.raise_for_status()
    #         return response.json().get('port', [{}])[0]
    #     except requests.exceptions.RequestException as e:
    #         logger.warning(f"Error en la solicitud para port_id {port_id}: {e}")
    #         return None

    # def get_device_details(self, device_id):
    #     url = f'{self.base_url}devices/{device_id}'
    #     try:
    #         response = self.session.get(url, headers=self.headers, timeout=10)
    #         response.raise_for_status()
    #         return response.json().get('devices', [{}])[0]
    #     except requests.exceptions.RequestException as e:
    #         logger.warning(f"Error en la solicitud para device_id {device_id}: {e}")
    #         return None

    # def find_interfaces(self, list_devices):
    #     with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
    #         futures = {executor.submit(self.get_port_details, item['port_id']): item for item in list_devices}

    #         for future in as_completed(futures):
    #             item = futures[future]
    #             interface = future.result()

    #             if interface:
    #                 item.update({
    #                     'ifAdminStatus': interface.get('ifAdminStatus'),
    #                     'ifOperStatus': interface.get('ifOperStatus'),
    #                     'ifDuplex': interface.get('ifDuplex'),
    #                     'ifSpeed': interface.get('ifSpeed'),
    #                     'ifInErrors': interface.get('ifInErrors'),
    #                     'ifOutErrors': interface.get('ifOutErrors'),
    #                     'ifInRate_bps': (interface.get('ifInOctets_rate', 0) * 8),
    #                     'ifInRate_percent': round(
    #                         ((interface.get('ifInRate_bps', 0) / interface.get('ifSpeed', 1)) * 100), 3
    #                     ) if interface.get('ifSpeed', 0) > 0 else 0
    #                 })
    #     return list_devices

    # def find_name_ap_interfaces(self, list_name_ap):
    #     list_all_ap = []
    #     with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
    #         futures = {executor.submit(self.search_ap_ifAlias, ap_name): ap_name for ap_name in list_name_ap}

    #         for future in as_completed(futures):
    #             ap_name = futures[future]
    #             interfaces = future.result()

    #             if interfaces:
    #                 for interface in interfaces:
    #                     device_data = self.get_device_details(interface['device_id'])
    #                     if device_data:
    #                         dict_one_ap = {
    #                             'ap_name': ap_name,
    #                             'ifName': interface.get('ifName'),
    #                             'sys_name': device_data.get('sysName'),
    #                             'hardware': device_data.get('hardware'),
    #                             'device_id': interface.get('device_id'),
    #                             'port_id': interface.get('port_id'),
    #                             'is_located': 'true'
    #                         }
    #                         list_all_ap.append(dict_one_ap)
    #             else:
    #                 logger.info(f"No se encontrÃ³ interfaz para el AP {ap_name}")
    #                 list_all_ap.append({'ap_name': ap_name, 'is_located': 'false'})
    #     return list_all_ap



        
    # def get_all_devices(self):
    #     devices = []
    #     page = 1
    #     while True:
    #         url = f'{self.base_url}devices?page={page}'
    #         try:
    #             response = self.session.get(url, headers=self.headers, timeout=10)
    #             response.raise_for_status()
    #             current_page_devices = response.json().get('devices', [])
                
    #             if not current_page_devices:
    #                 break  # Salir si no hay mÃ¡s dispositivos

    #             devices.extend(current_page_devices)
    #             page += 1  # Ir a la siguiente pÃ¡gina
    #         except requests.exceptions.RequestException as e:
    #             logger.error(f"Error obteniendo dispositivos: {e}")
    #             break
    #     return devices


    # def get_all_ports(self):


    #     url = f'{self.base_url}ports?columns=port_id%2Cdevice_id%2CifAlias%2CifPhysAddress%2CifName%2CifAdminStatus%2CifOperStatus%2CifDuplex%2CifSpeed%2CifInErrors%2CifInErrors_rate%2CifOutErrors%2CifOutErrors_rate%2CifInOctets_rate%2CifOutOctets_rate'
    #     try:
    #         response = self.session.get(url, headers=self.headers, timeout=10)
    #         response.raise_for_status()
    #         return response.json().get('ports', [])  # Lista de todos los puertos
    #     except requests.exceptions.RequestException as e:
    #         logger.error(f"Error obteniendo todos los puertos: {e}")
    #         return []


