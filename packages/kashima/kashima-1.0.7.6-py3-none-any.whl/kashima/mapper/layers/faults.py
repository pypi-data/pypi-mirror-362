# kashima/mapper/layers/faults.py
from __future__ import annotations
import geopandas as gpd
import folium
from ._layer_base import MapLayer


class FaultLayer(MapLayer):
    def __init__(self, gdf: gpd.GeoDataFrame, color="#ff8800", weight=2, show=True):
        self.gdf = gdf
        self.color = color
        self.weight = weight
        self.show = show

    def to_feature_group(self) -> folium.FeatureGroup:
        style = {"color": self.color, "weight": self.weight, "opacity": 1.0}
        fg = folium.FeatureGroup(name="Faults", show=self.show)
        folium.GeoJson(data=self.gdf, style_function=lambda _: style).add_to(fg)
        return fg
