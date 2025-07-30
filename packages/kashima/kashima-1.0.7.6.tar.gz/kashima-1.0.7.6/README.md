# Kashima

**Machine Learning Tools for Geotechnical Earthquake Engineering**

Kashima is a Python library designed for seismological and geotechnical applications, providing powerful tools for earthquake event visualization, catalog processing, and interactive mapping. Built on top of Folium, it creates rich web maps for seismic data analysis and visualization.

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Features

- **Interactive Seismic Maps**: Create stunning Folium-based web maps with earthquake events
- **Multi-Catalog Support**: Integrate data from USGS, ISC, and custom blast catalogs
- **Advanced Visualizations**: 
  - Magnitude-scaled event markers with customizable color schemes
  - Seismic moment tensor beachball plots
  - Epicentral distance circles
  - Activity heatmaps
  - Geological fault line overlays
  - Seismic station markers
- **Flexible Configuration**: Configuration-driven design using dataclasses
- **Coordinate System Support**: Handle multiple CRS with automatic transformations
- **Large Dataset Handling**: Efficient processing of large seismic catalogs
- **Mining Applications**: Specialized tools for blast event analysis

## Installation

### From PyPI
```bash
pip install kashima
```

### Development Installation
```bash
git clone https://github.com/averriK/kashima.git
cd kashima
pip install -e .
```

### Dependencies
```bash
pip install pandas numpy folium geopandas pyproj requests branca geopy matplotlib obspy
```

## Quick Start

### Basic Earthquake Map

```python
from kashima.mapper import EventMap, MapConfig, EventConfig, USGSCatalog
from datetime import datetime, timedelta

# Configure the map
map_config = MapConfig(
    project_name="Central California Seismicity",
    client="Research Project",
    latitude=36.7783,
    longitude=-119.4179,
    radius_km=200,
    base_zoom_level=8
)

event_config = EventConfig(
    color_palette="viridis",
    scaling_factor=3.0,
    show_events_default=True,
    show_heatmap_default=False
)

# Create the map
event_map = EventMap(map_config, event_config)

# Load USGS earthquake data
end_time = datetime.now()
start_time = end_time - timedelta(days=30)

catalog = USGSCatalog()
events = catalog.search(
    starttime=start_time,
    endtime=end_time,
    latitude=map_config.latitude,
    longitude=map_config.longitude,
    maxradiuskm=map_config.radius_km,
    minmagnitude=2.0
)

# Build and display the map
folium_map = event_map.build(events)
folium_map.save("earthquake_map.html")
```

### Mining Blast Analysis

```python
from kashima.mapper import EventMap, BlastCatalog, BlastConfig

# Configure blast data processing
blast_config = BlastConfig(
    blast_file_path="blast_data.csv",
    coordinate_system="EPSG:32722",  # UTM Zone 22S
    f_TNT=0.90,
    a_ML=0.75,
    b_ML=-1.0
)

# Process blast catalog
blast_catalog = BlastCatalog(blast_config)
blast_catalog.read_blast_data()
blast_events = blast_catalog.build_catalog()

# Create visualization
map_config = MapConfig(
    project_name="Mine Site Blasting",
    client="Mining Company",
    latitude=-23.5505,
    longitude=-46.6333,
    radius_km=50
)

event_map = EventMap(map_config)
blast_map = event_map.build(blast_events)
```

### Advanced Multi-Layer Visualization

```python
from kashima.mapper import EventMap, MapConfig, EventConfig, FaultConfig, StationConfig

# Complete configuration
map_config = MapConfig(
    project_name="Comprehensive Seismic Analysis",
    client="Seismic Network",
    latitude=37.7749,
    longitude=-122.4194,
    radius_km=300,
    default_tile_layer="ESRI_SATELLITE",
    epicentral_circles=7
)

event_config = EventConfig(
    color_palette="plasma",
    scaling_factor=2.5,
    show_events_default=True,
    show_heatmap_default=True,
    show_beachballs_default=True,
    beachball_min_magnitude=4.0,
    heatmap_radius=25
)

fault_config = FaultConfig(
    include_faults=True,
    faults_gem_file_path="faults.shp",
    regional_faults_color="red",
    regional_faults_weight=2
)

station_config = StationConfig(
    station_file_path="stations.csv",
    layer_title="Seismic Network"
)

# Build comprehensive map
event_map = EventMap(
    map_config=map_config,
    event_config=event_config,
    fault_config=fault_config,
    station_config=station_config
)

# Load and combine data sources
usgs_events = USGSCatalog().search(...)
comprehensive_map = event_map.build(usgs_events)
```

## Configuration Options

### MapConfig
Core map display settings:
```python
MapConfig(
    project_name="Project Name",
    client="Client Name", 
    latitude=40.0,
    longitude=-120.0,
    radius_km=100,
    base_zoom_level=8,
    default_tile_layer="OpenStreetMap",
    epicentral_circles=5,
    auto_fit_bounds=True
)
```

