from data.loader_oid import OIDLoader
from core.manager_log import logger
from typing import Dict, List

class OIDService:
    def __init__(self, path: str):
        self.path = path
        self.loader = OIDLoader(self.path)

    def load_all_by_category(self) -> Dict[str, List[Dict]]:
        data = self.loader.load_file_oids()
        if not data:
            logger.error(f"No se pudo cargar el archivo de OIDs: {self.path}")
            return {}
        return self.loader.get_all_oids_by_category(data)
