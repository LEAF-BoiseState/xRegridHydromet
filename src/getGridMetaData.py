import yaml

def getGridMetaData(gridinfo_yaml_fname):

    with open(gridinfo_yaml_fname, 'r') as yaml_file:
        gridinfo = yaml.load(yaml_file, Loader=yaml.FullLoader)

    iscurvilinear = gridinfo['curvilinear']

    if(iscurvilinear):
        print(gridinfo_yaml_fname+' indicates grid is curvilinear')
    else:
        print(gridinfo_yaml_fname+' indicates grid is rectilinear')
        
    # Example error checks
    assert gridinfo['latvar_name'], 'Source latvar_name key does not exist in'+gridinfo_yaml_fname
    assert gridinfo['lonvar_name'], 'Source latvar_name key does not exist in'+gridinfo_yaml_fname

    if(iscurvilinear):
        if('latvar_b_name' not in gridinfo) or ('lonvar_b_name' not in gridinfo):
            raise Exception('For curvilinear grids, variable containing cell borders must be included in'+gridinfo_yaml_fname)

    if('template_file' not in gridinfo):
        raise Exception('Name of a template file must be specified in'+gridinfo_yaml_fname)

    return gridinfo
