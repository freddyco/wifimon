from data.loader_device import DeviceLoader
from core.manager_log import logger
from typing import List, Dict

class DeviceService:
    def __init__(self, path: str):
        self.path = path

    def load_devices(self) -> List[Dict]:
        loader = DeviceLoader(self.path)
        devices = loader.load_file_devices()
        if not devices:
            logger.error(f"No se pudieron cargar los dispositivos desde: {self.path}")
        return devices or []
