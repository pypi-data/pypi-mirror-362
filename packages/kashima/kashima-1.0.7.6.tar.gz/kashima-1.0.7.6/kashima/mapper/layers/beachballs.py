# kashima/mapper/layers/beachballs.py   •  2025‑06‑26  magnitude‑scaled
from __future__ import annotations
import base64
import io
import logging
from itertools import count
from typing import Dict

import numpy as np
import pandas as pd
import folium
from folium.features import CustomIcon

import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from obspy.imaging.beachball import beach

logger = logging.getLogger(__name__)


class BeachballLayer:
    """
    Focal‑mechanism markers scaled by magnitude.

    Size rule mirrors EventMarkerLayer:
        size_px = base + scaling_factor * (Mw – vmin)
    """

    _CACHE: Dict[str, str] = {}
    _warned = count()

    def __init__(
        self,
        df: pd.DataFrame,
        *,
        show: bool = True,
        legend_map: dict[str, str] | None = None,
        vmin: float | None = None,
        scaling_factor: float = 2.0,
        base_size: int = 12,
    ):
        cols = ["mrr", "mtt", "mpp", "mrt", "mrp", "mtp"]
        self.df = df.dropna(subset=cols).copy()
        self.show = show
        self.vmin = vmin if vmin is not None else self.df["mag"].min()
        self.scaling = scaling_factor
        self.base = base_size
        self.legend_map = legend_map or {}

    # ------------------------------------------------------------------
    def _size_pixels(self, mag: float | None) -> int:
        if mag is None or not np.isfinite(mag):
            return self.base
        return int(self.base + self.scaling * max(0.0, mag - self.vmin))

    # ------------------------------------------------------------------
    def _render_icon(self, r) -> str | None:
        eid = r["event_id"]
        if eid in self._CACHE:
            return self._CACHE[eid]

        mt = [r.mrr, r.mtt, r.mpp, r.mrt, r.mrp, r.mtp]
        size_px = self._size_pixels(r.mag)

        try:
            fig_or_patch = beach(
                mt, size=size_px, linewidth=0.6, facecolor="k", edgecolor="k"
            )
            # accommodate ObsPy versions
            if isinstance(fig_or_patch, PatchCollection):
                fig = plt.figure(figsize=(size_px / 72, size_px / 72), dpi=72)
                ax = fig.add_axes([0, 0, 1, 1])
                ax.set_axis_off()
                ax.add_collection(fig_or_patch)
                ax.set_aspect("equal")
                ax.autoscale_view()
            else:
                fig = fig_or_patch

            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=72, transparent=True)
            plt.close(fig)

        except Exception as e:
            if next(self._warned) < 10:
                logger.warning("Skip beachball for %s: %s", eid, e)
            return None

        uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
        self._CACHE[eid] = uri
        return uri

    # ------------------------------------------------------------------
    def _make_popup(self, r) -> folium.Popup:
        lg = self.legend_map
        lines = [
            f"<b>{lg.get('mag','Magnitude')}:</b> {r.mag:.2f}",
            f"<b>{lg.get('fault_style','Fault Style')}:</b> {r.fault_style}",
            f"<b>{lg.get('latitude','Latitude')}:</b> {r.latitude:.4f}",
            f"<b>{lg.get('longitude','Longitude')}:</b> {r.longitude:.4f}",
        ]
        for field, label in lg.items():
            if field in ("mag", "fault_style", "latitude", "longitude"):
                continue
            val = r.get(field)
            if pd.notnull(val):
                lines.append(f"<b>{label}:</b> {val}")
        return folium.Popup("<br>".join(lines), max_width=300)

    # ------------------------------------------------------------------
    def to_feature_group(self) -> folium.FeatureGroup:
        fg = folium.FeatureGroup(name="Beachballs", show=self.show)
        added = 0

        for _, r in self.df.iterrows():
            uri = self._render_icon(r)
            if uri is None:
                continue
            size_px = self._size_pixels(r.mag)
            icon = CustomIcon(
                uri,
                icon_size=(size_px, size_px),
                icon_anchor=(size_px // 2, size_px // 2),
            )

            folium.Marker(
                location=[r.latitude, r.longitude],
                icon=icon,
                tooltip=f"Mw {r.mag:.1f}" if np.isfinite(r.mag) else None,
                popup=self._make_popup(r),
            ).add_to(fg)
            added += 1

        logger.info("Beachball layer: %d icons drawn.", added)
        return fg
