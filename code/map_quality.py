import geopandas as gpd
import pandas as pd
import json
from analysis import calculate_connection_quality
from utils.data_loader import *
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from difflib import get_close_matches
import folium

# -----------------------------
# 1. Calcular la calidad de conexión
# -----------------------------
df_clients = load_clients(
    data_dir="../anonymized_data/clients",
    max_files=10,
    verbose=True
)

# Ignorar last_connection_time
if 'last_connection_time' in df_clients.columns:
    df_clients = df_clients.drop(columns=['last_connection_time'])

df_quality = calculate_connection_quality(df_clients)

# Limpiar nombres
df_quality['associated_device_name'] = (
    df_quality['associated_device_name']
    .astype(str)
    .str.strip()
    .str.upper()
)
df_quality = df_quality[df_quality['associated_device_name'] != '']

# Crear diccionario de calidad
quality_dict = df_quality.set_index('associated_device_name')['connection_quality'].to_dict()

# -----------------------------
# 2. Cargar geolocalización y WiFi
# -----------------------------
# GeoJSON
gdf_geo = gpd.read_file('../data/aps_geolocalizados_wgs84.geojson')
print(f"✓ {len(gdf_geo)} APs con geolocalización")

# WiFi snapshot
with open('../anonymized_data/aps/AP-info-v2-2025-04-03T09_25_01+02_00.json', 'r') as f:
    wifi_data = json.load(f)
df_wifi = pd.DataFrame(wifi_data)
print(f"✓ {len(df_wifi)} APs WiFi cargados")

# Merge básico de WiFi + geo
df_merged = df_wifi.merge(
    gdf_geo[['USER_NOM_A', 'USER_EDIFI', 'Num_Planta', 'geometry']],
    left_on='name',
    right_on='USER_NOM_A',
    how='left'
)

# Convertir a GeoDataFrame
gdf_merged = gpd.GeoDataFrame(
    df_merged[df_merged['geometry'].notna()],
    geometry='geometry',
    crs='EPSG:4326'
)
print(f"✓ {len(gdf_merged)} APs con geolocalización y datos WiFi combinados")

# -----------------------------
# 3. Asignar connection_quality con fuzzy matching
# -----------------------------
def assign_quality_fuzzy(ap_name, quality_dict, cutoff=0.8):
    """
    Busca el nombre más parecido en quality_dict y devuelve su quality.
    Si no hay match suficiente, devuelve NaN.
    """
    ap_name_clean = str(ap_name).strip().upper()
    if ap_name_clean in quality_dict:
        return quality_dict[ap_name_clean]

    # fuzzy match
    matches = get_close_matches(ap_name_clean, quality_dict.keys(), n=1, cutoff=cutoff)
    if matches:
        return quality_dict[matches[0]]
    return float('nan')


gdf_merged['connection_quality'] = gdf_merged['USER_NOM_A'].apply(
    lambda x: assign_quality_fuzzy(x, quality_dict)
)

print(gdf_merged[['USER_NOM_A', 'connection_quality']].head(20))
print(f"✓ {gdf_merged['connection_quality'].isna().sum()} APs sin calidad asignada (NaN)")

# -----------------------------
# 4. Crear mapa con escala de colores correcta
# -----------------------------
# Crear mapa centrado en UAB
m = folium.Map(location=[41.50, 2.10], zoom_start=15)

# Preparar colormap
min_quality = gdf_merged['connection_quality'].min()
max_quality = gdf_merged['connection_quality'].max()
norm = mcolors.Normalize(vmin=min_quality, vmax=max_quality)
cmap = plt.cm.get_cmap('RdYlGn')  # alto = verde, bajo = rojo

# Añadir APs al mapa
for idx, row in gdf_merged.iterrows():
    val_norm = norm(row['connection_quality'])
    color = mcolors.to_hex(cmap(val_norm))

    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=5 + (row['client_count'] / 10),
        popup=f"{row['name']}<br>{row['USER_EDIFI']}<br>Clientes: {row['client_count']}<br>Calidad: {row['connection_quality']}",
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

m.save('mapa_aps.html')
print("✓ Mapa guardado en mapa_aps.html")
