import getConfig
import getBuildWeights
import RegridData
import time
import datetime 

def run(config_yaml_fname):

    # Start timer
    t_start = time.time()

    # Open and validate the config file data
    config_data = getConfig.getConfig(config_yaml_fname)

    # Check if we are building the grid weights
    if(config_data['jobinfo']['build_weights']):
        # Build the regridding weight matrix
        regridder = getBuildWeights.getBuildWeights(config_data)

        # Create a unique file name for the output weight matrix
        regridder_fname = config_data['jobinfo']['jobtag']+'_'+regridder.filename

        # Save the regridder weight matrix to a netcdf file
        regridder.to_netcdf(regridder_fname)
    else:
        regridder=None

    # Check if we are actually regridding any data
    if(config_data['jobinfo']['regrid_data']):
        RegridData.RegridData(config_data,regridder=regridder)

    # Stop timer 
    t_end = time.time()

    # Compute time delta
    dt = datetime.timedelta(seconds=(t_end - t_start))

    print('Job '+config_data['jobinfo']['jobname']+' completed at '+str(datetime.datetime.now())+' UTC')
    print('Total elapsed time = '+str(dt))

    return
