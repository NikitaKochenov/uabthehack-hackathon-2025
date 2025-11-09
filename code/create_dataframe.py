import pandas as pd
from utils.data_loader import *

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


def mother_table(df_aps: pd.DataFrame, df_clients: pd.DataFrame) -> pd.DataFrame:
    # 1️⃣ Crear columna "edifici" en df_aps
    df_aps = df_aps.copy()
    df_aps["edifici"] = (
        df_aps["name"]
        .astype(str)
        .str.strip()
        .str.upper()
        .replace(r"-+", "-", regex=True)
        .replace(r"\d+", "", regex=True)
    )

    df_aps_slim = (
        df_aps[["serial", "edifici"]]
        .drop_duplicates(subset=["serial"])
        .rename(columns={"serial": "AP", "edifici": "Building"})
    )

    df_clients_slim = (
        df_clients[["macaddr", "file_timestamp", "associated_device"]]
        .drop_duplicates(subset=["macaddr", "file_timestamp", "associated_device"])
        .rename(columns={"macaddr": "Cliente", "file_timestamp": "TimeStamp", "associated_device": "AP"})
    )

    # 3️⃣ Unir clientes con APs
    df_mother = pd.merge(df_clients_slim, df_aps_slim, on="AP", how="left")

    # 4️⃣ Reordenar columnas
    df_mother = df_mother[["TimeStamp", "Building", "AP", "Cliente"]]

    return df_mother


print(mother_table(df_aps, df_clients))