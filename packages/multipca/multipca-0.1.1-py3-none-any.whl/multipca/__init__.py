from .solver import mpca, mpca_CI
from .plot import CI_plot, CI_band_plot, loading_plot
import numpy as np
from pathlib import Path

__all__ = [
    "mpca", "mpca_CI",
    "CI_plot", "CI_band_plot", "loading_plot",
    "load_citibike_example"
]

def load_citibike_example():
    """Load the example Citibike dataset.
    
    Returns
    -------
    array : ndarray, shape (24, 35, 522)
        Bike sharing data from NYC where:
        - First dimension (24): Hours of the day
        - Second dimension (35): Different bike stations
        - Third dimension (522): Days in the dataset
    """
    data_path = Path(__file__).parent / 'data' / 'citibike_data.npy'
    return np.load(str(data_path))
