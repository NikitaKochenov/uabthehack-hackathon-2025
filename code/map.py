# map.py

import folium
import geopandas as gpd
from folium import PolyLine
import json
import pandas as pd


def draw_buildings_graph_map(grafos_por_edificio: dict, df_aps, output_file='mapa_aps_grafo.html'):
    """
    Crear un mapa interactivo de APs con los grafos de movimientos por edificio.

    Args:
        grafos_por_edificio: Dict[str, nx.Graph] → grafos precalculados por edificio.
        df_aps: DataFrame con info de APs, incluyendo 'serial' y 'name'.
        output_file: Nombre del archivo HTML donde se guardará el mapa.
    """
    # ---------------------------
    # Cargar datos de geolocalización y WiFi dentro de la función
    # ---------------------------
    gdf_geo = gpd.read_file('./geo_data/aps_geolocalizados_wgs84.geojson')

    print(f"✓ {len(gdf_geo)} APs con geolocalización")

    with open('./anonymized_data/aps/AP-info-v2-2025-04-03T00_00_01+02_00.json', 'r') as f:
        wifi_data = json.load(f)
    df_wifi = pd.DataFrame(wifi_data)
    print(f"✓ {len(df_wifi)} APs WiFi cargados")

    # Combinar datos por nombre de AP
    df_merged = df_wifi.merge(
        gdf_geo[['USER_NOM_A', 'USER_EDIFI', 'Num_Planta', 'geometry']],
        left_on='name',
        right_on='USER_NOM_A',
        how='left'
    )

    gdf_merged = gpd.GeoDataFrame(
        df_merged[df_merged['geometry'].notna()],
        geometry='geometry',
        crs='EPSG:4326'
    )
    print(f"✓ {len(gdf_merged)} APs con geolocalización y datos WiFi combinados")

    # ---------------------------
    # Crear mapa centrado
    # ---------------------------
    m = folium.Map(location=[41.50, 2.10], zoom_start=15)

    # Diccionario para mapear serial/nodo del grafo a USER_NOM_A
    serial_to_user_nom = dict(zip(df_aps['serial'], df_aps['name']))

    # Diccionario de coordenadas: USER_NOM_A -> (lat, lon)
    ap_coords = {row['USER_NOM_A']: (row.geometry.y, row.geometry.x) for _, row in gdf_merged.iterrows()}

    # ---------------------------
    # Dibujar nodos (APs)
    # ---------------------------
    for _, row in gdf_merged.iterrows():
        color = 'green' if row['status'] == 'Up' else 'red'
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=5 + (row['client_count'] / 10),
            popup=f"{row['name']}<br>{row['USER_EDIFI']}<br>Clientes: {row['client_count']}",
            color=color,
            fill=True
        ).add_to(m)

    # ---------------------------
    # Dibujar aristas de los grafos por edificio
    # ---------------------------
    for edificio, G_edif in grafos_por_edificio.items():
        for u, v, data in G_edif.edges(data=True):
            u_map = serial_to_user_nom.get(u)
            v_map = serial_to_user_nom.get(v)
            if u_map in ap_coords and v_map in ap_coords:
                coords = [ap_coords[u_map], ap_coords[v_map]]
                weight = data.get('weight', 1)
                opacity = min(0.3 + 0.7 * (weight / G_edif.size()), 1.0)
                PolyLine(
                    coords,
                    color='blue',
                    weight=2,
                    opacity=opacity,
                    tooltip=f"{u_map} ↔ {v_map}: {weight} movimientos"
                ).add_to(m)

    # ---------------------------
    # Guardar mapa final
    # ---------------------------
    m.save(output_file)
    print(f"✓ Mapa con grafo guardado en {output_file}")
    return m
