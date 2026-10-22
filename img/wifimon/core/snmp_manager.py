# core/snmp_manager.py

from pysnmp.proto.rfc1905 import EndOfMibView
from pysnmp.hlapi import *
from pysnmp.smi import builder, view, rfc1902
import os
from pathlib import Path
from utils.helpers import hexToString
from core.manager_log import logger
from core.snmp_data_model import SNMPDataModel

class SNMPManager:
    # ELIMINADO: Ya no usamos un lock ni una variable de clase compartida.
    # Cada instancia cargará sus propios MIBs.

    def __init__(self, community, port=161):
        self.community = community
        self.port = port

        # --- Carga de MIBs ---
        # Esta sección ahora se ejecuta cada vez que se crea un SNMPManager.
        # En un entorno de multiproceso, esto sucede una vez por proceso hijo.
        dir_path = Path(__file__).resolve().parent.parent
        path_mibs = os.path.join(dir_path, "mib/cisco")

        mib_builder = builder.MibBuilder()
        mib_sources = mib_builder.getMibSources() + (builder.DirMibSource(path_mibs),)
        mib_builder.setMibSources(*mib_sources)

        mib_builder.loadModules(
            'AIRESPACE-WIRELESS-MIB', 'CISCO-LWAPP-AP-MIB',
            'CISCO-LWAPP-SI-MIB', 'CISCO-LWAPP-CDP-MIB'
        )
        # Cada instancia tiene su propio MibViewController.
        self.mibView = view.MibViewController(mib_builder)

    def get_data(self, model: SNMPDataModel, device_ip: str, oids: list):
        oid_list = [rfc1902.ObjectType(rfc1902.ObjectIdentity(entry["oid"])) for entry in oids]
        self._query_snmp(model, device_ip, oid_list)

    def _query_snmp(self, model: SNMPDataModel, device_ip: str, oid_list: list):
        # Se crea un nuevo SnmpEngine para cada consulta, lo cual es seguro.
        snmp_engine = SnmpEngine()
        
        iterator = bulkCmd(
            snmp_engine,
            CommunityData(self.community),
            UdpTransportTarget((device_ip, self.port)),
            ContextData(), 0, 50, *oid_list, lexicographicMode=False
        )

        for errorIndication, errorStatus, errorIndex, varBinds in iterator:
            if errorIndication or errorStatus or errorIndex:
                logger.error(f"[{device_ip}] Error SNMP: {errorIndication or errorStatus or errorIndex}")
                continue

            for oidObj, value in varBinds:
                if isinstance(value, EndOfMibView):
                    continue

                identity = rfc1902.ObjectIdentity(oidObj)
                _, objectName, objectInstanceId = identity.resolveWithMib(self.mibView).getMibSymbol()
                index_parts = [sub_id.prettyPrint() for sub_id in objectInstanceId]
                
                main_value, extra_values = self._process_snmp_value(objectName, value)
                
                main_value = self._convert_to_number(main_value)
                model.add_value(device_ip, objectName, index_parts, main_value)
                
                if extra_values:
                    for key, val in extra_values.items():
                        val = self._convert_to_number(val)
                        model.add_value(device_ip, key, index_parts, val)

    def _convert_to_number(self, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return value

    def _obtener_tercer_valor(self, cadena, defecto="SIN_VALOR"):
        partes = cadena.split(":")
        return partes[2] if len(partes) >= 3 else defecto

    def _process_snmp_value(self, object_name, value):
        extra_values = {}
        main_value = value.prettyPrint()

        if object_name in ("bsnAPDot3MacAddress", "bsnAPEthernetMacAddress", "bsnMobileStationAPMacAddr"):
            main_value = hexToString(value)
        elif object_name in ("cLApUpTime", "cLLwappUpTime"):
            main_value = int(int(value.prettyPrint()) / 100)
        elif object_name == "bsnAPLocation":
            extra_values["geoLocation"] = self._obtener_tercer_valor(main_value)
        elif object_name == "bsnAPName":
            ap_name = main_value
            if len(ap_name) >= 5:
                campus = ap_name[:2]
                if campus in ("ap", "AP"): # cuando el ap recien se registra empieza a llamarse "ap..." y no tiene el formato esperado, entonces asignamos valores por defecto
                    extra_values["Campus"] = "NN"
                    extra_values["NroEdificio"] = 0

                else:

                    extra_values["Campus"] = campus
                    nroEdificio_str = ap_name[2:5]
                    try:
                        extra_values["NroEdificio"] = int(nroEdificio_str)
                    except ValueError:
                        logger.warning(f"El valor '{nroEdificio_str}' no es un número válido para NroEdificio. Asignando 0.")
                        extra_values["NroEdificio"] = 0



        return main_value, extra_values