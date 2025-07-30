# kashima/mapper/layers/_layer_base.py
from __future__ import annotations
import abc
import folium


class MapLayer(abc.ABC):
    """Abstract base class for all map layers."""

    @abc.abstractmethod
    def to_feature_group(self) -> folium.FeatureGroup:
        """Return a Folium FeatureGroup ready to be added to a map."""
        raise NotImplementedError
