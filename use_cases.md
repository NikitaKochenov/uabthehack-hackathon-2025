# Use Cases — analysis.py

## average_device_speed(df_clients)
Calculates the average connection speed of all client devices.  
Used to obtain a general measure of network performance.

## average_signal_quality(df_clients)
Computes the average signal strength (in dB) and signal quality across all clients.  
Useful for assessing overall connection health.

## worsts_aps_by_signal_quality(df_clients, top_n=10)
Finds the access points (APs) with the lowest connection quality.  
Used to identify problematic APs needing maintenance or optimization.

## best_aps_by_signal_quality(df_clients, top_n=10)
Finds the access points (APs) with the highest connection quality.  
Used to highlight well-performing APs and benchmark good coverage.

## average_signal_quality_per_ap(df_clients)
Aggregates average signal, strength, and speed for each access point.  
Prepares a clean, grouped DataFrame ready for analysis or scoring.

## calculate_connection_quality(df_clients)
Combines signal strength, dB level, and speed into a single heuristic score.  
Used to rank APs by overall connection quality in a simplified manner.


# Use Cases — basic_graphic_stats.py

## plot_top_aps_usage(df_clients, top_n=15, save=True)
Creates a horizontal bar chart of the top 15 most-used Access Points (APs).  
Used to visualize which APs handle the most connections.

## plot_hourly_activity(df_clients, save=True)
Plots the number of unique connected devices per hour of the day.  
Useful for identifying daily traffic patterns and peak hours.

## plot_weekly_activity(df_clients, save=True)
Displays a line graph showing the number of unique connected devices per weekday.  
Helps understand weekly activity trends and peak days.

## plot_signal_strength_distribution(df_clients, save=True)
Generates two plots: one for signal strength distribution (1–5) and another for signal dB histogram.  
Used to analyze the quality and strength of wireless signals across clients.

## plot_network_types_distribution(df_clients, save=True)
Creates a pie chart showing the proportion of clients using different network types (e.g., EDUROAM, UAB-WIFI).  
Useful for understanding network usage segmentation.

## plot_band_distribution(df_clients, save=True)
Builds a bar chart showing the number of connected devices per WiFi band (2.4GHz, 5GHz, 6GHz).  
Helps assess how devices are distributed across frequency bands.

## plot_top_buildings_by_aps(edificis, top_n=10, save=True)
Displays a horizontal bar chart of the buildings with the highest number of Access Points.  
Used to locate infrastructure density and identify areas with the most AP coverage.


# Use Cases — create_dataframe.py

## mother_table(df_aps, df_clients)
Generates a unified DataFrame linking clients to their associated Access Points and building names.  
Used to create a "master table" for further analysis, reporting, or aggregation of device connections by building.

# Use Cases — graph.py

## building_graph(df_mother_table, building_name, min_weight=1)
Builds a network graph representing client movements between APs within a specific building.  
Used to analyze mobility patterns, AP transitions, and traffic hotspots.

## create_building_graphs(df_mother, df_buildings, min_weight=1)
Generates a dictionary of graphs, one per building, showing client movements between APs.  
Useful for large-scale analysis across multiple buildings and for visualizing movement networks.


# Use Cases — map_distribution.py

## draw_buildings_graph_map(grafos_por_edificio, df_aps, output_file='mapa_aps_grafo.html')
Creates an interactive map showing all APs with their status and draws movement graphs for each building.  
Useful to visualize client transitions, AP load, and building connectivity in a single interactive map.


# Use Cases — map_quality.py

## assign_quality_fuzzy(ap_name, quality_dict, cutoff=0.8)
Finds the closest string match to an AP name in the connection quality dictionary to handle spelling inconsistencies or JSON mismatches.  
Useful to reliably assign a connection quality value even if the AP name is slightly different from the recorded data.


# Use Cases — timestamp_sorting.py

## clients_by_timestamps(df_clients)
Groups all client records by timestamp, keeping the full client information.  
Useful to analyze network activity over time or for time-based aggregation of client behavior.

## timestamp_ap_connections(ts_dict, df_aps)
Transforms the timestamp grouping into a nested dictionary of timestamp → AP → list of clients.  
Useful to quickly see which clients were connected to which AP at any given timestamp.

## get_building_serials(df_aps)
Creates a mapping from AP serial numbers to building names.  
Useful to relate client connections to physical locations and facilitate building-level analysis.

## get_building_by_ap(serial, ap_to_building)
Returns the building corresponding to an AP serial number.  
Useful when needing to quickly identify the physical location of a specific AP or client connection.


# Use Cases — zone_distribution.py

## building_types_distribution(df_aps)
Groups APs by their building name and collects each building's APs in a list, keeping key static fields like serial.  
Useful for understanding AP distribution per building, creating building-level analytics, or generating building-specific graphs.  
It also removes duplicates to ensure each AP is represented only once per building.
