"""
Einstellungen für das DGM-Projekt.
Definiere hier das Gebiet (Bounding Box) für das ein Höhenmodell erzeugt wird.
"""

# Bounding Box: (min_lon, min_lat, max_lon, max_lat)
# Standard: kleines Gebiet rund um Beelitz, Deutschland
BOUNDING_BOX = (12.94, 52.22, 12.98, 52.25)

# Rasterauflösung: Anzahl Punkte je Achse (z.B. 30 -> 30x30 Raster)
GRID_RESOLUTION = 30

# Ausgabe-Ordner
OUTPUT_DIR = "output"
