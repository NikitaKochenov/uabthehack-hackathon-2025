import pandas as pd
import networkx as nx
from typing import Dict

def building_graph(df_mother_table: pd.DataFrame, building_name: str, min_weight: int = 1):
    # 1️⃣ Filtrar por edificio
    df = df_mother_table[df_mother_table["Building"] == building_name].copy()

    # 2️⃣ Ordenar por cliente y timestamp
    df = df.sort_values(["Cliente", "TimeStamp"])

    # 3️⃣ Detectar cambios de AP (movimientos)
    df["prev_AP"] = df.groupby("Cliente")["AP"].shift(1)
    df["moved"] = (df["AP"] != df["prev_AP"]) & df["prev_AP"].notna()

    # 4️⃣ Filtrar movimientos
    df_moves = df[df["moved"]].copy()

    # 5️⃣ Crear aristas no dirigidas
    df_moves["edge"] = df_moves.apply(
        lambda r: tuple(sorted([r["prev_AP"], r["AP"]])), axis=1
    )

    # 6️⃣ Contar movimientos entre pares de APs
    edges = df_moves["edge"].value_counts().reset_index()
    edges.columns = ["edge", "weight"]

    # 7️⃣ Aplicar filtro de peso mínimo
    edges = edges[edges["weight"] >= min_weight]

    # 8️⃣ Construir el grafo
    G = nx.Graph()
    for (a, b), w in edges.values:
        G.add_edge(a, b, weight=w)

    return G

def create_building_graphs(df_mother: pd.DataFrame, df_buildings: pd.DataFrame, min_weight: int = 1) -> Dict[str, nx.Graph]:
    """
    Crear un grafo de movimientos de clientes por cada edificio.

    Args:
        df_mother: DataFrame con columnas ['TimeStamp', 'Building', 'AP', 'Cliente'].
        df_buildings: DataFrame con columnas ['edifici', 'array_aps'] que indica los APs de cada edificio.
        min_weight: Peso mínimo para incluir una arista en el grafo.

    Returns:
        Dict[str, nx.Graph]: Diccionario edificio -> grafo de movimientos.
    """
    grafos_por_edificio = {}

    for _, row in df_buildings.iterrows():
        edificio = row['edifici']
        aps_en_edificio = [ap['serial'] for ap in row['array_aps']]

        # Filtrar df_mother solo con APs de este edificio
        df_mother_edif = df_mother[df_mother['AP'].isin(aps_en_edificio)]

        if df_mother_edif.empty:
            continue  # No hay datos para este edificio

        # Crear grafo usando la función existente building_graph
        G_edif = building_graph(df_mother_edif, edificio, min_weight=min_weight)
        grafos_por_edificio[edificio] = G_edif

    return grafos_por_edificio