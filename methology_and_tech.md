# Project Overview

This project focuses on analyzing and visualizing Wi-Fi access point (AP) data and client connection quality across the UAB campus. It combines **data analysis**, **geospatial processing**, and **network performance evaluation** methodologies to generate meaningful insights from anonymized datasets.

---

## Methodologies

The workflow follows a structured **data engineering pipeline** consisting of:
1. **Data Ingestion** – Loading anonymized Wi-Fi and client data from JSON and CSV sources.  
2. **Preprocessing** – Cleaning inconsistent fields, normalizing names, and removing irrelevant columns.  
3. **Transformation** – Merging datasets, calculating connection quality metrics, and performing fuzzy matching to align AP identifiers.  
4. **Analysis** – Evaluating client distribution, connection performance, and building-level aggregation.  
5. **Visualization** – Generating geospatial and color-graded interactive maps using Folium.

---

## Technologies Used

- **Python** – Main programming language.  
- **pandas** and **NumPy** – Data manipulation and statistical processing.  
- **GeoPandas** – Handling of spatial data and coordinates.  
- **matplotlib** and **matplotlib.colors** – Color normalization and colormap generation.  
- **folium** – Creation of interactive maps with geolocated Wi-Fi access points.  
- **json** – Parsing and processing structured Wi-Fi data.  
- **difflib (fuzzy matching)** – Matching AP names across datasets with inconsistent naming.  

---

## Resources and Tools

- **Jupyter Notebooks / PyCharm** – Used for data exploration and development.  
- **Git & GitHub** – Version control, repository hosting, and collaborative development.  
- **Anonymized datasets** – Containing access point information, client connections, and geolocation data in GeoJSON format.  
- **Custom utility modules** – For modular loading, merging, and processing of data (`data_loader.py`, `analysis.py`, etc.).  

---

## Outcome

The project results in an **interactive geospatial visualization** showing the distribution and connection quality of Wi-Fi access points across the campus.  
This tool helps identify areas of poor connectivity and supports data-driven infrastructure improvements.

