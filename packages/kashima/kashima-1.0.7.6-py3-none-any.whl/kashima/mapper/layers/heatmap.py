# kashima/mapper/layers/heatmap.py
from __future__ import annotations
import pandas as pd
import folium
from folium import plugins
from ._layer_base import MapLayer


class HeatmapLayer(MapLayer):
    """Magnitude‑weighted heatmap."""

    def __init__(
        self,
        events_df: pd.DataFrame,
        *,
        mag_col: str = "mag",
        radius: int = 15,
        blur: int = 10,
        min_opacity: float = 0.2,
        show: bool = False,
    ):
        self.df = events_df
        self.mag_col = mag_col
        self.radius = radius
        self.blur = blur
        self.min_opacity = min_opacity
        self.show = show

    def to_feature_group(self) -> folium.FeatureGroup:
        fg = folium.FeatureGroup(name="Heatmap", show=self.show)
        data = [
            (r["latitude"], r["longitude"], r[self.mag_col])
            for _, r in self.df.iterrows()
        ]
        heat = plugins.HeatMap(
            data,
            radius=self.radius,
            blur=self.blur,
            min_opacity=self.min_opacity,
            max_zoom=8,
        )
        fg.add_child(heat)
        return fg
