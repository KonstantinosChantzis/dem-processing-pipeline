# Digital Elevation Model (DEM) Processing Pipeline

**[English](#english) | [Deutsch](#deutsch)**

---

## English

A portfolio project that builds a simple digital elevation model (DEM) from
freely available elevation data, computes slope, and generates contour
lines — a lightweight version of terrain-model workflows used in
infrastructure and construction project planning.

### What this project does

1. Builds a regular grid of coordinates within a chosen bounding box
2. Queries elevation for each point via the free **Open-Elevation API** (no
   API key required)
3. Processes the elevation grid:
   - Computes slope (in degrees) using `numpy.gradient`
   - Generates contour lines using `matplotlib`
4. Exports:
   - Elevation raster as GeoTIFF (`output/dgm.tif`)
   - Slope raster as GeoTIFF (`output/slope.tif`)
   - Contour lines as a Shapefile (`output/hoehenlinien.shp`)

All outputs open directly in QGIS.

### Tech stack

Python (numpy, pandas, requests, matplotlib, rasterio, geopandas)

### Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Edit `config.py` to set the bounding box for your area of interest, then:

```bash
python fetch_elevation.py
python process_dgm.py
```

### Note on data source

Open-Elevation is a free, community-run service and can be slow or
occasionally unavailable. For a production workflow, this would be replaced
with a proper LiDAR or Copernicus DEM data source.

### License

Elevation data via Open-Elevation (open data, various sources including
SRTM).

---

## Deutsch

Ein Portfolio-Projekt, das aus frei verfügbaren Höhendaten ein einfaches
digitales Geländemodell (DGM) erstellt, die Hangneigung berechnet und
Höhenlinien erzeugt — eine leichtgewichtige Version der
Geländemodell-Workflows, die in der Infrastruktur- und Bauprojektplanung
verwendet werden.

### Was dieses Projekt macht

1. Erstellt ein regelmäßiges Koordinatenraster innerhalb einer gewählten
   Bounding Box
2. Fragt für jeden Punkt die Höhe über die kostenlose **Open-Elevation API**
   ab (kein API-Key nötig)
3. Verarbeitet das Höhenraster:
   - Berechnet die Hangneigung (in Grad) mit `numpy.gradient`
   - Erzeugt Höhenlinien mit `matplotlib`
4. Exportiert:
   - Höhenraster als GeoTIFF (`output/dgm.tif`)
   - Hangneigungsraster als GeoTIFF (`output/slope.tif`)
   - Höhenlinien als Shapefile (`output/hoehenlinien.shp`)

Alle Ausgaben lassen sich direkt in QGIS öffnen.

### Technologien

Python (numpy, pandas, requests, matplotlib, rasterio, geopandas)

### Einrichtung

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Trage in `config.py` die Bounding Box für dein Zielgebiet ein, dann:

```bash
python fetch_elevation.py
python process_dgm.py
```

### Hinweis zur Datenquelle

Open-Elevation ist ein kostenloser, community-betriebener Dienst und kann
gelegentlich langsam oder nicht verfügbar sein. In einem produktiven
Workflow würde man stattdessen eine echte LiDAR- oder Copernicus-DEM-Quelle
verwenden.

### Lizenz

Höhendaten über Open-Elevation (offene Daten, u. a. aus SRTM).
