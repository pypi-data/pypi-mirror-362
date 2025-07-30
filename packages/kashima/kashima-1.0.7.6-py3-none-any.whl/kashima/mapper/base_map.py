import folium
import logging
import math
from .config import (
    MapConfig,
    EventConfig,
    FaultConfig,
    StationConfig,
    TILE_LAYER_CONFIGS,
)
from .utils import EARTH_RADIUS_KM
from pyproj import Transformer
from folium import plugins

logger = logging.getLogger(__name__)


class BaseMap:
    def __init__(
        self,
        map_config: MapConfig,
        event_config: EventConfig = None,
        fault_config: FaultConfig = None,
        station_config: StationConfig = None,
        log_level: int = logging.INFO,
    ):
        """
        Initialize the BaseMap object.

        Parameters:
            map_config (MapConfig): Configuration for the map.
            event_config (EventConfig, optional): Configuration for seismic events.
            fault_config (FaultConfig, optional): Configuration for fault lines.
            station_config (StationConfig, optional): Configuration for seismic stations.
            log_level (int, optional): Logging level. Defaults to logging.INFO.
        """
        logger.setLevel(log_level)
        # Validate that map_config is provided and is of correct type
        if not isinstance(map_config, MapConfig):
            logger.error("map_config must be an instance of MapConfig.")
            raise TypeError("map_config must be an instance of MapConfig.")
        self.map_config = map_config

        # Validate event_config if provided
        if event_config is not None and not isinstance(event_config, EventConfig):
            logger.error("event_config must be an instance of EventConfig.")
            raise TypeError("event_config must be an instance of EventConfig.")
        self.event_config = event_config

        # Validate fault_config if provided
        if fault_config is not None and not isinstance(fault_config, FaultConfig):
            logger.error("fault_config must be an instance of FaultConfig.")
            raise TypeError("fault_config must be an instance of FaultConfig.")
        self.fault_config = fault_config

        # Validate station_config if provided
        if station_config is not None and not isinstance(station_config, StationConfig):
            logger.error("station_config must be an instance of StationConfig.")
            raise TypeError("station_config must be an instance of StationConfig.")
        self.station_config = station_config

        self.events = None
        self.color_map = None
        self.m = None
        self.stations = None

        # Cap the radius to half the Earth's circumference (~20,037 km)
        max_radius = EARTH_RADIUS_KM * math.pi
        if self.map_config.radius_km > max_radius:
            logger.warning(
                f"radius_km exceeds half the Earth's circumference. Capping to {max_radius} km."
            )
            self.map_config.radius_km = max_radius

        # Ensure radius_km is positive
        if self.map_config.radius_km <= 0:
            logger.error("radius_km must be a positive value.")
            raise ValueError("radius_km must be a positive value.")

    def initialize_map(self):
        """Initialize the folium map object."""
        logger.info("Initializing folium map...")

        self.m = folium.Map(
            location=[self.map_config.latitude, self.map_config.longitude],
            zoom_start=self.map_config.base_zoom_level,
            min_zoom=self.map_config.min_zoom_level,
            max_zoom=self.map_config.max_zoom_level,
            tiles=None,  # Prevents adding the default OpenStreetMap layer
        )

        # Add tile layers
        self.add_tile_layers()

        logger.info("Folium map initialized.")

    def add_tooltip_css(self) -> None:
        """Add custom CSS for tooltip styling."""
        tooltip_style = """
            <style>
                .folium-tooltip {
                    width: 200px;
                    white-space: normal;
                }
            </style>
        """
        self.m.get_root().header.add_child(folium.Element(tooltip_style))

    def set_map_bounds(self):
        """Set the map bounds based on the site location and radius."""
        logger.info("Setting map bounds...")
        bounds = self.get_combined_bounds()
        self.m.fit_bounds(bounds)
        logger.info("Map bounds set.")

    def get_combined_bounds(self):
        """Calculate and return the combined bounds for the map."""
        logger.info("Calculating combined bounds...")

        # Start with the bounding box around the site location
        site_bounds = self.get_bounding_box()

        # Initialize lists to collect all coordinates
        all_lats = [site_bounds[0][0], site_bounds[1][0]]  # min_lat, max_lat
        all_lons = [site_bounds[0][1], site_bounds[1][1]]  # min_lon, max_lon

        # Include event coordinates if available
        if self.events is not None:
            all_lats.extend(self.events["latitude"].tolist())
            all_lons.extend(self.events["longitude"].tolist())

        # Include station coordinates if available
        if self.stations is not None:
            all_lats.extend(self.stations["latitude"].tolist())
            all_lons.extend(self.stations["longitude"].tolist())

        # Compute the min and max for latitude and longitude
        min_lat, max_lat = min(all_lats), max(all_lats)
        min_lon, max_lon = min(all_lons), max(all_lons)

        bounds = [[min_lat, min_lon], [max_lat, max_lon]]
        logger.info(f"Calculated map bounds: {bounds}")
        return bounds

    def get_bounding_box(self, padding_factor=1.1):
        """Calculate the bounding box for a given point and radius with padding."""
        lat_rad = math.radians(self.map_config.latitude)
        lon_rad = math.radians(self.map_config.longitude)
        angular_distance = (
            self.map_config.radius_km * padding_factor
        ) / EARTH_RADIUS_KM

        # Limit angular_distance to pi radians
        angular_distance = min(angular_distance, math.pi)

        min_lat = math.degrees(lat_rad - angular_distance)
        max_lat = math.degrees(lat_rad + angular_distance)

        # Ensure latitude bounds are within -90 and 90 degrees
        min_lat = max(min_lat, -90)
        max_lat = min(max_lat, 90)

        cos_lat_rad = math.cos(lat_rad)

        # Compute delta_lon with clamping to avoid math domain error
        if abs(cos_lat_rad) < 1e-10:
            # At the poles, longitude bounds are irrelevant
            min_lon = -180
            max_lon = 180
        else:
            sin_angular_distance = math.sin(angular_distance)
            ratio = sin_angular_distance / cos_lat_rad

            # Clamp the ratio between -1 and 1 to avoid math domain error
            ratio = max(-1, min(1, ratio))

            delta_lon = math.asin(ratio)
            min_lon = math.degrees(lon_rad - delta_lon)
            max_lon = math.degrees(lon_rad + delta_lon)

            # Normalize longitude to be within -180 to 180 degrees
            min_lon = (min_lon + 180) % 360 - 180
            max_lon = (max_lon + 180) % 360 - 180

        return [[min_lat, min_lon], [max_lat, max_lon]]

    def create_marker_group(self, name="Events"):
        """Create a feature group for markers."""
        logger.info(f"Creating marker feature group: {name}...")
        self.marker_group = folium.FeatureGroup(name=name)

    def convert_xy_to_latlon(self, df, x_col="x", y_col="y", source_crs="EPSG:4326"):
        """
            Convert XY coordinates in a given DataFrame to latitude/longitude (WGS84).

            Parameters
            ----------
            df : pd.DataFrame
                The DataFrame containing columns for X and Y coordinates.
        x_col : str, optional
            The column name of the X (easting) coordinate. Default is 'x'.
        y_col : str, optional
            The column name of the Y (northing) coordinate. Default is 'y'.
        source_crs : str, optional
            The coordinate reference system (CRS) of the input coordinates, e.g., "EPSG:31982".
            Default is 'EPSG:4326'.

            Returns
            -------
            pd.DataFrame
                The original DataFrame with two new columns: 'latitude' and 'longitude'.

            Raises
            ------
            ValueError
                If transformation fails or input columns are missing.
        """
        logger.info("Converting XY coordinates to latitude/longitude...")
        if x_col not in df.columns or y_col not in df.columns:
            logger.error(f"DataFrame must contain '{x_col}' and '{y_col}' columns.")
            raise ValueError(f"DataFrame must contain '{x_col}' and '{y_col}' columns.")

        try:
            transformer = Transformer.from_crs(
                source_crs,  # Source CRS provided
                "EPSG:4326",  # Target CRS (WGS84)
                always_xy=True,
            )
            x_coords = df[x_col].values
            y_coords = df[y_col].values
            lon, lat = transformer.transform(x_coords, y_coords)
            df["latitude"] = lat
            df["longitude"] = lon
            logger.info("Coordinate conversion complete.")
            return df
        except Exception as e:
            logger.error(f"Error converting station coordinates: {e}")
            raise ValueError(f"Error converting coordinates: {e}")

    def assign_color(self, value):
        """Assign color based on magnitude value."""
        return "lightgrey" if value < self.event_config.vmin else self.color_map(value)

    def calculate_radius(self, value):
        """Calculate the radius of the circle marker based on a value."""
        base_radius = 2
        return (
            base_radius
            + (value - self.event_config.vmin) * self.event_config.scaling_factor
        )

    def add_tile_layers(self):
        """Add all tile layers to the map, ensuring the specified layer is the default."""
        logger.info("Adding tile layers...")

        # Add all layers except the default one
        for layer_name, config in TILE_LAYER_CONFIGS.items():
            if layer_name != self.map_config.default_tile_layer:
                folium.TileLayer(
                    layer_name,
                    name=layer_name,
                    attr=config["attr"],
                    control=True,
                    max_zoom=self.map_config.max_zoom_level,
                    min_zoom=self.map_config.min_zoom_level,
                ).add_to(self.m)

        # Add the default layer last
        default_config = TILE_LAYER_CONFIGS[self.map_config.default_tile_layer]
        folium.TileLayer(
            self.map_config.default_tile_layer,
            name=self.map_config.default_tile_layer,
            attr=default_config["attr"],
            control=True,
            max_zoom=self.map_config.max_zoom_level,
            min_zoom=self.map_config.min_zoom_level,
        ).add_to(self.m)

        logger.info("Tile layers added.")

    def add_layer_controls(self):
        """Add layer controls to the map."""
        logger.info("Adding layer control...")
        folium.LayerControl().add_to(self.m)
        logger.info("Layer control added.")

    def add_fullscreen_option(self):
        """Add a fullscreen button to the map."""
        logger.info("Adding fullscreen option...")
        plugins.Fullscreen(
            position="topleft",
            title="Full Screen",
            title_cancel="Exit Full Screen",
            force_separate_button=True,
        ).add_to(self.m)
        logger.info("Fullscreen option added.")

    def add_legends(self) -> None:
        """Add legends to the map."""
        if self.event_config is None:
            logger.info("Event configuration is missing. Skipping legends.")
            return

        # Add the magnitude color legend using branca colormap
        logger.info("Adding magnitude color legend...")
        if hasattr(self, "color_map") and self.color_map:
            self.color_map.caption = self.event_config.legend_title
            self.color_map.position = self.get_color_map_position()
            self.color_map.add_to(self.m)
            logger.info("Magnitude color legend added.")
        else:
            logger.warning("Color map not found. Magnitude color legend not added.")

    def add_site_marker(self):
        """Add a marker for the site location on the map."""
        logger.info("Adding site location marker...")
        # Create the tooltip and popup content
        tooltip_content = self.map_config.project_name
        popup_content = f"""
        <b>Site Project:</b> {self.map_config.project_name}<br>
        <b>Client:</b> {self.map_config.client}
        """

        # Add the marker with star icon, tooltip, and popup
        folium.Marker(
            location=[self.map_config.latitude, self.map_config.longitude],
            icon=folium.Icon(color="red", icon="star", prefix="fa"),
            tooltip=tooltip_content,
            popup=folium.Popup(popup_content, max_width=300),
        ).add_to(self.m)
        logger.info("Site location marker added.")

    def get_position_style(self, position):
        positions = {
            "topright": "top: 10px; right: 10px;",
            "topleft": "top: 10px; left: 10px;",
            "bottomright": "bottom: 10px; right: 10px;",
            "bottomleft": "bottom: 10px; left: 10px;",
        }
        return positions.get(position.lower(), "top: 10px; right: 10px;")

    def get_color_map_position(self) -> str:
        """Get the position for the color map legend."""
        position = self.event_config.legend_position.lower()
        positions = {
            "topright": "topright",
            "topleft": "topleft",
            "bottomright": "bottomright",
            "bottomleft": "bottomleft",
        }
        return positions.get(position, "bottomright")
