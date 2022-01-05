import xesmf as xe
import numpy as np
import getGridMetaData
import getGridDictForESMF
import yaml

def getBuildWeights(config_dict):

    src_gridinfo_yaml = config_dict['srcinfo']['src_gridinfo']
    dest_gridinfo_yaml = config_dict['destinfo']['dest_gridinfo']

    # Get source grid info
    src_gridinfo = getGridMetaData.getGridMetaData(src_gridinfo_yaml)

    # Get destination grid info 
    dest_gridinfo = getGridMetaData.getGridMetaData(dest_gridinfo_yaml)

    # Prepare the source grid for input to xESMF regridder
    src_grid = getGridDictForESMF.getGridDictForESMF(src_gridinfo)

    # Prepare the destination grid for input to xESMF regridder
    dest_grid = getGridDictForESMF.getGridDictForESMF(dest_gridinfo)

    # Call xESMF regridder
    regrid_method = config_dict['jobinfo']['xesmf_method']

    regridder = xe.Regridder(src_grid, dest_grid, regrid_method)

    return regridder
    