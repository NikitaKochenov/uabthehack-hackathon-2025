import pandas as pd
import re
from utils.data_loader import *
from zone_distribution import building_types_distribution

# -----------------------------
# Funciones para gestionar timestamps y APs
# -----------------------------
def clients_by_timestamps(df_clients: pd.DataFrame):
    """Agrupa clientes por timestamp, guardando todo el registro"""
    timestamps = dict()
    for idx, row in df_clients.iterrows():
        ts = row['file_timestamp']
        if ts not in timestamps:
            timestamps[ts] = []
        timestamps[ts].append(row.to_dict())  # guardar todo el registro
    return timestamps

def timestamp_ap_connections(ts_dict, df_aps: pd.DataFrame):
    """Devuelve diccionario timestamp -> AP -> lista de clientes"""
    result = dict()
    for ts, clients in ts_dict.items():
        ts_ap_dict = dict()
        for client in clients:
            ap = client["associated_device"]
            if ap not in ts_ap_dict:
                ts_ap_dict[ap] = []
            ts_ap_dict[ap].append(client)
        result[ts] = ts_ap_dict
    return result

def get_building_serials(df_aps: pd.DataFrame):
    """Genera diccionario serial AP -> edificio"""
    buildings = building_types_distribution(df_aps)
    ap_to_building = dict()
    for index, row in buildings.iterrows():
        building_name = row["edifici"]
        for ap in row["array_aps"]:
            serial = ap["serial"]
            ap_to_building[serial] = building_name
    return ap_to_building

def get_building_by_ap(serial: str, ap_to_building: dict) -> str:
    """Devuelve el edificio de un AP por su serial"""
    return ap_to_building.get(serial, "Desconocido")

# -----------------------------
# Cargar datos
# -----------------------------
df_aps = load_aps(
    data_dir="../anonymized_data/aps",
    max_files=10,
    verbose=True
)

df_clients = load_clients(
    data_dir="../anonymized_data/clients",
    max_files=10,
    verbose=True
)

# -----------------------------
# Generar diccionarios y agrupaciones
# -----------------------------
ts_dict = clients_by_timestamps(df_clients)
ts_ap_connections = timestamp_ap_connections(ts_dict, df_aps)
building_serials = get_building_serials(df_aps)

# -----------------------------
# Ejemplo de impresión de resultados
# -----------------------------
for ts, ap_dict in ts_ap_connections.items():
    print(f"\n📅 Timestamp: {ts}")
    for ap, clients in ap_dict.items():
        print(f"  🔌 AP: {ap}")
        for client in clients:
            print(f"    • Cliente: {client['macaddr']}, señal: {client.get('signal_db', 'N/A')}")