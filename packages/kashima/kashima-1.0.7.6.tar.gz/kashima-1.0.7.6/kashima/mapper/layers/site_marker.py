# kashima/mapper/layers/site_marker.py
from __future__ import annotations
import folium


class SiteMarkerLayer:
    """
    A single red‑star marker at the site (project centre).
    """

    def __init__(self, latitude: float, longitude: float, project: str, client: str):
        self.lat = latitude
        self.lon = longitude
        self.project = project
        self.client = client

    def to_feature_group(self) -> folium.FeatureGroup:
        fg = folium.FeatureGroup(name="Site", show=True)

        popup = folium.Popup(
            f"<b>Site Project:</b> {self.project}<br>" f"<b>Client:</b> {self.client}",
            max_width=300,
        )
        folium.Marker(
            location=[self.lat, self.lon],
            icon=folium.Icon(color="red", icon="star", prefix="fa"),
            tooltip=self.project,
            popup=popup,
        ).add_to(fg)

        return fg
