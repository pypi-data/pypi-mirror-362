"""
USGS FDSN event‑service wrapper
==============================

• `bbox` convenience argument removed.
• `want_tensor=True` downloads the six moment‑tensor components.
• Robust against
  – empty chunks (never drops `event_id`),
  – missing geometry/depth values (returns NaN instead of crashing).
"""

from __future__ import annotations

import json
import logging
import random
import time
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
import requests

from .utils import stream_read_csv_bbox

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# ──────────────────────────────────────────────────────────────────────
#  Local CSV helper
# ──────────────────────────────────────────────────────────────────────
def load_usgs_csv(
    csv_path: str | Path,
    bbox: Tuple[float, float, float, float] | None = None,
) -> pd.DataFrame:
    usecols = [
        "time",
        "latitude",
        "longitude",
        "depth",
        "mag",
        "magType",
        "place",
        "id",
    ]
    dtypes = {
        "latitude": "float64",
        "longitude": "float64",
        "depth": "float32",
        "mag": "float32",
        "magType": "category",
        "place": "string",
        "id": "string",
    }

    df = stream_read_csv_bbox(
        csv_path,
        bbox=bbox,
        lat_col="latitude",
        lon_col="longitude",
        chunksize=50_000,
        dtype_map=dtypes,
        usecols=usecols,
        parse_dates=["time"],
    )

    df = df.rename(columns={"magType": "mag_type", "id": "event_id"}).assign(
        source="USGS",
        mrr=np.nan,
        mtt=np.nan,
        mpp=np.nan,
        mrt=np.nan,
        mrp=np.nan,
        mtp=np.nan,
    )
    return df.reindex(
        columns=[
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
    )


__all__ = ["load_usgs_csv"]


# ──────────────────────────────────────────────────────────────────────
#  Online catalogue wrapper
# ──────────────────────────────────────────────────────────────────────
class USGSCatalog:
    """Fetch earthquake events from the USGS FDSN web service."""

    SCHEMA = [
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

    def __init__(
        self,
        min_magnitude: float = 4.5,
        verbose: bool = True,
        url: str = "https://earthquake.usgs.gov/fdsnws/event/1/query",
        timeout: int = 30,
    ):
        self.min_magnitude = min_magnitude
        self.verbose = verbose
        self.url = url
        self.timeout = timeout
        self.dataframe: pd.DataFrame | None = None

    # ------------------------------------------------------------------
    def get_events(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        *,
        min_latitude: float | None = None,
        max_latitude: float | None = None,
        min_longitude: float | None = None,
        max_longitude: float | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        maxradiuskm: float | None = None,
        min_depth: float | None = None,
        max_depth: float | None = None,
        min_magnitude: float | None = None,
        max_magnitude: float | None = None,
        magnitude_type: str | None = None,
        event_type: str | None = None,
        want_tensor: bool = False,
        **extra: Any,
    ) -> pd.DataFrame:
        if start_date is None:
            start_date = datetime(1800, 1, 1)
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date >= end_date:
            raise ValueError("start_date must be before end_date")

        max_events = 20_000
        delta_days = 700
        current_date = start_date
        frames: List[pd.DataFrame] = []

        logger.setLevel(logging.INFO if self.verbose else logging.WARNING)
        if self.verbose:
            logger.info("Starting USGS download …")

        while current_date < end_date:
            interval_end = min(current_date + timedelta(days=delta_days), end_date)
            frame = self._fetch_chunk(
                current_date,
                interval_end,
                max_events,
                want_tensor=want_tensor,
                min_latitude=min_latitude,
                max_latitude=max_latitude,
                min_longitude=min_longitude,
                max_longitude=max_longitude,
                latitude=latitude,
                longitude=longitude,
                maxradiuskm=maxradiuskm,
                min_depth=min_depth,
                max_depth=max_depth,
                min_magnitude=min_magnitude,
                max_magnitude=max_magnitude,
                magnitude_type=magnitude_type,
                event_type=event_type,
                **extra,
            )

            if len(frame) >= max_events:
                delta_days = max(1, delta_days // 2)
                continue

            if not frame.empty:
                frames.append(frame)

            if len(frame) < max_events / 2 and delta_days < 700:
                delta_days = min(700, delta_days * 2)
            current_date = interval_end

        if not frames:
            logger.warning("No data retrieved.")
            self.dataframe = pd.DataFrame(columns=self.SCHEMA)
            return self.dataframe

        common = set.intersection(*(set(f.columns) for f in frames))
        self.dataframe = (
            pd.concat(frames, ignore_index=True)[list(common)]
            .drop_duplicates(subset="event_id")
            .reset_index(drop=True)
        )
        return self.dataframe

    # ------------------------------------------------------------------
    def _fetch_chunk(
        self,
        start: datetime,
        end: datetime,
        limit: int,
        *,
        want_tensor: bool,
        min_latitude,
        max_latitude,
        min_longitude,
        max_longitude,
        latitude,
        longitude,
        maxradiuskm,
        min_depth,
        max_depth,
        min_magnitude,
        max_magnitude,
        magnitude_type,
        event_type,
        **extra: Any,
    ) -> pd.DataFrame:
        fmt = "geojson" if want_tensor else "csv"
        q: Dict[str, Any] = {
            "format": fmt,
            "orderby": "time-asc",
            "limit": limit,
            "starttime": start.strftime("%Y-%m-%d"),
            "endtime": end.strftime("%Y-%m-%d"),
            "minmagnitude": (
                min_magnitude if min_magnitude is not None else self.min_magnitude
            ),
        }
        if max_magnitude is not None:
            q["maxmagnitude"] = max_magnitude
        if min_depth is not None:
            q["mindepth"] = min_depth
        if max_depth is not None:
            q["maxdepth"] = max_depth
        if min_latitude is not None:
            q["minlatitude"] = min_latitude
        if max_latitude is not None:
            q["maxlatitude"] = max_latitude
        if min_longitude is not None:
            q["minlongitude"] = min_longitude
        if max_longitude is not None:
            q["maxlongitude"] = max_longitude
        if latitude is not None and longitude is not None and maxradiuskm is not None:
            q.update(
                {
                    "latitude": latitude,
                    "longitude": longitude,
                    "maxradiuskm": maxradiuskm,
                }
            )
        if magnitude_type is not None:
            q["magnitudetype"] = magnitude_type
        if event_type is not None:
            q["eventtype"] = event_type
        q.update(extra)

        retries = 0
        while retries < 5:
            try:
                if self.verbose:
                    logger.info(
                        f"USGS {q['starttime']} → {q['endtime']} "
                        f"({fmt}, try {retries + 1})"
                    )
                resp = requests.get(self.url, params=q, timeout=self.timeout)
                resp.raise_for_status()
                return (
                    self._parse_geojson(resp.json())
                    if fmt == "geojson"
                    else self._parse_csv(resp.text)
                )
            except requests.exceptions.HTTPError as e:
                wait = (
                    int(e.response.headers.get("Retry-After", 60))
                    if e.response.status_code == 429
                    else random.uniform(1, 3) * (2**retries)
                )
                logger.warning(f"{e} – retrying in {wait:.1f}s")
            except (
                requests.exceptions.RequestException,
                pd.errors.EmptyDataError,
                json.JSONDecodeError,
            ) as e:
                wait = random.uniform(1, 3) * (2**retries)
                logger.warning(f"{e} – retrying in {wait:.1f}s")
            time.sleep(wait)
            retries += 1

        logger.error("Max retries reached – returning empty frame")
        return pd.DataFrame(columns=self.SCHEMA)

    # ------------------------------------------------------------------
    @classmethod
    def _parse_csv(cls, text: str) -> pd.DataFrame:
        df = pd.read_csv(StringIO(text), parse_dates=["time"])
        df = df.rename(columns={"magType": "mag_type", "id": "event_id"}).assign(
            source="USGS",
            mrr=np.nan,
            mtt=np.nan,
            mpp=np.nan,
            mrt=np.nan,
            mrp=np.nan,
            mtp=np.nan,
        )
        return df.reindex(columns=cls.SCHEMA)

    # ------------------------------------------------------------------
    @classmethod
    def _parse_geojson(cls, js: Dict[str, Any]) -> pd.DataFrame:
        feats = js.get("features", [])
        rows: List[Dict[str, Any]] = []

        for feat in feats:
            coords = feat.get("geometry", {}).get("coordinates", [None, None, None])
            # Ensure length 3
            if len(coords) < 3:
                coords = coords + [None] * (3 - len(coords))

            lon = float(coords[0]) if coords[0] is not None else np.nan
            lat = float(coords[1]) if coords[1] is not None else np.nan
            dep = float(coords[2]) if coords[2] is not None else np.nan

            p = feat.get("properties", {})
            row = dict(
                time=(
                    pd.to_datetime(p.get("time"), unit="ms", utc=True)
                    if p.get("time") is not None
                    else pd.NaT
                ),
                latitude=lat,
                longitude=lon,
                depth=dep,
                mag=p.get("mag"),
                mag_type=p.get("magType"),
                place=p.get("place"),
                event_id=feat.get("id"),
                source="USGS",
                mrr=np.nan,
                mtt=np.nan,
                mpp=np.nan,
                mrt=np.nan,
                mrp=np.nan,
                mtp=np.nan,
            )

            tensors = p.get("products", {}).get("moment-tensor", [])
            if tensors:
                props = tensors[0]["properties"]
                for k in ("mrr", "mtt", "mpp", "mrt", "mrp", "mtp"):
                    v = props.get(f"tensor-{k}")
                    if v not in (None, ""):
                        row[k] = float(v)

            rows.append(row)

        return pd.DataFrame.from_records(rows, columns=cls.SCHEMA)
