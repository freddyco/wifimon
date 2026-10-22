# core/reboot_tracker.py
import json
import os

class APTracker:
    def __init__(self, filepath="ap_uptime_state.json"):
        self.filepath = filepath
        self.state = self._load_state()

    def _load_state(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                return json.load(f)
        return {}

    def save_state(self):
        with open(self.filepath, "w") as f:
            json.dump(self.state, f, indent=2)

    # Lee valores almacenados en el tracker/state para el ap_id (valores previos)
    # y los compara al valor entregados en los parametros (valores actuales)

    def analyze_tracker(self, ap_id, uptime, lwap_uptime, channel_24, channel_5,name_ap):
        prev_uptime             = self.state.get(ap_id, {}).get("uptime")
        prev_reassociations     = self.state.get(ap_id, {}).get("lwap_uptime")

        prev_channel_24_value = self.state.get(ap_id, {}).get("channel_24")
        prev_channel_5_value = self.state.get(ap_id, {}).get("channel_5")

        
        reboots = 0
        reassociations = 0

        change_channel_24 = 0
        change_channel_5 = 0

        if prev_uptime is not None and uptime < prev_uptime:
            reboots = 1  # Detecta reinicio

        if prev_reassociations is not None and lwap_uptime < prev_reassociations:
            reassociations = 1  # Detecta reassociation


        if prev_channel_24_value is not None and channel_24 != prev_channel_24_value:
            change_channel_24 = 1

        if prev_channel_5_value is not None and channel_5 != prev_channel_5_value:
            change_channel_5 = 1


        # self.state[ap_id] = {
        #     "uptime": uptime,
        #     "lwap_uptime": lwap_uptime,
        #     "nameAP": name_ap,
        #     "reboots": reboots,
        #     "reassociations": reassociations,
            
        #     "change_channel_24": change_channel_24,
        #     "change_channel_5": change_channel_5

        # }

        self.state[ap_id] = {
            "uptime": uptime,
            "lwap_uptime": lwap_uptime,
            "nameAP": name_ap,
            "reboots": reboots,
            "reassociations": reassociations,
            "change_channel_24": change_channel_24,
            "change_channel_5": change_channel_5,
            "channel_24": channel_24,  # Guardamos el canal actual para la siguiente comparación
            "channel_5": channel_5
        }


    # def analyze_tracker(self, ap_id, uptime, lwap_uptime, name_ap):
    #     prev_uptime             = self.state.get(ap_id, {}).get("uptime")
    #     prev_reassociations     = self.state.get(ap_id, {}).get("lwap_uptime")

        
    #     reboots = 0
    #     reassociations = 0

    #     if prev_uptime is not None and uptime < prev_uptime:
    #         reboots = 1  # Detecta reinicio

    #     if prev_reassociations is not None and lwap_uptime < prev_reassociations:
    #         reassociations = 1  # Detecta reassociation

    #     self.state[ap_id] = {
    #         "uptime": uptime,
    #         "lwap_uptime": lwap_uptime,
    #         "nameAP": name_ap,
    #         "reboots": reboots,
    #         "reassociations": reassociations
    #     }


    # Devuelve el número de reinicios ("reboots") del ap_id si existe, 
    # o 0 si no hay registro o no tiene esa clave.
    def get_reboots(self, ap_id):
        return self.state.get(ap_id, {}).get("reboots", 0)


    # Devuelve el número de reasociations ("reasociaciones") del ap_id si existe, 
    # o 0 si no hay registro o no tiene esa clave.
    def get_reassociations(self, ap_id):
        return self.state.get(ap_id, {}).get("reassociations", 0)



    def get_change_channel_24(self, ap_id):
        return self.state.get(ap_id, {}).get("change_channel_24", 0)
    

    def get_change_channel_5(self, ap_id):
        return self.state.get(ap_id, {}).get("change_channel_5", 0)