### EventConfig
Event visualization parameters:
```python
EventConfig(
    color_palette="magma",           # Color scheme: magma, viridis, plasma, etc.
    color_reversed=False,
    scaling_factor=2.0,              # Size scaling for magnitude
    legend_position="bottomright",
    show_events_default=True,        # Layer visibility on load
    show_heatmap_default=False,
    show_beachballs_default=False,
    heatmap_radius=20,
    heatmap_blur=15,
    beachball_min_magnitude=4.0
)
```

## Supported Tile Layers

Kashima supports numerous base map layers:
- **OpenStreetMap**: Standard OSM rendering
- **ESRI Layers**: Satellite imagery, terrain, streets, relief
- **CartoDB**: Positron, dark matter, voyager themes  
- **Stamen**: Terrain and toner artistic styles
- **OpenTopoMap**: Topographic mapping
- **CyclOSM**: Cycling-focused rendering

## Data Sources

### USGS Earthquake Catalog
```python
from kashima.mapper import USGSCatalog

catalog = USGSCatalog()
events = catalog.search(
    starttime=datetime(2023, 1, 1),
    endtime=datetime(2023, 12, 31),
    latitude=36.0,
    longitude=-120.0,
    maxradiuskm=200,
    minmagnitude=3.0,
    want_tensor=True  # Include moment tensor data
)
```

### Custom Blast Data
For mining applications, process blast data with coordinate conversion:
```python
from kashima.mapper import BlastCatalog, BlastConfig

config = BlastConfig(
    blast_file_path="blasts.csv",
    coordinate_system="EPSG:32633",  # UTM Zone 33N
    f_TNT=0.85,     # TNT equivalency factor
    a_ML=0.75,      # Magnitude calculation parameters
    b_ML=-1.0
)
```

## Advanced Features

### Coordinate System Transformations
Automatic conversion between coordinate systems:
```python
# Input data in UTM, output in WGS84 for web mapping
blast_config = BlastConfig(
    coordinate_system="EPSG:32722"  # UTM Zone 22S
)
```

### Large Dataset Handling
Efficient processing of large catalogs:
```python
# Stream processing for large CSV files
from kashima.mapper.utils import stream_read_csv_bbox

bbox = great_circle_bbox(lon0, lat0, radius_km)
events = stream_read_csv_bbox(
    "large_catalog.csv", 
    bbox, 
    chunksize=50000
)
```

### Custom Layer Combinations
```python
from kashima.mapper.layers import (
    EventMarkerLayer, 
    HeatmapLayer, 
    BeachballLayer,
    EpicentralCirclesLayer
)

# Build custom layer combinations
event_layer = EventMarkerLayer(events, event_config)
heatmap_layer = HeatmapLayer(events, event_config) 
circles_layer = EpicentralCirclesLayer(map_config)
```

## Use Cases

- **Seismic Hazard Assessment**: Visualize historical earthquake activity
- **Mining Seismology**: Monitor and analyze blast-induced seismicity
- **Research Applications**: Academic earthquake research and publication
- **Emergency Response**: Real-time seismic event mapping
- **Geotechnical Engineering**: Site-specific seismic analysis
- **Education**: Teaching earthquake science and hazards

## API Reference

### Core Classes
- **`EventMap`**: Main visualization class
- **`USGSCatalog`**: USGS earthquake data interface  
- **`BlastCatalog`**: Mining blast data processor
- **`BaseMap`**: Foundation mapping functionality

### Configuration Classes
- **`MapConfig`**: Core map parameters
- **`EventConfig`**: Event visualization settings
- **`FaultConfig`**: Fault line display options
- **`StationConfig`**: Seismic station configuration
- **`BlastConfig`**: Blast data processing parameters

### Layer Classes  
- **`EventMarkerLayer`**: Individual event markers
- **`HeatmapLayer`**: Activity density visualization
- **`BeachballLayer`**: Moment tensor focal mechanisms
- **`FaultLayer`**: Geological fault lines
- **`StationLayer`**: Seismic station markers
- **`EpicentralCirclesLayer`**: Distance rings

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use Kashima in your research, please cite:

```bibtex
@software{kashima,
  author = {Alejandro Verri Kozlowski},
  title = {Kashima: Machine Learning Tools for Geotechnical Earthquake Engineering},
  url = {https://github.com/averriK/kashima},
  version = {1.0.7.3},
  year = {2024}
}
```

## Contact

- **Author**: Alejandro Verri Kozlowski
- **Email**: averri@fi.uba.ar
- **GitHub**: [@averriK](https://github.com/averriK)

## Changelog

### Version 1.0.7.3
- Enhanced coordinate system support
- Improved large dataset handling
- Added beachball visualization
- Extended tile layer options
- Better error handling and logging