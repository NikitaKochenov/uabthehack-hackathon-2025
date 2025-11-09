from utils.basic_graphic_stats import plot_band_distribution
from utils.data_loader import *
from utils.basic_stats import *
from utils.basic_graphic_stats import *
from utils.mother_table import *
from utils.graph import *
from utils.map import *
from config import setup_visuals

# Ajustes visuales
setup_visuals()

# Cargar Access Points
df_aps = load_aps(data_dir="anonymized_data/aps", max_files=600, verbose=True)
print(f"🎯 APs cargados: {len(df_aps):,} registros")
# Cargar Clientes
df_clients = load_clients(data_dir="anonymized_data/clients", max_files=600, verbose=True)
print(f"🎯 Clientes cargados: {len(df_clients):,} registros")

# Crear tabla madre uniendo TimeStamps, Edificios, APs y Clientes
df_mother = mother_table(df_aps, df_clients)
# Crear tabla de edificios uniendolos con sus APs
df_buildings = building_types_distribution(df_aps)

# Ejecutamos todos los plot
plot_band_distribution(df_clients)
plot_hourly_activity(df_clients)
plot_network_types_distribution(df_clients)
plot_signal_strength_distribution(df_clients)
plot_top_aps_usage(df_clients)
plot_top_buildings_by_aps(df_buildings)
plot_weekly_activity(df_clients)



# Crear lista de grafos por edificio
grafos_por_edificio = create_building_graphs(df_mother, df_buildings, min_weight=25)

m = draw_buildings_graph_map(
    grafos_por_edificio=grafos_por_edificio,
    df_aps=df_aps,
    output_file='mapa_aps_grafo.html'
)