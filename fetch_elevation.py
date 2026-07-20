"""
fetch_elevation.py
-------------------
Erzeugt ein regelmäßiges Punktraster innerhalb der in config.py definierten
Bounding Box und fragt für jeden Punkt die Höhe über der kostenlosen
Open-Elevation API ab (keine Anmeldung/API-Key nötig).

Speichert das Ergebnis als CSV (output/elevation_grid.csv), das von
process_dgm.py weiterverarbeitet wird.

Aufruf:
    python fetch_elevation.py
"""

import os
import time
import numpy as np
import pandas as pd
import requests

from config import BOUNDING_BOX, GRID_RESOLUTION, OUTPUT_DIR

API_URL = "https://api.open-elevation.com/api/v1/lookup"
BATCH_SIZE = 100


def build_grid(bbox, resolution):
    min_lon, min_lat, max_lon, max_lat = bbox
    lons = np.linspace(min_lon, max_lon, resolution)
    lats = np.linspace(min_lat, max_lat, resolution)
    grid_lon, grid_lat = np.meshgrid(lons, lats)
    points = list(zip(grid_lat.flatten(), grid_lon.flatten()))
    return points, grid_lon, grid_lat


def fetch_elevations(points):
    results = []
    total = len(points)
    for i in range(0, total, BATCH_SIZE):
        batch = points[i : i + BATCH_SIZE]
        locations = [{"latitude": lat, "longitude": lon} for lat, lon in batch]
        print(f"  Abfrage Punkte {i + 1}-{min(i + BATCH_SIZE, total)} von {total} ...")
        try:
            resp = requests.post(API_URL, json={"locations": locations}, timeout=30)
            resp.raise_for_status()
            data = resp.json()["results"]
            for d in data:
                results.append({"latitude": d["latitude"], "longitude": d["longitude"], "elevation": d["elevation"]})
        except requests.exceptions.RequestException as e:
            print(f"  Fehler bei Batch {i}: {e}. Versuche erneut in 5 Sekunden ...")
            time.sleep(5)
            resp = requests.post(API_URL, json={"locations": locations}, timeout=30)
            resp.raise_for_status()
            data = resp.json()["results"]
            for d in data:
                results.append({"latitude": d["latitude"], "longitude": d["longitude"], "elevation": d["elevation"]})
        time.sleep(1)  # freundlich zur kostenlosen API
    return results


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    points, grid_lon, grid_lat = build_grid(BOUNDING_BOX, GRID_RESOLUTION)
    print(f"Rasterpunkte erzeugt: {len(points)} ({GRID_RESOLUTION}x{GRID_RESOLUTION})")

    results = fetch_elevations(points)
    df = pd.DataFrame(results)
    df.to_csv(f"{OUTPUT_DIR}/elevation_grid.csv", index=False)

    print(f"\n{len(df)} Höhenpunkte gespeichert in '{OUTPUT_DIR}/elevation_grid.csv'.")
    print("Weiter mit: python process_dgm.py")
