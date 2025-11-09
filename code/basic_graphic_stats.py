import matplotlib.pyplot as plt
import pandas as pd
import os

# Top 15 APs más utilizados
def plot_top_aps_usage(df_clients: pd.DataFrame, top_n: int = 15, save: bool = True):
    top_aps_usage = df_clients['associated_device_name'].value_counts().head(top_n)

    plt.figure(figsize=(12, 6))
    top_aps_usage.plot(kind='barh', color='steelblue')
    plt.title('📡 Top 15 Access Points Más Utilizados', fontsize=16, fontweight='bold')
    plt.xlabel('Número de Conexiones', fontsize=12)
    plt.ylabel('Access Point', fontsize=12)
    plt.gca().invert_yaxis()
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()

    # Guardar imagen
    if save:
        path = os.path.join("media_stats", "top_aps_usage.jpg")
        plt.savefig(path, format='jpg', dpi=300)
        print(f"📁 Gráfico guardado en: {path}")

    plt.close()

    print(f"\n🔥 El AP más usado es: {top_aps_usage.index[0]} con {top_aps_usage.values[0]:,} conexiones")


# Actividad por hora del día
def plot_hourly_activity(df_clients: pd.DataFrame, save: bool = True):
    hourly_activity = df_clients.groupby('hour')['macaddr'].nunique()


    plt.figure(figsize=(14, 6))
    plt.plot(hourly_activity.index, hourly_activity.values, marker='o', linewidth=2, markersize=8, color='coral')
    plt.fill_between(hourly_activity.index, hourly_activity.values, alpha=0.3, color='coral')
    plt.title('⏰ Dispositivos Conectados por Hora del Día', fontsize=16, fontweight='bold')
    plt.xlabel('Hora del Día (0-23)', fontsize=12)
    plt.ylabel('Número de Dispositivos', fontsize=12)
    plt.xticks(range(0, 24))
    plt.grid(alpha=0.3)
    plt.tight_layout()

    if save:
        path = os.path.join("media_stats", "hourly_activity.jpg")
        plt.savefig(path, format='jpg', dpi=300)
        print(f"📁 Gráfico guardado en: {path}")

    plt.close()

    peak_hour = hourly_activity.idxmax()
    peak_devices = hourly_activity.max()
    print(f"\n🕐 Hora pico: {peak_hour}:00 con {peak_devices:,} dispositivos conectados")

