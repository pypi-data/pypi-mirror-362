# kashima/mapper/layers/stations.py
from __future__ import annotations
import folium
import pandas as pd
from ._layer_base import MapLayer

_ICON = {
    1: ("blue", "arrow-up"),
    2: ("green", "arrows-h"),
    3: ("red", "cube"),
}


class StationLayer(MapLayer):
    def __init__(self, stations_df: pd.DataFrame, show=True):
        self.df = stations_df
        self.show = show

    def to_feature_group(self) -> folium.FeatureGroup:
        fg = folium.FeatureGroup(name="Stations", show=self.show)
        for _, r in self.df.iterrows():
            color, icon = _ICON.get(int(r.get("axes", 0)), ("gray", "info-sign"))
            folium.Marker(
                location=[r["latitude"], r["longitude"]],
                icon=folium.Icon(color=color, icon=icon, prefix="fa"),
                tooltip=f"Station {r.get('ID','?')}",
            ).add_to(fg)
        return fg
