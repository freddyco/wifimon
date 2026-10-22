from core.data_tracker import APTracker
from core.snmp_data_model import SNMPDataModel
from core.manager_log import logger

class DataAnalyzer:
    def __init__(self):
        self.tracker = APTracker()

    # trackea cada item del modelo y lo analiza segun lo especificado en analyze_tracker()
    # posteriormente save/guarda el trackeo


    def analyze(self, model: SNMPDataModel):
        self.analyze_changes(model)
        self.filter_noise_power_by_channel(model)



    def analyze_changes(self, model):

        for ap_id, valores in model.get_all().items():
            uptime      = valores.get("cLApUpTime")
            lwap_uptime = valores.get("cLLwappUpTime")
            name_ap     = valores.get("bsnAPName")

            channel_number  = valores.get("bsnAPIfPhyChannelNumber", {})

            # Extrae canal 2.4 GHz (índice 0) y canal 5 GHz (índice 1)
            channel_24     = channel_number.get("0")
            channel_5      = channel_number.get("1")


            if uptime is not None:
                self.tracker.analyze_tracker(ap_id, uptime, lwap_uptime,channel_24,channel_5 , name_ap)
                model.data[ap_id]["reboots"]            = self.tracker.get_reboots(ap_id)
                model.data[ap_id]["reassociations"]     = self.tracker.get_reassociations(ap_id)

                model.data[ap_id]["change_channel_24"]   = self.tracker.get_change_channel_24(ap_id)
                model.data[ap_id]["change_channel_5"]    = self.tracker.get_change_channel_5(ap_id)

            # else:
            #     logger.debug(f"No se encontro 'cLApUpTime' en {ap_id}")

        self.tracker.save_state()


    # El modelo tiene los siguientes campos bsnAPIfPhyChannelNumber, bsnAPIfDBNoisePower
    # bsnAPIfPhyChannelNumber: {'0': 11, '1': 36}
    # bsnAPIfDBNoisePower: {'0': {'1': -95, '2': -96, ..., '10': -94, '11': -93, '12': -93, '13': -87, '14': -88}, '1': {'34': -128, '36': -94, ...}}
    # filter_noise_power_by_channel deja solo bsnAPIfDBNoisePower: {'0': -93, '1': -94 }, 
    # eliminando el canal, ya que se obtiene en bsnAPIfPhyChannelNumber


    def filter_noise_power_by_channel(self, model: SNMPDataModel):
        for ap_id, ap_data in model.get_all().items():
            phy_channels = ap_data.get("bsnAPIfPhyChannelNumber")
            noise_power = ap_data.get("bsnAPIfDBNoisePower")

            if not isinstance(phy_channels, dict) or not isinstance(noise_power, dict):
                continue  # Saltar si no tiene la estructura esperada

            simplified_noise = {}

            for band, channel in phy_channels.items():
                band_str = str(band)
                channel_str = str(channel)

                band_noise_data = noise_power.get(band_str)
                if isinstance(band_noise_data, dict):
                    noise_value = band_noise_data.get(channel_str)
                    if noise_value is not None:
                        simplified_noise[band_str] = noise_value

            ap_data["bsnAPIfDBNoisePower"] = simplified_noise



