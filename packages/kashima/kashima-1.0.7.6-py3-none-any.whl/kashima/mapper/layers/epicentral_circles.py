# kashima/mapper/layers/epicentral_circles.py
from __future__ import annotations
import folium
import math
from ._layer_base import MapLayer


class EpicentralCirclesLayer(MapLayer):
    def __init__(self, lat, lon, radius_km, n_circles=3, show=True):
        self.lat = lat
        self.lon = lon
        self.radius = radius_km
        self.n = max(1, n_circles)
        self.show = show

    def to_feature_group(self) -> folium.FeatureGroup:
        fg = folium.FeatureGroup(name="Epicentral circles", show=self.show)
        step = self.radius / self.n
        for i in range(1, self.n + 1):
            folium.Circle(
                location=[self.lat, self.lon],
                radius=i * step * 1000,
                color="blue",
                weight=1,
                opacity=0.5,
                fill=False,
                tooltip=f"{i*step:.0f} km",
            ).add_to(fg)
        return fg
