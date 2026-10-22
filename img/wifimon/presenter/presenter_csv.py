import csv
from core.snmp_data_model import SNMPDataModel
from presenter.presenter_base import PresenterBase
from utils.helpers import get_rounded_timestamp
class PresenterCSV(PresenterBase):

    def __init__(self):

        #timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        timestamp= get_rounded_timestamp()
        output_file = f"{timestamp}_ap.csv"
        self.output_file = output_file

    def export(self, model: SNMPDataModel):
        data = model.get_all()
        if not data:
            print("No data to export.")
            return

        # Recolectar todos los campos posibles
        all_keys = set()
        for values in data.values():
            for k, v in values.items():
                if isinstance(v, dict):
                    all_keys.update(f"{k}_{subk}" for subk in v)
                else:
                    all_keys.add(k)

        # Ordenar las columnas
        fieldnames = ["index"] + sorted(all_keys)

        try:
            with open(self.output_file, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for index, values in data.items():
                    flat_row = {"index": index}
                    for k, v in values.items():
                        if isinstance(v, dict):
                            for subk, subv in v.items():
                                flat_row[f"{k}_{subk}"] = subv
                        else:
                            flat_row[k] = v
                    writer.writerow(flat_row)
            print(f"Datos exportados correctamente a {self.output_file}")
        except Exception as e:
            print(f"Error al exportar el archivo CSV: {e}")
