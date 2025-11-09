from utils.data_loader import load_aps, load_clients
import pandas as pd
import numpy as np

# Velocidad media de los dispositivos
def average_device_speed(df_clients: pd.DataFrame) -> float:
    average_speed = float(df_clients['speed'].mean())
    return round(average_speed, 2)

# Calidad media de la señal y la calidad en los clientes
def average_signal_quality(df_clients: pd.DataFrame) -> Tuple[float, float]:
    average_signal = float(df_clients['signal_db'].mean())
    average_quality = float(df_clients['signal_strength'].mean())
    return round(average_signal, 2), round(average_quality, 2)

# Ordenamos de peor a mejor señal por AP
def worsts_aps_by_signal_quality(df_clients: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    df_signal_quality = average_signal_quality_per_ap(df_clients)
    df_sorted = df_signal_quality.sort_values(by='connection_quality').head(top_n)
    return df_sorted

# Ordenamos de mejor a peor señal por AP
def best_aps_by_signal_quality(df_clients: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    df_signal_quality = average_signal_quality_per_ap(df_clients)
    df_sorted = df_signal_quality.sort_values(by='connection_quality', ascending=False).head(top_n)
    return df_sorted

def average_signal_quality_per_ap(df_clients: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula la calidad promedio de señal, fuerza y velocidad por AP.
    Devuelve un DataFrame limpio, sin NaN falsos, listo para análisis o scoring.
    """
    # --- Limpiar nombres de AP ---
    df_clients['associated_device_name'] = df_clients['associated_device_name'].astype(str).str.strip()
    df_clients['associated_device_name'] = df_clients['associated_device_name'].str.replace(r'\s+', '', regex=True)

    # --- Asegurarse de que las columnas existan y sean numéricas ---
    for col in ['signal_db', 'signal_strength', 'speed']:
        if col not in df_clients.columns:
            df_clients[col] = np.nan
        else:
            # Convertir a float, valores no convertibles se vuelven NaN
            df_clients[col] = pd.to_numeric(df_clients[col], errors='coerce')

    # --- Filtrar filas donde cualquiera de las métricas sea NaN ---
    df_clients = df_clients.dropna(subset=['signal_db', 'signal_strength', 'speed'], how='any')

    # --- Agrupar por AP ---
    df_grouped = (
        df_clients
        .groupby('associated_device_name', as_index=False)
        .agg(
            avg_signal_db=('signal_db', 'mean'),
            avg_signal_strength=('signal_strength', 'mean'),
            avg_speed=('speed', 'mean')
        )
    )

    # --- Redondear los valores ---
    for col in ['avg_signal_db', 'avg_signal_strength', 'avg_speed']:
        df_grouped[col] = df_grouped[col].apply(lambda x: round(float(x), 2) if pd.notna(x) else np.nan)

    return df_grouped


def calculate_connection_quality(df_clientes: pd.DataFrame) -> pd.DataFrame:
    """
    Heurística simple para calidad de conexión sin normalización.
    Suma los tres indicadores para obtener un número de calidad.
    """
    df_ap_metrics=average_signal_quality_per_ap(df_clientes)
    df = df_ap_metrics.copy()

    # --- Invertimos avg_signal_db porque más negativo es peor ---
    df['db_score'] = -df['avg_signal_db']  # ej: -(-70) = 70 -> mejor

    # --- Señal y velocidad tal cual ---
    df['strength_score'] = df['avg_signal_strength']
    df['speed_score'] = df['avg_speed']

    # --- Calidad heurística: suma de los tres ---
    df['connection_quality'] = df['db_score'] + df['strength_score'] + df['speed_score']

    return df[['associated_device_name', 'avg_signal_db', 'avg_signal_strength', 'avg_speed', 'connection_quality']]
# --- Cargar datos ---
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

# --- Ejecutar función y ordenar ---
"""
df_average = average_signal_quality_per_ap(df_clients)
df_average_sorted = df_average.sort_values(by="avg_speed", ascending=False)

df_quality=calculate_connection_quality(df_average)
print(df_quality.sort_values(by="connection_quality", ascending=False))
"""
