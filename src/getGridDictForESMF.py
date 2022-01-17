
# This function prepares a grid dictionary for use in the xESMF.Regridder() function

import xarray as xr
import numpy as np

def getGridDictForESMF(gridinfo_dict):

    iscurvilinear = gridinfo_dict['curvilinear']
    
    latvar_name = gridinfo_dict['latvar_name']
    lonvar_name = gridinfo_dict['lonvar_name']

    if iscurvilinear:
        latvar_b_name = gridinfo_dict['latvar_b_name']
        lonvar_b_name = gridinfo_dict['lonvar_b_name']
    else: # See if the user entered variable names for latvar_b_name and lonvar_b_name, even if 
        # The grid is rectilinear
            
        if(('latvar_b_name' in gridinfo_dict) and 
           ('lonvar_b_name' in gridinfo_dict)):
            latvar_b_name = gridinfo_dict['latvar_b_name']
            lonvar_b_name = gridinfo_dict['lonvar_b_name']
        else:
            latvar_b_name = None
            lonvar_b_name = None
            
    grid_template_fname = gridinfo_dict['template_file']
    
    ds = xr.open_dataset(grid_template_fname)
    
    lat = ds[latvar_name].data
    lon = ds[lonvar_name].data
    
    if(ds[latvar_name].ndim==1):
        lat = ds[latvar_name].data
    elif(ds[latvar_name].ndim==2):
        lat = ds[latvar_name].data    
    else:
        dropdim = gridinfo_dict['latvar_dropdim']
        lat = ds[latvar_name].isel({dropdim: 0}).data

    if(ds[lonvar_name].ndim==1):
        lon = ds[lonvar_name].data
    elif(ds[latvar_name].ndim==2):
        lon = ds[lonvar_name].data    
    else:
        dropdim = gridinfo_dict['lonvar_dropdim']
        lon = ds[lonvar_name].isel({dropdim: 0}).data
            
    # Boundaries of cells
    if(iscurvilinear): # If curvilinear, these must be provided
        # Get boundary latitude
        if(ds[latvar_b_name].ndim==2):
            lat_b = ds[latvar_b_name].data
        else:
            dropdim = gridinfo_dict['latvar_b_dropdim']
            lat_b = ds[latvar_b_name].isel({dropdim: 0}).data

        # Get boundary latitude
        if(ds[lonvar_b_name].ndim==2):
            lon_b = ds[lonvar_b_name].data
        else:
            dropdim = gridinfo_dict['lonvar_b_dropdim']
            lon_b = ds[lonvar_b_name].isel({dropdim: 0}).data

    # If rectilinear, these *might* have been provided
    elif (iscurvilinear == False) and (latvar_b_name is not None) and (lonvar_b_name is not None): 
        # Get boundary latitude
        if(ds[latvar_b_name].ndim==2):
            lat_b = ds[latvar_b_name].data
        else:
            dropdim = gridinfo_dict['latvar_b_dropdim']
            lat_b = ds[latvar_b_name].isel({dropdim: 0}).data

        # Get boundary latitude
        if(ds[lonvar_b_name].ndim==2):
            lon_b = ds[lonvar_b_name].data
        else:
            dropdim = gridinfo_dict['lonvar_b_dropdim']
            lon_b = ds[lonvar_b_name].isel({dropdim: 0}).data
    
    else: # Calculate corners for rectilinear cases where boundaries not provided
        
        if(lat.ndim==1) and (lon.ndim==1):
            lat_b = np.append((lat[0]-0.5*(lat[1]-lat[0])),(lat+0.5*(lat[1]-lat[0])))
            lon_b = np.append((lon[0]-0.5*(lon[1]-lon[0])),(lon+0.5*(lon[1]-lon[0])))
        
        else:

            lat_b = np.concatenate(((np.expand_dims(lat[0,:]-0.5*(lat[1,:]-lat[0,:]),axis=0)),
                                    np.array(lat+0.5*(lat[1,:]-lat[0,:]))),axis=0)
            lat_b = np.concatenate((lat_b,np.expand_dims(lat_b[:,-1],axis=1)),axis=1)
            
            lon_b = np.concatenate(((np.expand_dims(lon[:,0]-0.5*(lon[:,1]-lon[:,0]),axis=1)),
                                    np.array(lon+0.5*(lon[1,:]-lon[0,:]))),axis=1)
            lon_b = np.concatenate((lon_b,np.expand_dims(lon_b[-1,:],axis=0)),axis=0)
            
    # If lat, lat_b, lon, and lon_b are 1-D arrays, use meshgrid to make 2-D arrays
    if(lat.ndim==1) and (lon.ndim==1):
        lon, lat = np.meshgrid(lon,lat)
        
    if(lat_b.ndim==1) and (lon_b.ndim==1):
        lon_b, lat_b = np.meshgrid(lon_b,lat_b)

    grid_for_esmf = {'lon': lon, 'lat': lat,
            'lon_b': lon_b, 'lat_b': lat_b}

    return grid_for_esmf
