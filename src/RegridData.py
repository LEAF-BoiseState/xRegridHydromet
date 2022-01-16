import xarray as xr
import numpy as np
import xesmf as xe 
import glob
import getGridMetaData
import getGridDictForESMF
import time
import datetime

def RegridData(config_data,regridder=None):

    # This is a stub... data regridding will be added here
    start = time.time()

    # If regridder is none, the user wants to reuse a previous weight file
    if(regridder is None):
        
        # If regridder is None, check to make sure 'regridder_fname' is in the config file
        if('regridder_fname' not in config_data['jobinfo']):
            # If not raise exception
            raise Exception('If build_weights is False, then regridder file name must be specified') 

        # If passing, get the regridder file name
        regridder_fname = config_data['jobinfo']['regridder_fname']

    # Get the metadata for the source and destination grids
    src_gridinfo = getGridMetaData.getGridMetaData(config_data['srcinfo']['src_gridinfo'])

    # Get the source directory where the grid data is stored
    dest_gridinfo = getGridMetaData.getGridMetaData(config_data['destinfo']['dest_gridinfo'])

    # We are doing file-by-file regridding. Why, when we could open as an xArray dataset?
    # Because we can't be sure on the correct dimension for contatenation.
    if('src_dir' not in config_data['srcinfo']):
        raise Exception()

    # Get the source folder
    src_dir = config_data['srcinfo']['src_dir']

    # Get list of source files
    # Error trap to ensure the user provided a string to use to search for files
    if('srcfile_pattern' not in config_data['srcinfo']):
        raise Exception('srcfile_pattern missing! The source grid metadata file must '
            'contain a string file name pattern with which to search for files to regrid')

    src_file_pattern = config_data['srcinfo']['srcfile_pattern'] # Get the search string pattern
    src_files = glob.glob(src_file_pattern) # Get a list of source grid files to regrid

    # Get the destination folder of the destination regridded files
    # Error trap to ensure the user provided a folder in which to save regridded files
    if('dest_dir' not in config_data['destinfo']):
        raise Exception()

    dest_dir = config_data['destinfo']['dest_dir'] # Get the destination directory of regridded files

    # Error trap to ensure the user provided a string that will replace the source file string pattern
    # when saving
    if('destfile_pattern' not in config_data['destinfo']):
        raise Exception('destfile_pattern missing! The destination grid metadata file must '
            'contain a string file name pattern with save regridded files')

    # Get the file name pattern for destination files
    dest_file_pattern = config_data['destinfo']['destfile_pattern']

    # Read regridder if we are reusing weights
    if(regridder is None):
        # Prepare the source grid for input to xESMF regridder
        src_grid = getGridDictForESMF.getGridDictForESMF(src_gridinfo)

        # Prepare the destination grid for input to xESMF regridder
        dest_grid = getGridDictForESMF.getGridDictForESMF(dest_gridinfo)

        regridder = xe.Regridder(src_grid, dest_grid, config_data['jobinfo']['xesmf_method'], 
            weights=regridder_fname)

    # Loop through files
    for src_file in src_files:        

        # Open the file
        ds_src = xr.open_dataset(src_file)

        # Apply the regridder
        ds_out = regridder(ds_src)

        # Save the output
        out_fname = dest_dir + src_file.replace(src_file_pattern, dest_file_pattern)
        ds_out.to_netcdf(out_fname)

    end = time.time()

    dt = datetime.timedelta(seconds=(end-start))
    print('Completed data regridding process in elapsed time of '+str(dt))

    return