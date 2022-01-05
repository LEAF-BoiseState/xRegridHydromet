import sys
sys.path.append('src')

import conductor

def main(argv):

    # Check for correct number of arguments
    if(len(argv)!=1):
        print('\nusage: xRegridHydromet.py <config YAML file>')
        print('\t <config YAML file>: Config file containing key-value pairs for the regridding')
        raise Exception('Incorrect number of input arguments')

    config_yaml_fname = argv[0]

    conductor.run(config_yaml_fname)

if __name__ == '__main__':
    main(sys.argv[1:])