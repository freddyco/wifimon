from core.nms_manager import NMSManager
from core.manager_log import logger

class NMSService:
    def __init__(self, nms_token):
        self.nms_token = nms_token
        self.client_librenms = NMSManager(self.nms_token, max_workers=20)

    def query_all_ports(self, model) -> tuple:
        """
        Enriches each AP dictionary in `all_data` with port data from NMS based on description/ifAlias.
        Returns two lists:
        1. A list of dictionaries for APs not found in the NMS descriptions/ifAlias.
        2. A list of dictionaries for APs that have duplicate matches in the NMS descriptions/ifAlias.
        """
        ports_found = []  # List to store APs found in NMS
        aps_not_found = model.get_all().items()  
        duplicated_aps = []  # List for storing duplicate APs


        ap_name_filters = [
            "CC1", "CC2", "CC3", "CC4", "CC7", "CC9", "CC0",
            "SJ1", "SJ2", "SJ3", "SJ4", "SJ5", "SJ6", "SJ7", "SJ8", "SJ9",
            "CP9", "LC1", "LC3", "LC4", "LF9", "LX1", "NC1", "OR8", "OR9",
            "SR9", "TE9", "VL1"
        ]

        logger.debug(f"Sending NMS request ")
        
        # Fetch all ports from NMS filtered by AP name patterns
        for ap_name in ap_name_filters:
            port_data = self.client_librenms.search_ap_ifAlias(ap_name)
            if port_data:
                ports_found.extend(port_data)

        logger.debug(f"Finished NMS request ")
        logger.debug(f"Starting AP/switch data consolidation ")

        aps_to_remove = set()  # Set to keep track of APs found

        # Iterate over each AP record in `all_data` (now assuming it's a list of dicts)
        #for ap_info in model:
        for ap_id, valores in model.get_all().items():
            ap_name = valores.get('bsnAPName')  # Assuming 'bsnAPName' exists in each AP dict
            matching_ports = [port for port in ports_found if port['ifAlias'] == ap_name]

            # Compare AP name with the interface alias
            for port in matching_ports:
                if valores['bsnAPName'] == port['ifAlias']:  # This comparison was missing earlier
                    
                    if_speed = port.get('ifSpeed') or 0
                    in_rate = port.get('ifInOctets_rate') or 0
                    out_rate = port.get('ifOutOctets_rate') or 0
                    
                    dic_aux = {
                        'port_id': port['port_id'],
                        'device_id': port['device_id'],
                        'ifName': port['ifName'],
                        'ifAdminStatus': port['ifAdminStatus'],
                        'ifOperStatus': port['ifOperStatus'],
                        'ifDuplex': port['ifDuplex'],
                        'ifSpeed': port['ifSpeed'],
                        'ifInErrors': port['ifInErrors'],
                        'ifOutErrors': port['ifOutErrors'],

                        'ifInRate_bps': in_rate * 8,
                        'ifOutRate_bps': out_rate * 8,
                        'ifInRate_percent': round((in_rate * 8 * 100) / if_speed, 3) if if_speed > 0 else 0,
                        'ifOutRate_percent': round((out_rate * 8 * 100) / if_speed, 3) if if_speed > 0 else 0


                        # 'ifInRate_bps': port['ifInOctets_rate'] * 8,
                        # 'ifOutRate_bps': port['ifOutOctets_rate'] * 8,
                        # 'ifInRate_percent': round((port['ifInOctets_rate'] * 8 * 100) / port['ifSpeed'], 3) if port['ifSpeed'] > 0 else 0,
                        # 'ifOutRate_percent': round((port['ifOutOctets_rate'] * 8 * 100) / port['ifSpeed'], 3) if port['ifSpeed'] > 0 else 0
                    }
                    valores.update(dic_aux)  # Add enriched port data to the AP info
                    aps_to_remove.add(ap_name)  # Mark AP as found

                    # Check if there are duplicate ports
                    if len(matching_ports) > 1:
                        duplicated_aps.append({
                            'port_id': port['port_id'],
                            'device_id': port['device_id'],
                            'ifName': port['ifName']
                        })

        # Create a list of APs that were not found, now comparing by 'bsnAPName'
        aps_not_found = [ap for ap, data in aps_not_found if data.get('bsnAPName') not in aps_to_remove]

        return aps_not_found, duplicated_aps

