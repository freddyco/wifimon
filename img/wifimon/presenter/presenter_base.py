# my_presenter/presenter_base.py
from abc import ABC, abstractmethod
from core.snmp_data_model import SNMPDataModel

class PresenterBase(ABC):
    @abstractmethod
    def export(self, model: SNMPDataModel):
        """Método para exportar datos. Debe ser implementado por todas las subclases."""
        pass
