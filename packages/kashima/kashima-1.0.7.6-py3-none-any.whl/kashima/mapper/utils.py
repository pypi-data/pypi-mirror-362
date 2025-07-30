# kashima/mapper/utils.py
# ---------------------------------------------------------------------
# Generic helpers used across the mapper package
# Patched 2025‑06‑18:
# • great_circle_bbox robust at high latitudes
# • stream_read_csv_bbox understands dateline wrap & new bbox ordering
# ---------------------------------------------------------------------
from __future__ import annotations
import math
from pathlib import Path
from typing import Sequence, Tuple, List, Iterable


import numpy as np
import pandas as pd
import geopandas as gpd
from pyproj import Transformer, CRS

# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------
EARTH_RADIUS_KM = 6371.0


# ---------------------------------------------------------------------
# 0.  Bounding box  (lon0, lat0 → min_lon, max_lon, min_lat, max_lat)
# ---------------------------------------------------------------------
def great_circle_bbox(
    lon0: float, lat0: float, radius_km: float
) -> Tuple[float, float, float, float]:
    """
    Return a *conservative* bounding box enclosing the circle of
    `radius_km` around (lat0, lon0).

    Output order: **(min_lon, max_lon, min_lat, max_lat)**

    Works safely up to |lat| ≈ 88° and wraps across the 180° meridian.
    """
    d_lat = radius_km / 111.0  # deg
    cos_phi = max(0.01, math.cos(math.radians(lat0)))  # avoid /0
    d_lon = radius_km / (111.320 * cos_phi)

    min_lat = max(-90.0, lat0 - d_lat)
    max_lat = min(+90.0, lat0 + d_lat)

    def _wrap(x):
        return ((x + 180.0) % 360.0) - 180.0

    min_lon = _wrap(lon0 - d_lon)
    max_lon = _wrap(lon0 + d_lon)
    return min_lon, max_lon, min_lat, max_lat


# ---------------------------------------------------------------------
# 1.  Stream‑read CSV restricted to bbox (now dateline‑aware)
# ---------------------------------------------------------------------
def stream_read_csv_bbox(
    csv_path: str | Path,
    bbox: Tuple[float, float, float, float],
    lat_col: str = "latitude",
    lon_col: str = "longitude",
    chunksize: int = 50_000,
    dtype_map: dict | None = None,
    **read_csv_kwargs,
) -> pd.DataFrame:
    """
    Read large CSV in chunks, keeping only rows that fall inside *bbox*.

    Parameters
    ----------
    bbox : (min_lon, max_lon, min_lat, max_lat)  – the exact tuple
           returned by `great_circle_bbox()`.
           Handles the dateline case where min_lon > max_lon.
    **read_csv_kwargs : any additional keyword passed to `pd.read_csv`
                        (sep, names, comment, etc.)
    """
    min_lon, max_lon, min_lat, max_lat = bbox
    dtype_map = dtype_map or {
        lat_col: "float32",
        lon_col: "float32",
        "mag": "float32",
    }

    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(csv_path)

    keep: List[pd.DataFrame] = []
    reader = pd.read_csv(
        csv_path, chunksize=chunksize, dtype=dtype_map, **read_csv_kwargs
    )

    # longitude test must cope with wrap‑around
    if min_lon <= max_lon:
        lon_test = lambda ser: ser.between(min_lon, max_lon, inclusive="both")
    else:  # bbox crosses the dateline
        lon_test = lambda ser: (ser >= min_lon) | (ser <= max_lon)

    for chunk in reader:
        m = lon_test(chunk[lon_col]) & chunk[lat_col].between(
            min_lat, max_lat, inclusive="both"
        )
        if m.any():
            keep.append(chunk.loc[m])

    if keep:
        return pd.concat(keep, ignore_index=True)
    return pd.DataFrame()  # empty, but with no rows


# ---------------------------------------------------------------------
# 2.  Misc. utilities (unchanged except for type hints)
# ---------------------------------------------------------------------
def calculate_zoom_level(radius_km: float) -> int:
    max_zoom = 18
    zoom_level = int(max_zoom - np.log2(radius_km / 500))
    return max(min(zoom_level, max_zoom), 1)


def haversine_distance(lat1, lon1, lat2, lon2):
    lat1_rad, lon1_rad = np.radians(lat1), np.radians(lon1)
    lat2_rad, lon2_rad = np.radians(lat2), np.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2) ** 2
    )
    c = 2 * np.arcsin(np.sqrt(a))
    return EARTH_RADIUS_KM * c


def calculate_distances_vectorized(
    events_df: pd.DataFrame,
    center_lat: float,
    center_lon: float,
    lat_col: str = "latitude",
    lon_col: str = "longitude",
    out_col: str = "Repi",
):
    lat1_rad = math.radians(center_lat)
    lon1_rad = math.radians(center_lon)

    lat2_rad = np.radians(events_df[lat_col].values)
    lon2_rad = np.radians(events_df[lon_col].values)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2) ** 2
    )
    c = 2 * np.arcsin(np.sqrt(a))
    events_df[out_col] = EARTH_RADIUS_KM * c


