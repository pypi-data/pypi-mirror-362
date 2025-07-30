# kashima/mapper/layers/event_markers.py   • 2025‑06‑26  (adds Repi line)
from __future__ import annotations
import html
import numpy as np
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from ._layer_base import MapLayer


class EventMarkerLayer(MapLayer):
    """
    Coloured circle markers for each event, with formatted pop‑ups.
    """

    def __init__(
        self,
        events_df: pd.DataFrame,
        *,
        mag_col: str = "mag",
        color_map,
        legend_map: dict[str, str],
        tooltip_fields: list[str] | None = None,
        clustered: bool = False,
        show: bool = True,
    ):
        self.df = events_df
        self.mag_col = mag_col
        self.color_map = color_map
        self.legend = legend_map
        self.tooltip_fields = tooltip_fields or ["place"]
        self.clustered = clustered
        self.show = show

    # ------------------------------------------------------------------
    @staticmethod
    def _fmt(val):
        """Pretty print floats & timestamps."""
        if isinstance(val, (float, np.floating)):
            if val == 0 or (1e-3 < abs(val) < 1e4):
                return f"{val:.3f}"
            return f"{val:.2e}"
        if isinstance(val, pd.Timestamp):
            return val.strftime("%Y-%m-%d %H:%M:%S")
        return str(val)

    # ------------------------------------------------------------------
    def to_feature_group(self):
        fg = (
            MarkerCluster(name="Events", show=self.show)
            if self.clustered
            else folium.FeatureGroup(name="Events", show=self.show)
        )

        esc = lambda s: s.replace("\\", "\\\\").replace("`", "\\`").replace("\n", "\\n")

        for _, row in self.df.iterrows():
            colour = self.color_map(row[self.mag_col]) if self.color_map else "blue"

            # ── tooltip ────────────────────────────────────────────────
            tt = " | ".join(
                esc(str(row.get(f, ""))).strip()
                for f in self.tooltip_fields
                if pd.notnull(row.get(f, ""))
            )

            # ── popup lines ────────────────────────────────────────────
            lines: list[str] = []

            # 1) iterate over legend.csv fields
            for col, label in self.legend.items():
                if col in row and pd.notnull(row[col]):
                    lines.append(
                        f"<b>{html.escape(label)}:</b> "
                        f"{html.escape(self._fmt(row[col]))}"
                    )

            # 2) Epicentral distance (always shown if present)
            if "Repi" in row and np.isfinite(row["Repi"]):
                lines.append(f"<b>Epicentral Distance:</b> {row['Repi']:.1f}&nbsp;km")

            popup = folium.Popup("<br>".join(lines), max_width=300)

            # ── marker ────────────────────────────────────────────────
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=4,
                color=colour,
                fill=True,
                fill_opacity=0.7,
                tooltip=tt or None,
                popup=popup,
            ).add_to(fg)

        return fg
