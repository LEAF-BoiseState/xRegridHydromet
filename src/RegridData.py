import xarray as xr
import numpy as np
import xesmf as xe 
import glob
import getGridMetaData
import time
import datetime

def RegridData(config_data,regridder=None):

    # # This is a stub... data regridding will be added here
    # start = time.time()

    # # If regridder is none, the user wants to reuse a previous weight file
    # if(regridder is None):
        
    #     # If regridder is None, check to make sure 'regridder_fname' is in the config file
    #     if('regridder_fname' not in config_data['jobinfo']):
    #         # If not raise exception
    #         raise Exception('If build_weights is False, then regridder file name must be specified') 

    #     # If passing, get the regridder file name
    #     regridder_fname = config_data['jobinfo']['regridder_fname']

    # # Get the metadata for the source and destination grids
    # src_gridinfo = getGridMetaData.getGridMetaData(config_data['srcinfo']['src_gridinfo'])

    # # Get the source directory where the grid data is stored
    # dest_gridinfo = getGridMetaData.getGridMetaData(config_data['destinfo']['dest_gridinfo'])

    # # We are doing file-by-file regridding. Why, when we could open as an xArray dataset?
    # # Because we can't be sure on the correct dimension for contatenation.
    # if('src_dir' not in config_data['srcinfo']):
    #     raise Exception()

    # # Get the source folder
    # src_dir = config_data['srcinfo']['src_dir']

    # if('dest_dir' not in config_data['destinfo']):
    #     raise Exception()

    # # Get the destination folder
    # dest_dir = config_data['destinfo']['dest_dir']

    # # Get list of source files
    # src_file_pattern = src_gridinfo
    # src_files = glob.glob()

    # # Read regridder if we are reusing weights
    # if(regridder is None):
    #     regridder = xe.ASDF(regridder_fname)


    # # Loop through files
    # for src_file in src_files:        

    #     # Open the file
    #     ds = xr.open_dataset(file)

    #     # Apply the regridder
    #     ds_out = regridder(ds)

    #     # Save the output
    #     out_fname = 
    #     ds_out.to_netcdf(out_fname)

    # end = time.time()

    # dt = datetime.timedelta(seconds=(end-start))
    # print('Completed data regridding process in elapsed time of '+str(dt))

    return