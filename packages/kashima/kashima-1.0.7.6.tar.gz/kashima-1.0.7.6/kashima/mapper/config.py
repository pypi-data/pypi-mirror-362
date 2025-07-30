# file: config.py

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

EARTH_RADIUS_KM = 6371.0  # Earth's radius in kilometers

# ----------------------------------------------------------------
# Extended TILE_LAYERS dict to include OpenStreetMap, Stamen, etc.
# ----------------------------------------------------------------
TILE_LAYERS = {
    "ESRI_SATELLITE": "Esri.WorldImagery",
    "OPEN_TOPO": "OpenTopoMap",
    "ESRI_NATGEO": "Esri.NatGeoWorldMap",
    "CYCL_OSM": "CyclOSM",
    "CARTO_POSITRON": "CartoDB positron",
    "CARTO_DARK": "CartoDB dark_matter",
    "ESRI_STREETS": "Esri.WorldStreetMap",
    "ESRI_TERRAIN": "Esri.WorldTerrain",
    "ESRI_RELIEF": "Esri.WorldShadedRelief",
    # Newly added recognized strings by Folium:
    "OPENSTREETMAP": "OpenStreetMap",
    "STAMEN_TERRAIN": "Stamen Terrain",
    "STAMEN_TONER": "Stamen Toner",
    "CARTO_VOYAGER": "CartoDB voyager",
}

# ----------------------------------------------------------------
# Each key -> a dict with 'tiles' (the actual Folium identifier or URL)
# and 'attr' for attribution
# ----------------------------------------------------------------
TILE_LAYER_CONFIGS = {
    TILE_LAYERS["ESRI_SATELLITE"]: {
        "tiles": "Esri.WorldImagery",
        "attr": "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, etc.",
    },
    TILE_LAYERS["OPEN_TOPO"]: {
        "tiles": "OpenTopoMap",
        "attr": "Map data: © OpenStreetMap contributors, SRTM | Map style: © OpenTopoMap",
    },
    TILE_LAYERS["ESRI_NATGEO"]: {
        "tiles": "Esri.NatGeoWorldMap",
        "attr": "Tiles &copy; Esri &mdash; National Geographic, Esri, DeLorme, NAVTEQ, etc.",
    },
    TILE_LAYERS["CYCL_OSM"]: {
        "tiles": "CyclOSM",
        "attr": '<a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases">CyclOSM</a>',
    },
    TILE_LAYERS["CARTO_POSITRON"]: {
        "tiles": "CartoDB positron",
        "attr": "© CartoDB © OpenStreetMap contributors",
    },
    TILE_LAYERS["CARTO_DARK"]: {
        "tiles": "CartoDB dark_matter",
        "attr": "© CartoDB © OpenStreetMap contributors",
    },
    TILE_LAYERS["ESRI_STREETS"]: {
        "tiles": "Esri.WorldStreetMap",
        "attr": "Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, etc.",
    },
    TILE_LAYERS["ESRI_TERRAIN"]: {
        "tiles": "Esri.WorldTerrain",
        "attr": "Tiles &copy; Esri &mdash; Source: USGS, Esri, TANA, DeLorme, etc.",
    },
    TILE_LAYERS["ESRI_RELIEF"]: {
        "tiles": "Esri.WorldShadedRelief",
        "attr": "Tiles &copy; Esri &mdash; Source: Esri",
    },
    # New layers
    TILE_LAYERS["OPENSTREETMAP"]: {
        "tiles": "OpenStreetMap",
        "attr": "© OpenStreetMap contributors",
    },
    TILE_LAYERS["STAMEN_TERRAIN"]: {
        "tiles": "Stamen Terrain",
        "attr": "Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap contributors",
    },
    TILE_LAYERS["STAMEN_TONER"]: {
        "tiles": "Stamen Toner",
        "attr": "Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap contributors",
    },
    # Additional tile config
    TILE_LAYERS["CARTO_VOYAGER"]: {
        "tiles": "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png",
        "attr": "Map tiles by CartoDB, under CC BY 3.0. Data by OSM.",
    },
}


# kashima/mapper/config.py
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class MapConfig:
    project_name: str
    client: str
    latitude: float
    longitude: float
    radius_km: float

    # map controls
    base_zoom_level: int = 8
    min_zoom_level: int = 4
    max_zoom_level: int = 18
    default_tile_layer: str = "OpenStreetMap"

    # epicentral circles
    epicentral_circles_title: str = "Epicentral Distance"
    epicentral_circles: int = 5
    MIN_EPICENTRAL_CIRCLES: int = 3
    MAX_EPICENTRAL_CIRCLES: int = 25

    # NEW – let the caller decide whether to auto‑fit after drawing
    auto_fit_bounds: bool = True
    lock_pan: bool = False  # freeze panning when True


@dataclass
class EventConfig:
    """
    Visual & filtering parameters for EventMap layers.
    New in v2025‑06‑18:
        • show_events_default
        • show_heatmap_default
        • show_cluster_default
        • show_epicentral_circles_default
    """

    # ── colours / sizes ───────────────────────────────────────────────
    color_palette: str = "magma"
    color_reversed: bool = False
    scaling_factor: float = 2.0
    legend_position: str = "bottomright"
    legend_title: str = "Magnitude (Mw)"

    # ── heat‑map tuning ──────────────────────────────────────────────
    heatmap_radius: int = 20
    heatmap_blur: int = 15
    heatmap_min_opacity: float = 0.5

    # ── distance / magnitude filters ─────────────────────────────────
    event_radius_multiplier: float = 1.0
    vmin: Optional[float] = None
    vmax: Optional[float] = None

    # ── NEW: default layer visibility flags ──────────────────────────
    show_events_default: bool = True  # markers visible on load
    show_heatmap_default: bool = False  # heat‑map hidden on load
    show_cluster_default: bool = False  # marker‑cluster hidden
    show_epicentral_circles_default: bool = False  # rings hidden
    show_beachballs_default: bool = False
    beachball_min_magnitude: float | None = None


@dataclass
class FaultConfig:
    include_faults: bool = False
    faults_gem_file_path: str = ""
    regional_faults_color: str = "darkblue"
    regional_faults_weight: int = 3
    coordinate_system: str = "EPSG:4326"


@dataclass
class StationConfig:
    station_file_path: str = ""
    coordinate_system: str = "EPSG:4326"
    layer_title: str = "Seismic Stations"


@dataclass
class BlastConfig:
    blast_file_path: str = ""
    coordinate_system: str = "EPSG:32722"
    f_TNT: float = 0.90
    a_ML: float = 0.75
    b_ML: float = -1.0


__version__ = "1.0.1.7"
