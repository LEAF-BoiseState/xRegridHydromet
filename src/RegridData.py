import xarray as xr
import numpy as np
import xesmf as xe 
import glob
import getGridMetaData
import getGridDictForESMF
import time
import datetime

def RegridData(config_data,regridder=None):

    start = time.time() # Start timing

    #=========================================#
    # Retrieve information about source files # 
    #=========================================#

    # We are doing file-by-file regridding. Why, when we could open as an xArray dataset?
    # Because we can't be sure on the correct dimension for contatenation.
    if('src_dir' not in config_data['srcinfo']):
        raise Exception('Location of source grids not provided in config file')

    # Get the source folder
    src_dir = config_data['srcinfo']['src_dir']

    # Get list of source files
    # Error trap to ensure the user provided a string to use to search for files
    if('srcfile_pattern' not in config_data['srcinfo']):
        raise Exception('srcfile_pattern missing! The source grid metadata file must '
            'contain a string file name pattern with which to search for files to regrid')

    src_file_pattern = config_data['srcinfo']['srcfile_pattern'] # Get the search string pattern
    src_files = glob.glob(src_dir+src_file_pattern+'*') # Get a list of source grid files to regrid

    # Get the metadata for the source and destination grids
    src_gridinfo = getGridMetaData.getGridMetaData(config_data['srcinfo']['src_gridinfo'])

    #=============================================#
    # Retrieve information about destination grid # 
    #=============================================#

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

    # Get the source directory where the grid data is stored
    dest_gridinfo = getGridMetaData.getGridMetaData(config_data['destinfo']['dest_gridinfo'])

    #======================================================#
    # Prepare the regridder, if it was not passed as input # 
    #======================================================#
    # If the regridder is not passed as input, assuming the user wants 
    # passed a filename to a previously created weight file. Open it now
    if(regridder is None):
        
        # If regridder is None, check to make sure 'regridder_fname' is in the config file
        if('regridder_fname' not in config_data['jobinfo']):
            # If not raise exception
            raise Exception('If build_weights is False, then regridder file name must be specified') 

        # Prepare the source grid for input to xESMF regridder
        src_grid_dict = getGridDictForESMF.getGridDictForESMF(src_gridinfo)

        # Prepare the destination grid for input to xESMF regridder
        dest_grid_dict = getGridDictForESMF.getGridDictForESMF(dest_gridinfo)

        # If passing, get the regridder file name
        regridder_fname = config_data['jobinfo']['regridder_fname']

        regridder = xe.Regridder(src_grid_dict, dest_grid_dict, config_data['jobinfo']['xesmf_method'], 
            weights=regridder_fname)

    #===============================================#
    # Loop through the source grid files and regrid # 
    #===============================================#

    for src_file in src_files:        

        # Open the file
        ds_src = xr.open_dataset(src_file)

        # Apply the regridder
        ds_out = regridder(ds_src)

        # Check and set the correct coordiates 
        if(dest_gridinfo['latvar_name'] != 'lat'):
            ds_out = ds_out.rename({'lat': dest_gridinfo['latvar_name']})

        if(dest_gridinfo['lonvar_name'] != 'lon'):
            ds_out = ds_out.rename({'lon': dest_gridinfo['lonvar_name']})

        # Check and set dimension names
        if('xdimname' in dest_gridinfo):
            ds_out = ds_out.rename({'x': dest_gridinfo['xdimname']})

        if('ydimname' in dest_gridinfo):
            ds_out = ds_out.rename({'y': dest_gridinfo['ydimname']})

        # Prepare the filename and save the output
        out_fname = src_file.split('/')[-1] # Get just the file name, without the path
        out_fname = out_fname.replace(src_file_pattern, dest_file_pattern) # Replace the search pattern with destination
        ds_out.to_netcdf(dest_dir + out_fname) # Save to NetCDF file

    end = time.time() # Stop timing

    dt = datetime.timedelta(seconds=(end-start))
    print('Completed data regridding process in elapsed time of '+str(dt))

    return