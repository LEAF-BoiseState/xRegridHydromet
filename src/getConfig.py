# The purpose of this function is to get and validate information in the config file
import yaml

def getConfig(config_yaml_fname):

    # This opens a YAML file with required keys in the config file
    with open('./src/required_keys.yml', 'r') as reqkeys_file:
        reqkeys = yaml.load(reqkeys_file, Loader=yaml.FullLoader)

    # This opens the YAML config file
    with open(config_yaml_fname, 'r') as yaml_config_file:
        config_info = yaml.load(yaml_config_file, Loader=yaml.FullLoader)

    # Check that the required control blocks and keys are in the config file. This just checks
    # that the keys are there and does not check the validity of the associated values. This 
    # compares required keys specified in the hierarchical 'required_keys.yml' file against 
    # those in the config file and raises an exception if they're not present. This approach 
    # allows expansion of future required keys, should they arise. Note that some optional keys
    # may be present but are checked in the code that requires them.

    # A key assumption is that the config file is not any deeper than two indents. That is, each
    # key block in the config file is assumed to only have one nested list

    # Get the number of required key-pair blocks in the config file
    nBlocks = len(config_info)

    for block in range(nBlocks):

        blockname = list(reqkeys[block].keys())[0]

        if(blockname not in config_info):
            raise Exception(blockname+' block is missing from '+config_yaml_fname)

        nKeysBlock = len(reqkeys[block][blockname])

        for key in range(nKeysBlock):

            this_key = reqkeys[block][blockname][key]

            if(this_key not in config_info[blockname]):
                raise Exception(this_key+' key is missing from '+blockname+' block in '+config_yaml_fname)

    return config_info