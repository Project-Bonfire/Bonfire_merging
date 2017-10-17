"""
Reads and processes the configuration files for desingns

Copyright (C) 2016 - 2017 Karl Janson, Siavoosh Payandeh Azad, Behrad Niazmand

Release under the GPLv3 license:
https://www.gnu.org/licenses/gpl-3.0.en.html
"""

import sys
import yaml
from Scripts.include.misc.helper_func import *
from Scripts.include.misc.package import *


def extract_config_path(args):
    """
    Calculates a config directory based on the script's arguments
    :param args: ArgParser instance
    :return:     Directory for the configuration files
    """

    if args.simulate:
        config_dir = package.SIM_CONF_DIR
        config_name = args.simulate

    elif args.asic:
        config_dir = package.ASIC_CONF_DIR
        config_name = args.asic

    elif args.fpga:
        config_dir = package.FPGA_CONF_DIR
        config_name = args.fpga

    else:
        raise ValueError("Unknown config type. How did we get here???")

    config_file = os.path.join(config_dir, config_name + '.yml')

    return config_file


def check_file_format(yaml_config, config_file, top_level):
    """
    Checks if all required fields exist in the YAML file
    :param yaml_config: (dictionary) Top level configuration read from a YAML file
    :param config_file: (str)        Name of the configuration file
    :param top_level:   (bool)       If we are checking the top level if the main config file
                                     (while calling the function from outside of this function
                                     it should be always True)
    :return:                         None
    """

    if top_level:
        list_of_elements = package.TOP_LEVEL_YAML_LISTS

    else:
        list_of_elements = package.SIMULATION_CONFIG_PARAMS

    for list_name in list_of_elements:
        if list_name not in yaml_config or yaml_config[list_name] is None:
            raise ValueError(list_name + ' not specified in loaded configuration! (' + config_file + ')')

        elif list_name == 'simulation_config':
            check_file_format(yaml_config['simulation_config'], config_file, False)


# def read_config(config_dir, config_name):
def read_config(config_file, top_level_conf):
    """
    Recursively read a configuration from a YAML file
    :param config_file:     (str)  Path to the YAML configuration file to read
    :param top_level_conf:  (bool) If we are checking the top level if the main config file
                                   (while calling the function from outside of this function
                                   it should be always True)
    :return:                (Dictionary) Contains the configuration that was read
    """

    config = dict()
    files_to_add = list()

    with open(config_file) as yaml_file:
        yaml_config = yaml.load(yaml_file)

        try:
            if top_level_conf:

                # Test if all required fields are available
                check_file_format(yaml_config, config_file, True)

                # From this point all we can assume all the needed fields exist in the file
                config['simulation_config'] = yaml_config['simulation_config']
                config['network_template'] = yaml_config['network_template']
                config['tb_template'] = yaml_config['tb_template']

            if 'files' in yaml_config:
                for file in yaml_config['files']:
                    files_to_add.append(file)

            if 'designs' in yaml_config:

                for design in yaml_config['designs']:
                    design_config = read_config(os.path.join(package.COMPONENT_CONF_DIR, design + '.yml'), False)

                    if 'files' in design_config:

                        for file in design_config['files']:
                            files_to_add.append(file)

            if files_to_add is not None:
                config['files'] = files_to_add

        except TypeError:
            raise ValueError('Configuration file seems to be empty?!?!?! (' + config_file + ')')

    return config



