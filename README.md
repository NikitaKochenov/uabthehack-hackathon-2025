# 🧠 Projecte: Anàlisi de Moviments Wi-Fi a la UAB

## 📋 Descripció

Aquest projecte analitza les connexions Wi-Fi dels punts d’accés (**APs**) de la **Universitat Autònoma de Barcelona (UAB)** per estudiar el **comportament espacial dels dispositius al llarg del temps**.  
Mitjançant dades anonimitzades dels clients (dispositius) i dels APs, es construeix una sèrie d'eines per visualitzar i comprendre el comportament de la xarxa Wi-Fi dins dels edificis del campus.

A partir d’això, em generat varis mapas interactius i gràfics per visualitzar la situació actual de la xarxa Wi-Fi.

- La localització geogràfica dels APs (nodes).  
- Qualitat mostrada en cada AP segons certs paràmetres.
- Moviment frequent entre APs (arestes).
- Gràfics tenint en compte la temporalitat i l’edifici.

---

## ⚙️ Estructura del projecte

```plaintext
📦 uabthehack-hackathon-2025/
 ┣ 📂 anonymized_data/
 ┃ ┣ 📂 aps/                # Dades anonimitzades dels Access Points
 ┃ ┗ 📂 clients/            # Dades anonimitzades dels clients Wi-Fi
 ┣ 📂 data/
 ┃ ┗ 📂 aps/aps_geolocalizados_wgs84.geojson
 ┣ 📂 code/
 ┃ ┣ analysis.py            # Anàlisi de dades
 ┃ ┣ basic_graphic_stats.py # Gràfics estadístics bàsics
 ┃ ┣ create_dataframe.py    # Creació i manipulació de DataFrames
 ┃ ┣ graph.py               # Creació de grafs per edifici
 ┃ ┣ main.py                # Punt d’entrada principal dins de code
 ┃ ┣ distribution_map.py    # Mapa de distribució d’APs
 ┃ ┣ mapa_aps.html          # Mapes estàtics generats
 ┃ ┣ mapa_aps_grafo.html    # Mapes de grafs generats
 ┃ ┣ mapa_calidad.py        # Anàlisi de qualitat de cobertura
 ┃ ┣ timestamp_sorting.py   # Ordenació i filtratge per timestamps
 ┃ ┗ zone_distribution.py   # Distribució de zones i clients
 ┣ 📂 utils/
 ┃ ┗ data_loader.py       # Funcions per carregar dades
 ┣ 📂 graphics/
 ┃ ┗ (archivos jpg)
 ┣ config.py                  # Configuració visual i estils
 ┗ README.md                  # Aquest document
```
⚠️ Nota important:
Les carpetes data/ i anonymized_data/ no es troben al repositori per motius de confidencialitat i protecció de dades sensibles.
El codi està preparat per treballar amb aquestes dades, però no s’inclouen públicament.

---

## 🧩 Funcionament del pipeline

1. **Càrrega de dades**  
   Les funcions de `utils/data_loader.py` llegeixen i combinen múltiples fitxers JSON dels APs i dels clients Wi-Fi.

2. **Creació de la taula mare (`mother_table`)**  
   Aquesta taula unifica dades de temps (`timestamp`), edifici, AP i client per facilitar anàlisi temporal i espacial.

3. **Distribució d’APs per edifici (`building_types_distribution`)**  
   Es genera una taula que associa cada edifici amb la seva llista d’APs únics.
4. **Creació dels gràfics bàsics (`graphic_basic_stats`)**  
   Es creen gràfics i estadístiques descriptives per entendre la distribució de clients i APs.

5. **Creació dels grafs (`create_building_graphs`)**  
   Cada edifici obté un graf que representa moviments detectats entre APs al llarg del temps.  
   Els **nodes** = APs, les **arestes** = moviments de clients.

6. **Representacións en mapa (`distributon_map` i `map_quality`)**  
   S’integra la informació geogràfica (`GeoJSON`) i emb els dataframes.  
   - **Intensitat del color de les arestes** → freqüència de moviments.  
   - **Grandària i color dels nodes** → estat i quantitat de clients.

---

## 🧰 Requisits

```bash
pip install pandas geopandas folium seaborn networkx matplotlib difflib
```
▶️ Execució

Executa el pipeline complet amb:
python main.py
El resultat generarà un fitxer HTML amb el mapa interactiu:
mapa_aps_grafo.html
Obre’l amb el navegador per explorar els moviments dins de cada edifici.

## 💡 Objectiu i utilitat

L’anàlisi permet:

- 🔍 **Detectar patrons de mobilitat** dins de la xarxa Wi-Fi.  
- 📶 **Identificar APs amb alta connectivitat o transició.**  
- 🏗️ **Ajudar en la planificació de la infraestructura Wi-Fi** del campus.  
- 🕒 **Estudiar la dinàmica d’ocupació** dels espais universitaris al llarg del temps.

---

## 👨‍💻 Autors

Projecte desenvolupat per:
- Víctor Frauca  
- Nikita Kochenov  
- Alexy Lysenko