# ---------------------------------------------------------------------
# 3.  Coordinate transforms, magnitude helpers, etc.  (unchanged)
# ---------------------------------------------------------------------
def convert_xy_to_latlon(x, y, source_crs="EPSG:32722", target_crs="EPSG:4326"):
    transformer = Transformer.from_crs(
        CRS.from_user_input(source_crs), CRS.from_user_input(target_crs), always_xy=True
    )
    lon, lat = transformer.transform(x, y)
    return lon, lat


def calculate_magnitude(Q, f_TNT, a_ML, b_ML):
    Q_TNT = Q * f_TNT
    return a_ML * np.log10(Q_TNT) + b_ML


def load_faults(faults_gem_file_path, coordinate_system="EPSG:4326"):
    gdf = gpd.read_file(faults_gem_file_path)
    if coordinate_system:
        gdf = gdf.to_crs("EPSG:4326")
    return gdf


def load_stations_csv(station_file_path, station_crs="EPSG:4326"):
    stations_df = pd.read_csv(station_file_path)
    if "latitude" not in stations_df.columns or "longitude" not in stations_df.columns:
        if {"x", "y"} <= set(stations_df.columns):
            lon, lat = convert_xy_to_latlon(
                stations_df["x"].values,
                stations_df["y"].values,
                source_crs=station_crs,
                target_crs="EPSG:4326",
            )
            stations_df["latitude"] = lat
            stations_df["longitude"] = lon
        else:
            raise ValueError("Station CSV lacks latitude/longitude and x,y columns.")
    return stations_df


# ────────────────────────────────────────────────────────────────────
#  Six‑class focal‑mechanism classification (Frohlich 1992 triangle)
# ────────────────────────────────────────────────────────────────────

import numpy as np


def _fault_style_from_principal_axes(plunge_P: float, plunge_T: float) -> str:
    if plunge_P >= 55 and plunge_T < 40:
        return "Reverse"
    if plunge_T >= 55 and plunge_P < 40:
        return "Normal"
    if plunge_P < 40 and plunge_T < 40:
        return "Strike‑slip"
    if 40 <= plunge_T < 55 and plunge_P < 40:
        return "Normal–Strike‑slip"
    if 40 <= plunge_P < 55 and plunge_T < 40:
        return "Reverse–Strike‑slip"
    return "Oblique"


def classify_fault_style(
    mrr, mtt, mpp, mrt, mrp, mtp, *, source: str | None = None
) -> str:
    """
    Robust six‑class mechanism classifier.

    • Detects catalogue type:
        - if |trace| > 1 % of max(abs(M))  ⇒ treat as **USGS** (Up‑South‑East)
        - else                              ⇒ treat as **ISC/GCMT** (North‑East‑Down, trace ≈ 0)

    • Always returns one of the six labels unless tensor contains NaNs.
    """
    # ---------- 0. raw matrix in catalogue convention -----------------
    if source == "USGS" or source is None:
        # assume USGS by default, convert later if needed
        M_cat = np.array([[mrr, mrt, mrp], [mrt, mtt, mtp], [mrp, mtp, mpp]], float)
    else:  # explicit ISC
        M_cat = np.array([[mrr, mrp, mrt], [mrp, mtt, mtp], [mrt, mtp, mpp]], float)

    if not np.isfinite(M_cat).all() or np.isclose(np.linalg.norm(M_cat), 0.0):
        return "Undetermined"

    # ---------- 1. auto‑detect catalogue orientation ------------------
    trace = np.trace(M_cat)
    if abs(trace) > 0.01 * np.max(np.abs(M_cat)):  # USGS case
        # convert Up‑South‑East → North‑East‑Down
        UUU, SSS, EEE = mrr, mtt, mpp
        USE, UEE, SEE = mrt, mrp, mtp
        M = np.array([[SSS, -SEE, +USE], [-SEE, EEE, -UEE], [+USE, -UEE, UUU]], float)
    else:  # ISC / GCMT
        M = np.array([[mrr, mrp, mrt], [mrp, mtt, mtp], [mrt, mtp, mpp]], float)

    # ---------- 2. deviatoric tensor ---------------------------------
    M -= np.eye(3) * np.trace(M) / 3.0

    # ---------- 3. principal axes & plunges ---------------------------
    _, vecs = np.linalg.eigh(M)
    P, T = vecs[:, 0], vecs[:, 2]  # compression, tension
    plunge_P = abs(np.degrees(np.arcsin(P[2])))  # Down (+Z)
    plunge_T = abs(np.degrees(np.arcsin(T[2])))

    return _fault_style_from_principal_axes(plunge_P, plunge_T)
