import logging
import pandas as pd
from .config import BlastConfig
from .utils import convert_xy_to_latlon, calculate_magnitude  # Import functions from utils

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class BlastCatalog:
    """Class to process blast data and build a catalog."""
    def __init__(self, blast_config: BlastConfig):
        self.blast_config = blast_config
        self.dataframe = None

    def read_blast_data(self):
        """Read blast data from CSV file."""
        try:
            self.dataframe = pd.read_csv(self.blast_config.blast_file_path)
            logger.info(f"Blast data loaded from {self.blast_config.blast_file_path}")
        except Exception as e:
            logger.error(f"Failed to read blast data: {e}")
            self.dataframe = pd.DataFrame()

    def build_catalog(self):
        """Build catalog DataFrame with required columns."""
        if self.dataframe is None or self.dataframe.empty:
            logger.error("No data to build catalog.")
            return pd.DataFrame()

        # Check for essential columns x, y, Q
        essential_columns = ['x', 'y', 'Q']
        missing_essentials = [col for col in essential_columns if col not in self.dataframe.columns]
        if missing_essentials:
            logger.error(f"Missing essential columns: {missing_essentials}")
            return pd.DataFrame()

        # Convert coordinates if not already done
        if 'latitude' not in self.dataframe.columns or 'longitude' not in self.dataframe.columns:
            self.process_data()

        # Calculate magnitude if not already done
        if 'mag' not in self.dataframe.columns:
            self.calculate_magnitude()
        
        # Add or modify the 'magType' column
        self.dataframe['magType'] = 'ML'

        # Handle 'depth' column; if not present, create with default value 0
        if 'depth' not in self.dataframe.columns:
            if 'z' in self.dataframe.columns:
                self.dataframe['depth'] = self.dataframe['z']
            else:
                self.dataframe['depth'] = 0

        # Handle 'time' column; if not present, create with an arbitrary date
        if 'date' in self.dataframe.columns:
            self.dataframe['time'] = pd.to_datetime(self.dataframe['date'], format='%d/%m/%Y', errors='coerce')
        else:
            # Assign arbitrary date '1970-01-01'
            self.dataframe['time'] = pd.Timestamp('1970-01-01')

        # Handle 'place' column; if not present, assign 'Unknown'
        self.dataframe['place'] = self.dataframe.get('place', 'Unknown')

        # Handle 'id' column; if not present, assign sequence numbers
        if 'id' not in self.dataframe.columns:
            self.dataframe['id'] = range(1, len(self.dataframe) + 1)

        # Select required columns
        required_columns = ['latitude', 'longitude', 'mag', 'magType', 'depth', 'id', 'time', 'place']
        catalog = self.dataframe[required_columns].copy()

        # Drop rows with missing essential values
        catalog.dropna(subset=['latitude', 'longitude', 'mag'], inplace=True)

        logger.info(f"Catalog built with {len(catalog)} events.")
        return catalog

    def process_data(self):
        """Process the blast data by converting coordinates and calculating magnitude."""
        if self.dataframe is None or self.dataframe.empty:
            logger.error("No data to process.")
            return

        # Convert coordinates using the utility function
        x_coords = self.dataframe['x'].values
        y_coords = self.dataframe['y'].values

        lon, lat = convert_xy_to_latlon(
            x_coords,
            y_coords,
            source_crs=self.blast_config.coordinate_system
        )

        self.dataframe['longitude'] = lon
        self.dataframe['latitude'] = lat

        # Calculate magnitude using the function from utils
        Q_values = self.dataframe['Q'].values

        mag = calculate_magnitude(
            Q=Q_values,
            f_TNT=self.blast_config.f_TNT,
            a_ML=self.blast_config.a_ML,
            b_ML=self.blast_config.b_ML
        )

        self.dataframe['mag'] = mag
        logger.info("Magnitude calculation completed.")


