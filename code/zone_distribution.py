import pandas as pd
from utils.data_loader import *
def building_types_distribution(df_aps: pd.DataFrame):
    # Definimos los campos estáticos que nos interesan guardar
    static_fields = [
        "serial"
    ]
    # Crear columna "building_type" a partir del nombre
    df_aps = df_aps.copy()
    df_aps["edifici"] = (
        df_aps["name"]
        .astype(str)
        .str.strip()
        .str.upper()
        .replace(r"-+", "-", regex=True)
        .replace(r"\d+", "", regex=True)
    )

    # Agrupar por building_type y recolectar los APs con sus datos estáticos
    buildings_data = (
        df_aps
        .groupby("edifici")
        .apply(lambda g: g[static_fields].to_dict(orient="records"))
        .reset_index(name="array_aps")
    )

    # Eliminar duplicados dentro de cada array_aps
    def deduplicate_ap_list(ap_list):
        seen = set()
        unique_list = []
        for ap in ap_list:
            # Usar MAC como identificador único, si no existe usar serial o name
            ap_id = ap.get("serial")
            if ap_id not in seen:
                seen.add(ap_id)
                unique_list.append(ap)
        return unique_list

    buildings_data["array_aps"] = buildings_data["array_aps"].apply(deduplicate_ap_list)

    return buildings_data


df_aps = load_aps(
    data_dir="../anonymized_data/aps",
    max_files=10,
    verbose=True
)
print(building_types_distribution(df_aps))