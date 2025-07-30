"""
ISC‑GEM (v 11.0) catalogue loader
================================

Produces a dataframe that matches the unified EventMap schema *plus*
the six moment‑tensor components that exist in the raw CSV.

Unified schema
--------------
time | latitude | longitude | depth | mag | mag_type | place | event_id |
source | mrr | mtt | mpp | mrt | mrp | mtp
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd

from .utils import stream_read_csv_bbox

# ---------------------------------------------------------------------
# Fixed column list for the raw v11.0 CSV (do not change order)
# ---------------------------------------------------------------------
COLS = [
    "time_str",
    "latitude",
    "longitude",
    "smajax",
    "sminax",
    "strike",
    "epi_q",
    "depth_km",
    "depth_unc",
    "depth_q",
    "mw",
    "mw_unc",
    "mw_q",
    "mw_src",
    "moment",
    "moment_fac",
    "mo_auth",
    "mpp",
    "mpr",
    "mrr",
    "mrt",
    "mtp",
    "mtt",
    "str1",
    "dip1",
    "rake1",
    "str2",
    "dip2",
    "rake2",
    "mech_type",
    "eventid",
]


# ---------------------------------------------------------------------
# Public helper
# ---------------------------------------------------------------------
def load_isc(
    path: str | Path,
    bbox: Tuple[float, float, float, float] | None = None,
) -> pd.DataFrame:
    """
    Parameters
    ----------
    path
        Path to the ISC‑GEM main catalogue CSV.
    bbox
        Optional (min_lon, max_lon, min_lat, max_lat) bounding box
        for pre‑filtering while streaming.

    Returns
    -------
    pd.DataFrame
        Columns
        -------
        time, latitude, longitude, depth, mag, mag_type, place,
        event_id, source, mrr, mtt, mpp, mrt, mrp, mtp
    """
    usecols = [
        "time_str",
        "latitude",
        "longitude",
        "depth_km",
        "mw",
        "eventid",
        # moment tensor
        "mrr",
        "mtt",
        "mpp",
        "mrt",
        "mpr",
        "mtp",
    ]
    dtypes = {
        "latitude": "float64",
        "longitude": "float64",
        "depth_km": "float32",
        "mw": "float32",
        "eventid": "string",
        "mrr": "float64",
        "mtt": "float64",
        "mpp": "float64",
        "mrt": "float64",
        "mpr": "float64",
        "mtp": "float64",
    }

    df = stream_read_csv_bbox(
        path,
        bbox=bbox,
        lat_col="latitude",
        lon_col="longitude",
        chunksize=50_000,
        dtype_map=dtypes,
        sep=r"\s*,\s*",
        engine="python",
        comment="#",
        names=COLS,
        usecols=usecols,
        parse_dates={"time": ["time_str"]},
        keep_date_col=False,
    )

    # Harmonise with USGS schema and append tensor columns untouched
    df = df.rename(
        columns={
            "depth_km": "depth",
            "mw": "mag",
            "eventid": "event_id",
            "mpr": "mrp",  # keep consistent order
        }
    ).assign(
        mag_type="Mw",
        place=pd.NA,
        source="ISC-GEM",
    )[
        [
            "time",
            "latitude",
            "longitude",
            "depth",
            "mag",
            "mag_type",
            "place",
            "event_id",
            "source",
            "mrr",
            "mtt",
            "mpp",
            "mrt",
            "mrp",
            "mtp",
        ]
    ]

    return df
