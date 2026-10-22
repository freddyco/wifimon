from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, List
from core.snmp_manager import SNMPManager
from core.snmp_data_model import SNMPDataModel
from core.manager_log import logger
import time


# ---------------------------------------------------------------------------
# Worker — ejecuta consultas SNMP y mide tiempos
# ---------------------------------------------------------------------------
def process_query_device(device: Dict, categories: List[str], oids_por_categoria: Dict,
                         community: str, port: int) -> Dict:
    """
    Ejecuta consultas SNMP a un dispositivo y devuelve:
      - Modelo SNMPDataModel con los datos
      - Tiempo total y por categoría
    """
    ip = device.get("ip", "unknown")
    start_total = time.perf_counter()
    manager = SNMPManager(community, port)
    model = SNMPDataModel()

    logger.debug(f"[{ip}] Worker iniciado")

    tiempos_categoria = {}

    for categoria in categories:
        oids = oids_por_categoria.get(categoria, [])
        if not oids:
            logger.warning(f"[{ip}] Categoría '{categoria}' sin OIDs definidos.")
            continue

        start_cat = time.perf_counter()
        manager.get_data(model, ip, oids)
        end_cat = time.perf_counter()
        tiempos_categoria[categoria] = round(end_cat - start_cat, 3)

        logger.debug(f"[{ip}] '{categoria}' completada en {end_cat - start_cat:.2f} s")

    end_total = time.perf_counter()
    elapsed_total = end_total - start_total

    logger.info(f"[{ip}] Worker finalizado en {elapsed_total:.2f} s")

    return {
        "ip": ip,
        "model": model,
        "elapsed_total": elapsed_total,
        "tiempos_categoria": tiempos_categoria,
    }


# ---------------------------------------------------------------------------
# Servicio SNMP — coordina los procesos y mide integración
# ---------------------------------------------------------------------------
class SNMPService:
    def __init__(self, categorias: List[str], community: str, port: int):
        self.categorias = categorias
        self.community = community
        self.port = port

    def query_all_devices(self, devices: List[Dict],
                          oids_por_categoria: Dict[str, List[Dict]],
                          start_time_global=None) -> SNMPDataModel:
        modelo_final = SNMPDataModel()
        tiempos_por_dispositivo = {}

        start_global = time.perf_counter()
        with ProcessPoolExecutor() as executor:
            futures = {
                executor.submit(
                    process_query_device,
                    d,
                    self.categorias,
                    oids_por_categoria,
                    self.community,
                    self.port
                ): d for d in devices
            }

            logger.info(f"Lanzados {len(futures)} procesos para consultar dispositivos.")

            for future in as_completed(futures):
                device_info = futures[future]
                ip = device_info.get("ip", "unknown")

                try:
                    result = future.result()
                    result_model = result["model"]
                    elapsed_total = result["elapsed_total"]

                    # 🔹 Medimos tiempo de integración (merge)
                    merge_start = time.perf_counter()
                    modelo_final.merge(result_model)
                    merge_end = time.perf_counter()
                    elapsed_merge = merge_end - merge_start

                    tiempos_por_dispositivo[ip] = {
                        "snmp": elapsed_total,
                        "merge": elapsed_merge,
                        "categorias": result["tiempos_categoria"]
                    }

                    logger.debug(
                        f"[{ip}] Integrado en {elapsed_merge:.4f} s "
                        f"(consulta SNMP {elapsed_total:.2f} s)"
                    )

                except Exception as e:
                    logger.error(f"[{ip}] Falló el proceso: {e}", exc_info=True)

        end_global = time.perf_counter()
        total_time = end_global - start_global

        # -------------------------------------------------------------------
        # Resumen de tiempos
        # -------------------------------------------------------------------
        if tiempos_por_dispositivo:
            total_snmp = sum(v["snmp"] for v in tiempos_por_dispositivo.values())
            total_merge = sum(v["merge"] for v in tiempos_por_dispositivo.values())
            avg_snmp = total_snmp / len(tiempos_por_dispositivo)
            avg_merge = total_merge / len(tiempos_por_dispositivo)

            slowest = max(tiempos_por_dispositivo, key=lambda x: tiempos_por_dispositivo[x]["snmp"])
            fastest = min(tiempos_por_dispositivo, key=lambda x: tiempos_por_dispositivo[x]["snmp"])

            logger.info(
                f"\n=== Resumen SNMP ===\n"
                f"Dispositivos: {len(tiempos_por_dispositivo)}\n"
                f"Tiempo total global: {total_time:.2f} s\n"
                f"Tiempo total SNMP: {total_snmp:.2f} s\n"
                f"Tiempo total merge: {total_merge:.2f} s\n"
                f"Promedio SNMP por dispositivo: {avg_snmp:.2f} s\n"
                f"Promedio merge por dispositivo: {avg_merge:.4f} s\n"
                f"Más lento (SNMP): {slowest} = {tiempos_por_dispositivo[slowest]['snmp']:.2f} s\n"
                f"Más rápido (SNMP): {fastest} = {tiempos_por_dispositivo[fastest]['snmp']:.2f} s\n"
            )
        else:
            logger.warning("No se obtuvieron resultados de ningún dispositivo.")

        return modelo_final
