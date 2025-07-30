"""
data_loader.py
Module to load time series data and provide a shared interface for other modules.
"""
import logging
from typing import Optional, Union
import pandas as pd
import json
import os


class DataLoader:
    """
    DataLoader is a class for loading and managing time series data from a CSV file.
    Attributes:
        filepath (str): Path to the CSV file containing the data.
        index_col (str or int, optional): Column to use as the row labels of the DataFrame.
        parse_dates (bool or list, optional): Whether to parse dates in the index column.
        data (pd.DataFrame or None): Loaded data after calling `load()`.
    Methods:
        load():
            Loads the data from the specified CSV file, saves metadata, and standardizes column names to lowercase.
            Returns the loaded DataFrame.
        is_regular():
            Checks if the time series index is regular (i.e., intervals between timestamps are uniform).
            Returns True if regular, False otherwise.
        save_metadata():
            Saves metadata (columns, dtypes, shape, index name) of the loaded DataFrame to a JSON file
            with the same name as the CSV file, suffixed with '_meta.json'.
        run_pipeline():
            Runs the data loading pipeline: loads data, checks regularity, and renames the first column to 'y' if regular.
            Returns the processed DataFrame if regular, otherwise None.
    """
    
    def __init__(self, filepath: str, index_col: Optional[Union[str, int]] = None, parse_dates: Union[bool, list] = True):
        self.filepath = filepath
        self.index_col = index_col
        self.parse_dates = parse_dates
        self.data = None

        # Data paths file name
        self.base_name = os.path.splitext(os.path.basename(self.filepath))[0]

        base_dir = os.getcwd()
        log_dir = os.path.join(base_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_filename = os.path.splitext(os.path.basename(__file__))[0] + ".log"
        log_path = os.path.join(log_dir, log_filename)
        
        # Set up logging
        if not logging.getLogger().hasHandlers():
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_path),
                    logging.StreamHandler()
                ]
                )

    def load(self) -> pd.DataFrame:
        """Load the data from the specified CSV file."""
        try:
            self.data = pd.read_csv(self.filepath, index_col=self.index_col, parse_dates=self.parse_dates)
            self.data.columns = self.data.columns.str.lower()
            self.data.index.name = self.data.index.name.lower() if self.data.index.name else None
            # self.save_metadata()
            return self.data
        except Exception as e:
            logging.error(f"Error loading data from {self.filepath}: {e}")
            raise ValueError(f"Failed to load data from {self.filepath}. Please check the file format and path.") from e
    
    def is_regular(self) -> bool:
        """Check if the time series data is regular."""
        if self.data.index.isnull().sum() > 0:
            logging.warning("Data contains null values in the index, Cannot proceed with this data further.")
            return False

        # Ensure index is a DatetimeIndex
        if not isinstance(self.data.index, pd.DatetimeIndex):
            logging.warning("Index is not a DatetimeIndex. Cannot check regularity.")
            return False

        # Calculate differences between consecutive timestamps
        diffs = self.data.index.to_series().diff().dropna()
        if diffs.nunique() == 1:
            logging.info(f"Data is regular. Index differences are uniform: {diffs.iloc[0]}")
            return True
        else:
            logging.warning("Data is not regular. Index differences are not uniform.")
            logging.warning(f"Unique differences found: {diffs.unique()}" )
            return False


    def save_metadata(self) -> None:
        """Save metadata of the DataFrame to a JSON file."""

        # base_name = os.path.splitext(os.path.basename(self.filepath))[0]
        base_dir = os.getcwd()
        metadata_dir = os.path.join(base_dir, "metadata")
        os.makedirs(metadata_dir, exist_ok=True)
        meta_filename = os.path.splitext(os.path.basename(self.filepath))[0] + "_meta.json"
        meta_path = os.path.join(metadata_dir, meta_filename)

        metadata = {
            "columns": list(self.data.columns),
            "dtypes": {col: str(dtype) for col, dtype in self.data.dtypes.items()},
            "shape": self.data.shape,
            "index_name": self.data.index.name,
        }
        try:
            with open(meta_path, "w") as f:
                json.dump(metadata, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving metadata to {meta_path}: {e}")
            raise ValueError(f"Failed to save metadata to {meta_path}.") from e
        
    def run_pipeline(self) -> Optional[pd.DataFrame]:
        """Run the data loading pipeline."""
        logging.info("loading data...")
        self.load()
        if not self.is_regular():
            logging.warning("Pipeline completed. Data is loaded but may not be regular.")
            return self.data   # Return the data anyway for inspection.        
        logging.info("Data loaded is regular. Further processing may be needed.")
        self.save_metadata()
        return self.data


# Usage
if __name__ == "__main__":
    loader = DataLoader(filepath="sample_data/date_count.csv", index_col="Date")
    result = loader.run_pipeline()
    if result is not None:
        logging.info("Data loaded successfully.")
 