# Actividad por día de la semana
def plot_weekly_activity(df_clients: pd.DataFrame, save: bool = True):
    # Agrupar por día de la semana
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_activity = df_clients.groupby('day_of_week')['macaddr'].nunique().reindex(day_order)

    plt.figure(figsize=(14, 6))
    plt.plot(weekly_activity.index, weekly_activity.values, marker='o', linewidth=2, markersize=8, color='mediumseagreen')
    plt.fill_between(weekly_activity.index, weekly_activity.values, alpha=0.3, color='mediumseagreen')
    plt.title('📅 Dispositivos Conectados por Día de la Semana', fontsize=16, fontweight='bold')
    plt.xlabel('Día de la Semana', fontsize=12)
    plt.ylabel('Número de Dispositivos', fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()

    if save:
        os.makedirs("media_stats", exist_ok=True)
        path = os.path.join("media_stats", "weekly_activity.jpg")
        plt.savefig(path, format='jpg', dpi=300)
        print(f"📁 Gráfico guardado en: {path}")

    plt.close()

    # Día pico
    peak_day = weekly_activity.idxmax()
    peak_devices = weekly_activity.max()
    print(f"\n📆 Día pico: {peak_day} con {peak_devices:,} dispositivos conectados")

    # --- Mostrar información del pico ---
    peak_day = weekly_activity.idxmax()
    peak_devices = weekly_activity.max()
    print(f"\n📆 Día pico: {peak_day} con {peak_devices:,} dispositivos conectados")



# Distribución de signal_strength (1-5)
def plot_signal_strength_distribution(df_clients: pd.DataFrame, save: bool = True):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Gráfico 1: Signal Strength (1-5)
    signal_counts = df_clients['signal_strength'].value_counts().sort_index()
    axes[0].bar(signal_counts.index, signal_counts.values, color='seagreen', alpha=0.7)
    axes[0].set_title('📶 Distribución de Calidad de Señal (1-5)', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Signal Strength (1=peor, 5=mejor)', fontsize=11)
    axes[0].set_ylabel('Número de Dispositivos', fontsize=11)
    axes[0].set_xticks([1, 2, 3, 4, 5])
    axes[0].grid(axis='y', alpha=0.3)

    # Gráfico 2: Signal dB (histograma)
    axes[1].hist(df_clients['signal_db'].dropna(), bins=30, color='royalblue', alpha=0.7, edgecolor='black')
    axes[1].set_title('📊 Distribución de Señal (dBm)', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Señal (dBm)', fontsize=11)
    axes[1].set_ylabel('Frecuencia', fontsize=11)
    axes[1].axvline(x=-60, color='red', linestyle='--', label='Umbral débil (-60 dBm)')
    axes[1].legend()
    axes[1].grid(axis='y', alpha=0.3)

    plt.tight_layout()

    if save:
        path = os.path.join("media_stats", "signal_strength_distribution.jpg")
        plt.savefig(path, format='jpg', dpi=300)
        print(f"📁 Gráfico guardado en: {path}")

    plt.close()

    # Estadísticas
    avg_signal = df_clients['signal_db'].mean()
    weak_signal = (df_clients['signal_db'] < -60).sum()
    pct_weak = (weak_signal / len(df_clients)) * 100

    print(f"\n📡 Señal promedio: {avg_signal:.1f} dBm")
    print(f"⚠️  Dispositivos con señal débil (<-60 dBm): {weak_signal:,} ({pct_weak:.1f}%)")

# Distribución por tipo de red
def plot_network_types_distribution(df_clients: pd.DataFrame, save: bool = True):
    network_counts = df_clients['network'].value_counts()

    plt.figure(figsize=(8, 8))
    colors = ['#3498db', '#e74c3c']
    plt.pie(
        network_counts.values,
        labels=network_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        textprops={'fontsize': 14, 'weight': 'bold'}
    )
    plt.title('🌐 Distribución por Tipo de Red', fontsize=16, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()

    # Guardar imagen
    if save:
        path = os.path.join("media_stats", "network_types_distribution.jpg")
        plt.savefig(path, format='jpg', dpi=300)
        print(f"📁 Gráfico guardado en: {path}")

    plt.close()

    print("\n📊 Desglose por red:")
    for network, count in network_counts.items():
        pct = (count / len(df_clients)) * 100
        print(f"   {network}: {count:,} dispositivos ({pct:.1f}%)")


# Distribución por banda
def plot_band_distribution(df_clients: pd.DataFrame, save: bool = True):
    band_counts = df_clients['band'].value_counts().sort_index()
    band_labels = {2.4: '2.4 GHz', 5: '5 GHz', 6: '6 GHz'}

    plt.figure(figsize=(10, 6))
    colors_band = ['#f39c12', '#9b59b6', '#1abc9c']
    bars = plt.bar(
        [band_labels.get(x, str(x)) for x in band_counts.index],
        band_counts.values,
        color=colors_band[:len(band_counts)],
        alpha=0.8
    )
    plt.title('📻 Distribución por Banda WiFi', fontsize=16, fontweight='bold')
    plt.xlabel('Banda', fontsize=12)
    plt.ylabel('Número de Dispositivos', fontsize=12)
    plt.grid(axis='y', alpha=0.3)

    # Añadir valores encima de las barras
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2.,
            height,
            f'{int(height):,}',
            ha='center',
            va='bottom',
            fontsize=11,
            fontweight='bold'
        )

    plt.tight_layout()

    # Guardar imagen
    if save:
        path = os.path.join("media_stats", "band_distribution.jpg")
        plt.savefig(path, format='jpg', dpi=300)
        print(f"📁 Gráfico guardado en: {path}")

    plt.close()

# Top edificios con más APs
def plot_top_buildings_by_aps(edificis: pd.DataFrame, top_n: int = 10, save: bool = True):
    # 1️⃣ Calcular el número de APs por edificio
    edificis['num_aps'] = edificis['array_aps'].apply(len)
    top_buildings = edificis.sort_values('num_aps', ascending=False).head(top_n)

    # 2️⃣ Crear el gráfico
    plt.figure(figsize=(12, 6))
    plt.barh(top_buildings['edifici'], top_buildings['num_aps'], color='slateblue', alpha=0.8)
    plt.title(f'🏢 Top {top_n} Edificios con Más Access Points', fontsize=16, fontweight='bold')
    plt.xlabel('Número de Access Points', fontsize=12)
    plt.ylabel('Edificio', fontsize=12)
    plt.gca().invert_yaxis()
    plt.grid(axis='x', alpha=0.3)

    # Añadir etiquetas con valores
    for i, (count, name) in enumerate(zip(top_buildings['num_aps'], top_buildings['edifici'])):
        plt.text(count + 0.1, i, str(count), va='center', fontsize=11, fontweight='bold')

    plt.tight_layout()

    # 3️⃣ Guardar el gráfico
    if save:
        os.makedirs("media_stats", exist_ok=True)
        path = os.path.join("media_stats", "top_buildings_by_aps.jpg")
        plt.savefig(path, format='jpg', dpi=300)
        print(f"📁 Gráfico guardado en: {path}")

    plt.close()

    # 4️⃣ Mostrar resumen
    top_building = top_buildings.iloc[0]
    print(f"\n🏆 Edificio con más APs: {top_building['edifici']} ({top_building['num_aps']} APs)")
