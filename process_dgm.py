"""
process_dgm.py
----------------
Verarbeitet das Höhenraster aus fetch_elevation.py zu einem einfachen
digitalen Geländemodell (DGM):

  1. Baut ein reguläres Höhenraster (2D-Array) aus den CSV-Punkten
  2. Berechnet die Hangneigung (Slope) mittels numpy.gradient
  3. Erzeugt Höhenlinien (Contours) mit matplotlib
  4. Exportiert:
       - Höhenraster als GeoTIFF (output/dgm.tif)
       - Hangneigung als GeoTIFF (output/slope.tif)
       - Höhenlinien als Shapefile (output/hoehenlinien.shp)

Aufruf:
    python process_dgm.py
"""

import os
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")  # kein interaktives Fenster nötig
import matplotlib.pyplot as plt
import rasterio
from rasterio.transform import from_bounds
import geopandas as gpd
from shapely.geometry import LineString

from config import BOUNDING_BOX, GRID_RESOLUTION, OUTPUT_DIR


def load_grid():
    df = pd.read_csv(f"{OUTPUT_DIR}/elevation_grid.csv")
    n = GRID_RESOLUTION
    elevation = df["elevation"].to_numpy().reshape(n, n)
    return elevation


def export_geotiff(array, bbox, path):
    min_lon, min_lat, max_lon, max_lat = bbox
    transform = from_bounds(min_lon, min_lat, max_lon, max_lat, array.shape[1], array.shape[0])
    with rasterio.open(
        path, "w", driver="GTiff", height=array.shape[0], width=array.shape[1],
        count=1, dtype=array.dtype, crs="EPSG:4326", transform=transform,
    ) as dst:
        dst.write(array, 1)
    print(f"  -> GeoTIFF gespeichert: {path}")


def compute_slope(elevation, bbox):
    min_lon, min_lat, max_lon, max_lat = bbox
    # ungefähre Zellgröße in Metern (grobe Näherung über Breitengrad)
    cellsize_deg_lat = (max_lat - min_lat) / elevation.shape[0]
    cellsize_m = cellsize_deg_lat * 111_000
    dy, dx = np.gradient(elevation, cellsize_m)
    slope_rad = np.arctan(np.sqrt(dx**2 + dy**2))
    slope_deg = np.degrees(slope_rad)
    return slope_deg


def export_contours(elevation, bbox, path, levels=10):
    min_lon, min_lat, max_lon, max_lat = bbox
    n_rows, n_cols = elevation.shape
    lons = np.linspace(min_lon, max_lon, n_cols)
    lats = np.linspace(min_lat, max_lat, n_rows)

    fig, ax = plt.subplots()
    cs = ax.contour(lons, lats, elevation, levels=levels)
    plt.close(fig)

    lines = []
    heights = []
    for level, segs in zip(cs.levels, cs.allsegs):
        for seg in segs:
            if len(seg) >= 2:
                lines.append(LineString(seg))
                heights.append(level)

    if lines:
        gdf = gpd.GeoDataFrame({"hoehe_m": heights, "geometry": lines}, crs="EPSG:4326")
        gdf.to_file(path)
        print(f"  -> {len(lines)} Höhenlinien gespeichert: {path}")
    else:
        print("  -> Keine Höhenlinien erzeugt (Gebiet zu flach oder zu wenige Punkte).")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("[1/3] Lade Höhenraster ...")
    elevation = load_grid()
    print(f"  -> Raster geladen: {elevation.shape}, Höhe min={elevation.min():.1f}m max={elevation.max():.1f}m")

    print("\n[2/3] Berechne Hangneigung ...")
    slope = compute_slope(elevation, BOUNDING_BOX)
    print(f"  -> Hangneigung berechnet: min={slope.min():.1f}°, max={slope.max():.1f}°, mittel={slope.mean():.1f}°")

    print("\n[3/3] Erzeuge Höhenlinien und exportiere Ergebnisse ...")
    export_geotiff(elevation.astype("float32"), BOUNDING_BOX, f"{OUTPUT_DIR}/dgm.tif")
    export_geotiff(slope.astype("float32"), BOUNDING_BOX, f"{OUTPUT_DIR}/slope.tif")
    export_contours(elevation, BOUNDING_BOX, f"{OUTPUT_DIR}/hoehenlinien.shp")

    print("\nFertig. Öffne dgm.tif, slope.tif und hoehenlinien.shp in QGIS.")


if __name__ == "__main__":
    main()
