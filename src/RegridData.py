import xarray as xr
import numpy as np
import xesmf as xe 
import time
import datetime

def RegridData(config_data,regridder=None):

    # This is a stub... data regridding will be added here
    start = time.time()

    # Pseudocode:
    # If regridder is not None, then we've been handed a regridder
    # If regridder is None, we need to open it based on a file name in the config file
    #     error trap that the file name is in the config file 
    #     open it
    #
    # Get the source directory where the grid data is stored
    # Open the source data
    # Apply the regridder
    # Save the output
    # Clean up

    end = time.time()

    dt = datetime.timedelta(seconds=(end-start))
    print('Completed data regridding process in elapsed time of '+str(dt))

    return